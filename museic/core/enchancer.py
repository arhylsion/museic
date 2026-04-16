import os
import subprocess
from pathlib import Path

def process_enhancement(input_path, output_dir="output", denoise=False, boost=False):
    os.makedirs(output_dir, exist_ok=True)
    song_name = Path(input_path).stem
    output_path = os.path.join(output_dir, f"{song_name}_enhanced.mp3")

    print("Initializing audio enhancement pipeline")
    filters = []

    if denoise:
        filters.append("afftdn=nf=-25")

    if boost:
        filters.append("acompressor=threshold=-20dB:ratio=4:attack=5:release=50")
        filters.append("treble=g=4")
        filters.append("bass=g=2")

    if not filters:
        raise ValueError("No enhancement flags provided")

    filter_str = ",".join(filters)
    print("Applying acoustic filters")

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", input_path,
        "-af", filter_str,
        "-acodec", "libmp3lame",
        "-b:a", "192k",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Enhancement engine failed {e}")