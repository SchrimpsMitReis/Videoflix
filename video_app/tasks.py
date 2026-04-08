import subprocess
import os
import json

from video_app.models import Video

TARGETS = {
    144: {"width": 256, "bandwidth": 300000},
    240: {"width": 426, "bandwidth": 500000},
    360: {"width": 640, "bandwidth": 900000},
    480: {"width": 854, "bandwidth": 1400000},
    720: {"width": 1280, "bandwidth": 2800000},
    1080: {"width": 1920, "bandwidth": 5000000},
    1440: {"width": 2560, "bandwidth": 8000000},
    2160: {"width": 3840, "bandwidth": 14000000},
}


def convert_480p(video_id):
    video = Video.objects.get(id=video_id)
    source = video.video_file.path

    base, _ = os.path.splitext(source)
    target = base + "_480p.mp4"

    if os.path.exists(target):
        os.remove(target)

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-i", source,
            "-vf", "scale=-2:480",
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "128k",
            target,
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    print("RETURN CODE:", result.returncode)
    print("STDERR:", result.stderr)
    print("TARGET EXISTS:", os.path.exists(target))

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return target


def convert_to_hls(video_id, resolution, codec):
    video = Video.objects.get(id=video_id)
    source = video.video_file.path

    base, _ = os.path.splitext(source)
    video_name = os.path.basename(base)

    output_dir = base + "_480p_hls"
    os.makedirs(output_dir, exist_ok=True)

    playlist_path = os.path.join(output_dir, f"{video_name}_480p.m3u8")
    segment_pattern = os.path.join(output_dir, f"{video_name}_480p_%03d.ts")

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-i", source,
            "-vf", "scale=-2:480",
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "128k",
            "-hls_time", "6",
            "-hls_list_size", "0",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", segment_pattern,
            playlist_path,
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )

    print("RETURN CODE:", result.returncode)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return {
        "output_dir": output_dir,
        "playlist": playlist_path,
    }

# valid_heights = [h for h in TARGET_HEIGHTS if h <= source_height]


def get_video_height(video_path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=height",
            "-of", "json",
            video_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)
    streams = data.get("streams", [])

    if not streams:
        raise ValueError("Kein Videostream gefunden.")

    height = streams[0].get("height")

    if not height:
        raise ValueError("Videohöhe konnte nicht ermittelt werden.")

    return int(height)


def convert_to_hls(video_id):
    video = Video.objects.get(id=video_id)
    source = video.video_file.path
    base_name = os.path.splitext(os.path.basename(source))[0]

    source_height = get_video_height(source)
    valid_heights = [h for h in TARGETS.keys() if h <= source_height]

    base, _ = os.path.splitext(source)
    output_root = base + "_hls"
    os.makedirs(output_root, exist_ok=True)

    variants = []

    for height in valid_heights:
        variant_info = convert_single_hls_variant(source, output_root, height)
        variants.append(variant_info)

    create_master_playlist(output_root, variants, base_name)


def convert_single_hls_variant(source, output_root, height):
    base_name = os.path.splitext(os.path.basename(source))[0]

    playlist_name = f"{base_name}_{height}p.m3u8"
    segment_pattern = os.path.join(
        output_root, f"{base_name}_{height}p_%03d.ts")
    playlist_path = os.path.join(output_root, playlist_name)

    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-i", source,
            "-vf", f"scale=-2:{height}",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "hls",
            "-hls_time", "10",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", segment_pattern,
            playlist_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    print(result.stdout)
    print(result.stderr)

    return {
       "height": height,
        "width": TARGETS[height]["width"],
        "bandwidth": TARGETS[height]["bandwidth"],
        "playlist_name": playlist_name,
    }


def create_master_playlist(output_root, variants, base_name):
    master_path = os.path.join(output_root, f"{base_name}master.m3u8")

    lines = [
       "#EXTM3U",
        "#EXT-X-VERSION:3",
        "",
    ]

    for variant in variants:
        lines.append(
           f'#EXT-X-STREAM-INF:BANDWIDTH={variant["bandwidth"]},RESOLUTION={variant["width"]}x{variant["height"]}'
        )
        lines.append(variant["playlist_name"])
        lines.append("")

    with open(master_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
