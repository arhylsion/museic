import os
import subprocess
import gc
from pathlib import Path
from pydub import AudioSegment
from museic.utils.helpers import nuclear_cleanup, cleanup_temp_files

def process_separation(input_path, output_dir="output", start_sec=0, end_sec=10, target_format="mp3"):
    os.makedirs(output_dir, exist_ok=True)
    
    song_name = Path(input_path).stem
    segment_temp = os.path.join(output_dir, f"{song_name}_seg.wav")
    clean_temp = os.path.join(output_dir, f"{song_name}_clean.wav")

    try:
        print("Extracting target slice")
        full_audio = AudioSegment.from_file(input_path)
        segment = full_audio[int(start_sec*1000) : int(end_sec*1000)]
        segment.export(segment_temp, format="wav")
        
        del full_audio
        del segment
        gc.collect()
        
        nuclear_cleanup(segment_temp, clean_temp)

        print("Running Demucs engine")
        subprocess.run([
            "demucs", 
            "--two-stems", "vocals",
            "-n", "mdx_extra_q", 
            "-j", "4",
            "--shifts", "0",
            "--overlap", "0.1",
            "-o", output_dir, 
            clean_temp
        ], check=True, stdout=subprocess.DEVNULL)

        print("Processing separated stems")
        demucs_result_dir = os.path.join(output_dir, "mdx_extra_q", f"{song_name}_clean")
        final_song_dir = os.path.join(output_dir, song_name)

        if not os.path.exists(demucs_result_dir):
            raise FileNotFoundError("Engine failed to output files")

        os.makedirs(final_song_dir, exist_ok=True)

        vocals = AudioSegment.from_wav(os.path.join(demucs_result_dir, "vocals.wav"))
        instrumental = AudioSegment.from_wav(os.path.join(demucs_result_dir, "no_vocals.wav"))

        stems = {"vocals": vocals, "instrumental": instrumental}

        print("Exporting stems")
        for stem_name, audio_data in stems.items():
            out_file = os.path.join(final_song_dir, f"{stem_name}.{target_format}")
            bitrate = "192k" if target_format == "mp3" else None
            audio_data.export(out_file, format=target_format, bitrate=bitrate)

        return final_song_dir

    finally:
        cleanup_temp_files(segment_temp, clean_temp)
        raw_model_dir = os.path.join(output_dir, "mdx_extra_q")
        cleanup_temp_files(raw_model_dir)