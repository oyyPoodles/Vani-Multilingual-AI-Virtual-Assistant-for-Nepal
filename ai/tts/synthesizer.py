"""
VANI — Text-to-Speech Synthesizer
Supports Coqui TTS (local) and ElevenLabs (cloud).
Config-switchable via voice_config.py.
"""

import os
import logging
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)


class TTSSynthesizer:
    """Generates speech audio from text responses."""

    def __init__(self, engine: str = "auto", language: str = "en"):
        self.engine = engine  # "coqui", "elevenlabs", or "auto"
        self.language = language
        self._coqui_model = None
        self._eleven_client = None

    def synthesize(self, text: str, output_path: Optional[str] = None, language: str = None) -> str:
        """
        Convert text to speech audio file.

        Args:
            text: Text to synthesize
            output_path: Output audio file path (auto-generated if None)
            language: Override language ('ne' or 'en')

        Returns:
            Path to generated audio file
        """
        lang = language or self.language
        if output_path is None:
            output_path = tempfile.mktemp(suffix=".wav")

        if self.engine == "auto":
            try:
                return self._synthesize_coqui(text, output_path, lang)
            except (ImportError, Exception) as e:
                logger.warning(f"Coqui TTS unavailable ({e}), trying ElevenLabs")
                return self._synthesize_elevenlabs(text, output_path, lang)
        elif self.engine == "coqui":
            return self._synthesize_coqui(text, output_path, lang)
        elif self.engine == "elevenlabs":
            return self._synthesize_elevenlabs(text, output_path, lang)
        else:
            raise ValueError(f"Unknown TTS engine: {self.engine}")

    def _synthesize_coqui(self, text: str, output_path: str, language: str) -> str:
        """Synthesize using Coqui TTS (local, free)."""
        try:
            from TTS.api import TTS

            if self._coqui_model is None:
                model_name = "tts_models/en/ljspeech/tacotron2-DDC"
                if language == "ne":
                    # Use multilingual model for Nepali
                    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
                self._coqui_model = TTS(model_name)
                logger.info(f"Coqui TTS model loaded: {model_name}")

            self._coqui_model.tts_to_file(text=text, file_path=output_path)
            logger.info(f"Coqui TTS generated: {output_path}")
            return output_path

        except ImportError:
            raise ImportError("Coqui TTS not installed. Run: pip install TTS")

    def _synthesize_elevenlabs(self, text: str, output_path: str, language: str) -> str:
        """Synthesize using ElevenLabs API (cloud, paid)."""
        from .voice_config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

        if not ELEVENLABS_API_KEY:
            raise ValueError("ElevenLabs API key not configured in voice_config.py")

        try:
            import requests

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            mp3_path = output_path.replace('.wav', '.mp3')
            with open(mp3_path, 'wb') as f:
                f.write(response.content)

            logger.info(f"ElevenLabs TTS generated: {mp3_path}")
            return mp3_path

        except ImportError:
            raise ImportError("requests not installed. Run: pip install requests")
