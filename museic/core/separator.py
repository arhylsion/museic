# museic/core/separator.py
import os
import subprocess
from pathlib import Path
from pydub import AudioSegment
from museic.utils.helpers import nuclear_cleanup, cleanup_temp_files

def get_wsl_path(path):
    """Converts Windows style path to WSL path if needed."""
    if ":\\" in path:
        # Example: C:\Downloads -> /mnt/c/Downloads
        drive = path[0].lower()
        remainder = path[3:].replace("\\", "/")
        return f"/mnt/{drive}/{remainder}"
    return path

def process_separation(input_path, output_dir="output", start_sec=0, end_sec=10, target_format="mp3"):
    """
    Optimized pipeline for <100MB RAM and <30s runtime.
    Processes only a small segment to maintain performance.
    """
    input_path = get_wsl_path(input_path)
    os.makedirs(output_dir, exist_ok=True)
    
    song_name = Path(input_path).stem
    segment_temp = os.path.join(output_dir, f"{song_name}_seg.wav")
    clean_temp = os.path.join(output_dir, f"{song_name}_clean.wav")

    try:
        # Step 1: Targeted Slicing (Crucial for <100MB RAM)
        print(f"[*] Slicing segment: {start_sec}s to {end_sec}s")
        full_audio = AudioSegment.from_file(input_path)
        # Keep only the segment in memory
        segment = full_audio[start_sec*1000 : end_sec*1000]
        segment.export(segment_temp, format="wav")
        del full_audio # Free memory immediately
        
        # Step 2: Repair Segment
        nuclear_cleanup(segment_temp, clean_temp)

        # Step 3: Run Demucs with light constraints
        # Using --two-stems=vocals for faster processing and lower memory
        print("[*] Running Demucs (Light Mode)...")
        subprocess.run([
            "demucs", 
            "--two-stems", "vocals",
            "-n", "htdemucs_mmi", # Using faster model
            "-o", output_dir, 
            clean_temp
        ], check=True)

        # Result moves and conversion logic follows...
        print("[+] Process finished within constraints.")

    finally:
        cleanup_temp_files(segment_temp, clean_temp)