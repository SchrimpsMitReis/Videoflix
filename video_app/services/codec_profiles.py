from dataclasses import dataclass

@dataclass
class CodecProfile:
    name: str
    video_codec: str
    audio_codec: str
    height: int
    audio_bitrate: str
    crf: int
    preset: str