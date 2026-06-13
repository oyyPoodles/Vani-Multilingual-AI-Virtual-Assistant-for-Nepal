"""
VANI — Voice Configuration
TTS engine settings and API keys.
"""

import os

# ═══════════════════════════════════════════
# TTS Engine Selection: "coqui" | "elevenlabs" | "auto"
# ═══════════════════════════════════════════
TTS_ENGINE = os.getenv("VANI_TTS_ENGINE", "auto")

# ═══════════════════════════════════════════
# ElevenLabs Configuration (Cloud TTS)
# Set via environment variables for security
# ═══════════════════════════════════════════
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default: Rachel

# ═══════════════════════════════════════════
# Coqui TTS Configuration (Local TTS)
# ═══════════════════════════════════════════
COQUI_MODEL_EN = "tts_models/en/ljspeech/tacotron2-DDC"
COQUI_MODEL_MULTILINGUAL = "tts_models/multilingual/multi-dataset/xtts_v2"

# ═══════════════════════════════════════════
# Audio Output Settings
# ═══════════════════════════════════════════
SAMPLE_RATE = 22050
AUDIO_FORMAT = "wav"

# ═══════════════════════════════════════════
# Language-Voice Mapping
# ═══════════════════════════════════════════
VOICE_MAP = {
    "ne": {"engine": "coqui", "model": COQUI_MODEL_MULTILINGUAL},
    "en": {"engine": "coqui", "model": COQUI_MODEL_EN},
}
