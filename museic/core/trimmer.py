import os
import subprocess
from pathlib import Path

def process_trimming(input_path, output_dir="output", aggressive=False):
    os.makedirs(output_dir, exist_ok=True)
    song_name = Path(input_path).stem
    output_path = os.path.join(output_dir, f"{song_name}_trimmed.mp3")

    print("Analyzing and removing dead silence")

    if aggressive:
        filter_str = "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-30dB"
    else:
        filter_str = "silenceremove=stop_periods=-1:stop_duration=1.0:stop_threshold=-35dB"

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
        raise RuntimeError(f"Trimming engine failed {e}")