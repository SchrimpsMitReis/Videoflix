from codec_profiles import CodecProfile

H264_480P = CodecProfile(
    name="480p",
    video_codec="libx264",
    audio_codec="aac",
    height=480,
    audio_bitrate="128k",
    crf=23,
    preset="fast",
)

H264_720P = CodecProfile(
    name="720p",
    video_codec="libx264",
    audio_codec="aac",
    height=720,
    audio_bitrate="128k",
    crf=23,
    preset="fast",
)

H264_1080P = CodecProfile(
    name="1080p",
    video_codec="libx264",
    audio_codec="aac",
    height=1080,
    audio_bitrate="192k",
    crf=23,
    preset="fast",
)

H264_1440P = CodecProfile(
    name="1440p",
    video_codec="libx264",
    audio_codec="aac",
    height=1440,
    audio_bitrate="192k",
    crf=22,  # leicht bessere Qualität
    preset="fast",
)

H264_4K = CodecProfile(
    name="2160p",
    video_codec="libx264",
    audio_codec="aac",
    height=2160,
    audio_bitrate="256k",
    crf=20,  # bessere Qualität für 4K
    preset="slow",  # effizienter bei großen Videos
)