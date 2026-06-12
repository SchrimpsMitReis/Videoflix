import json
import subprocess

from video_app.models import Video

def convert_to_hls(video_id):
    """Inspect and print the dimensions of a video's primary stream."""

    video = Video.objects.get(id=video_id)
    path = video.video_file.path

    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)

    video_stream = next(
        (stream for stream in data["streams"] if stream["codec_type"] == "video"),
        None
    )

    if video_stream:
        width = video_stream.get("width")
        height = video_stream.get("height")
        print(width, height)
