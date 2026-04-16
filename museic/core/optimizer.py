import os
import subprocess
from pathlib import Path

def process_optimization(input_path, output_dir="output", target_lufs=-14.0):
    os.makedirs(output_dir, exist_ok=True)
    song_name = Path(input_path).stem
    output_path = os.path.join(output_dir, f"{song_name}_optimized.mp3")

    print(f"Applying LUFS Normalization ({target_lufs} LUFS)")
    
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", input_path,
        "-af", f"loudnorm=I={target_lufs}:LRA=11:TP=-1.5",
        "-acodec", "libmp3lame",
        "-b:a", "192k",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Optimization complete")
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg optimization failed: {e}")