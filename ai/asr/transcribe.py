"""
VANI ASR — Speech-to-Text Pipeline using Faster Whisper
Supports Nepali, English, and code-switched input.
Target WER: < 15%
"""

import os
import wave
import tempfile
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════
# TRAINING PLACEHOLDER
# This section is intentionally left for
# execution on a separate training machine.
# Dataset: datasets/speech/nepali_commands/
# Model: faster-whisper (large-v3)
# Output: ai/asr/models/whisper_finetuned/
# Fine-tuning NOT done here — use pretrained.
# ═══════════════════════════════════════════


class WhisperTranscriber:
    """Transcribes audio using Faster Whisper (pretrained)."""

    def __init__(self, model_size: str = "large-v3", device: str = "auto", compute_type: str = "float16"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load_model(self):
        """Load the Faster Whisper model."""
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            logger.info(f"Whisper model '{self.model_size}' loaded successfully.")
        except ImportError:
            logger.error("faster-whisper not installed. Run: pip install faster-whisper")
            raise
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to audio file (WAV, MP3, FLAC, etc.)
            language: Optional language hint ('ne' for Nepali, 'en' for English, None for auto)

        Returns:
            Dict with keys: text, language, segments, confidence
        """
        if self.model is None:
            self.load_model()

        try:
            segments, info = self.model.transcribe(
                audio_path,
                language=language,
                beam_size=5,
                best_of=5,
                temperature=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    speech_pad_ms=400
                )
            )

            all_segments = []
            full_text = []

            for segment in segments:
                all_segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                    "avg_logprob": segment.avg_logprob,
                    "no_speech_prob": segment.no_speech_prob
                })
                full_text.append(segment.text.strip())

            result = {
                "text": " ".join(full_text),
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "segments": all_segments
            }

            logger.info(f"Transcription complete: lang={info.language}, "
                        f"prob={info.language_probability:.2f}, "
                        f"text='{result['text'][:80]}...'")
            return result

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def transcribe_stream(self, audio_chunks, language: Optional[str] = None):
        """
        Transcribe streaming audio chunks.

        Args:
            audio_chunks: Generator/iterator of audio byte chunks
            language: Optional language hint

        Yields:
            Partial transcription results
        """
        if self.model is None:
            self.load_model()

        # Buffer audio to temp file for processing
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            # Write WAV header + accumulated chunks
            for chunk in audio_chunks:
                tmp.write(chunk)

        try:
            result = self.transcribe(tmp_path, language=language)
            yield result
        finally:
            os.unlink(tmp_path)


class AudioRecorder:
    """Records audio from microphone for transcription."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size

    def record(self, duration: float = 5.0, output_path: Optional[str] = None) -> str:
        """
        Record audio from microphone.

        Args:
            duration: Recording duration in seconds
            output_path: Optional output file path

        Returns:
            Path to recorded WAV file
        """
        try:
            import pyaudio
        except ImportError:
            logger.error("pyaudio not installed. Run: pip install pyaudio")
            raise

        if output_path is None:
            output_path = tempfile.mktemp(suffix=".wav")

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        logger.info(f"Recording for {duration}s...")
        frames = []
        for _ in range(int(self.sample_rate / self.chunk_size * duration)):
            data = stream.read(self.chunk_size)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save as WAV
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))

        logger.info(f"Audio saved to {output_path}")
        return output_path


# ═══════════════════════════════════════════
# Pipeline: Mic → Noise Reduction → Whisper → Text
# ═══════════════════════════════════════════

def transcribe_from_mic(
    duration: float = 5.0,
    language: Optional[str] = None,
    denoise: bool = True,
    model_size: str = "large-v3"
) -> Dict[str, Any]:
    """
    Full pipeline: Record from mic → denoise → transcribe.

    Args:
        duration: Recording duration in seconds
        language: Language hint (None=auto, 'ne'=Nepali, 'en'=English)
        denoise: Whether to apply noise reduction
        model_size: Whisper model size

    Returns:
        Transcription result dict
    """
    from .noise_reduction import denoise_audio

    recorder = AudioRecorder()
    audio_path = recorder.record(duration=duration)

    if denoise:
        audio_path = denoise_audio(audio_path)

    transcriber = WhisperTranscriber(model_size=model_size)
    result = transcriber.transcribe(audio_path, language=language)

    # Clean up temp files
    if os.path.exists(audio_path):
        os.unlink(audio_path)

    return result
