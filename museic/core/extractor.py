import os
import librosa
import numpy as np
from museic.core.separator import process_separation

def find_the_hook(audio_path, duration_sec=30):
    y, sr = librosa.load(audio_path, sr=8000, mono=True)
    rms = librosa.feature.rms(y=y)[0]
    frames_in_slice = librosa.time_to_frames(duration_sec, sr=sr)
    
    max_energy = 0
    best_start_frame = 0
    
    for i in range(len(rms) - frames_in_slice):
        window_energy = np.sum(rms[i:i+frames_in_slice])
        if window_energy > max_energy:
            max_energy = window_energy
            best_start_frame = i
            
    start_time = librosa.frames_to_time(best_start_frame, sr=sr)
    return start_time, start_time + duration_sec

def process_extraction(input_path, duration=30, export_format="mp3", output_dir="output"):
    print("Running Smart Hook Detection")
    start_sec, end_sec = find_the_hook(input_path, duration_sec=duration)
    
    print(f"Hook isolated at {start_sec:.2f}s to {end_sec:.2f}s")
    
    out_dir = process_separation(
        input_path=input_path,
        output_dir=output_dir,
        start_sec=start_sec,
        end_sec=end_sec,
        target_format=export_format
    )
    return out_dir