from dataclasses import dataclass

@dataclass
class CodecProfile:
    """Describe the encoding settings for one video output profile."""

    name: str
    video_codec: str
    audio_codec: str
    height: int
    audio_bitrate: str
    crf: int
    preset: str
