import os
import subprocess
import gc
import shutil
from pathlib import Path
from pydub import AudioSegment
from museic.utils.helpers import cleanup_temp_files

def process_separation(input_path, output_dir="output", start_sec=0, end_sec=10, target_format="mp3"):
    os.makedirs(output_dir, exist_ok=True)
    
    song_name = Path(input_path).stem
    temp_wav = os.path.join(output_dir, f"{song_name}_temp.wav")
    final_song_dir = os.path.join(output_dir, song_name)

    try:
        print("Extracting target slice")
        full_audio = AudioSegment.from_file(input_path)
        
        start_ms = int(start_sec * 1000)
        end_ms = int(end_sec * 1000) if end_sec > 0 else len(full_audio)
        
        segment = full_audio[start_ms:end_ms]
        segment.export(temp_wav, format="wav")
        
        del full_audio
        del segment
        gc.collect()

        print("Running Demucs engine")
        subprocess.run([
            "demucs", 
            "--two-stems", "vocals",
            "-n", "mdx_extra_q", 
            "-j", "4",
            "--shifts", "0",
            "--overlap", "0.1",
            "-o", output_dir, 
            temp_wav
        ], check=True, stdout=subprocess.DEVNULL)

        print("Processing separated stems")
        demucs_result_dir = os.path.join(output_dir, "mdx_extra_q", f"{song_name}_temp")

        if not os.path.exists(demucs_result_dir):
            raise FileNotFoundError("Engine failed to output files")

        os.makedirs(final_song_dir, exist_ok=True)

        vocals = AudioSegment.from_wav(os.path.join(demucs_result_dir, "vocals.wav"))
        instrumental = AudioSegment.from_wav(os.path.join(demucs_result_dir, "no_vocals.wav"))

        print(f"Exporting stems to {target_format.upper()}")
        vocals.export(os.path.join(final_song_dir, f"vocals.{target_format}"), format=target_format, bitrate="192k")
        instrumental.export(os.path.join(final_song_dir, f"instrumental.{target_format}"), format=target_format, bitrate="192k")

        return final_song_dir

    finally:
        cleanup_temp_files(temp_wav)
        raw_model_dir = os.path.join(output_dir, "mdx_extra_q")
        if os.path.exists(raw_model_dir):
            shutil.rmtree(raw_model_dir, ignore_errors=True)