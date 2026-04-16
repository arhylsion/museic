import os
import subprocess
from pathlib import Path

def process_vibe(input_path, output_dir="output", slowed=False, nightcore=False):
    os.makedirs(output_dir, exist_ok=True)
    song_name = Path(input_path).stem
    
    filters = []
    if slowed:
        output_path = os.path.join(output_dir, f"{song_name}_slowed.mp3")
        filters.append("asetrate=44100*0.85,aresample=44100,aecho=0.8:0.9:1000:0.3")
    elif nightcore:
        output_path = os.path.join(output_dir, f"{song_name}_nightcore.mp3")
        filters.append("asetrate=44100*1.25,aresample=44100")
    else:
        raise ValueError("Must select either slowed or nightcore")

    print("Applying dynamic tempo and spatial filters")
    
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", input_path,
        "-af", ",".join(filters),
        "-acodec", "libmp3lame",
        "-b:a", "192k",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Vibe engine failed {e}")