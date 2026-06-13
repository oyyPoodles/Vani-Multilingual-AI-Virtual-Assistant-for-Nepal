"""
VANI — Audio Noise Reduction
Uses DeepFilterNet or fallback spectral gating for noise cleanup.
"""

import os
import logging
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)


def denoise_audio(input_path: str, output_path: Optional[str] = None, method: str = "auto") -> str:
    """
    Remove noise from audio file.

    Args:
        input_path: Path to noisy audio file
        output_path: Path to save cleaned audio (auto-generated if None)
        method: 'deepfilter', 'spectral', or 'auto'

    Returns:
        Path to denoised audio file
    """
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_clean{ext}"

    if method == "auto":
        # Try DeepFilterNet first, fall back to spectral gating
        try:
            return _denoise_deepfilter(input_path, output_path)
        except (ImportError, Exception) as e:
            logger.warning(f"DeepFilterNet unavailable ({e}), falling back to spectral gating")
            return _denoise_spectral(input_path, output_path)
    elif method == "deepfilter":
        return _denoise_deepfilter(input_path, output_path)
    elif method == "spectral":
        return _denoise_spectral(input_path, output_path)
    else:
        raise ValueError(f"Unknown denoising method: {method}")


def _denoise_deepfilter(input_path: str, output_path: str) -> str:
    """Denoise using DeepFilterNet (high quality)."""
    try:
        from df.enhance import enhance, init_df, load_audio, save_audio

        model, df_state, _ = init_df()
        audio, _ = load_audio(input_path, sr=df_state.sr())
        enhanced = enhance(model, df_state, audio)
        save_audio(output_path, enhanced, sr=df_state.sr())

        logger.info(f"DeepFilterNet denoising complete: {output_path}")
        return output_path
    except ImportError:
        raise ImportError("DeepFilterNet not installed. Run: pip install deepfilternet")


def _denoise_spectral(input_path: str, output_path: str) -> str:
    """Denoise using spectral gating (lightweight fallback)."""
    try:
        import noisereduce as nr
        import soundfile as sf
        import numpy as np

        data, rate = sf.read(input_path)

        # Apply spectral gating noise reduction
        reduced = nr.reduce_noise(
            y=data,
            sr=rate,
            stationary=True,
            prop_decrease=0.75,
            freq_mask_smooth_hz=500,
            time_mask_smooth_ms=50
        )

        sf.write(output_path, reduced, rate)
        logger.info(f"Spectral gating denoising complete: {output_path}")
        return output_path
    except ImportError:
        logger.warning("noisereduce/soundfile not installed. Returning original audio.")
        return input_path
