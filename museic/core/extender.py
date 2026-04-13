# museic/core/extender.py
import os
import librosa
import numpy as np
from pydub import AudioSegment

def detect_segments(audio_path):
    """Detects the chorus area using Librosa."""
    print(f"[*] Analyzing tempo and beats for: {audio_path}")
    y, sr = librosa.load(audio_path, mono=True)
    
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    sim_matrix = np.dot(chroma.T, chroma)

    sim_sums = np.sum(sim_matrix, axis=1)
    peak_idx = np.argmax(sim_sums)

    start_sec = max(0, beat_times[peak_idx] - 10)  
    end_sec = min(beat_times[-1], beat_times[peak_idx] + 20)

    return {
        "tempo": tempo,
        "suggested_segment": (round(start_sec, 2), round(end_sec, 2))
    }

def extend_music(input_path, start_sec, end_sec, repeat=2, crossfade_ms=500):
    """Extends a specific segment of the music."""
    print(f"[*] Loading audio for extension...")
    song = AudioSegment.from_file(input_path)
    duration_sec = len(song) / 1000
    end_sec = min(end_sec, duration_sec)

    segment = song[start_sec * 1000:end_sec * 1000]
    if len(segment) == 0:
        raise ValueError("Empty segment. Check start and end values.")

    print(f"[*] Applying crossfade ({crossfade_ms}ms) and extending {repeat} times...")
    segment = segment.fade_in(crossfade_ms // 2).fade_out(crossfade_ms // 2)

    extended_part = segment
    for _ in range(repeat - 1):
        extended_part = extended_part.append(segment, crossfade=crossfade_ms)

    output_song = song[:end_sec * 1000] + extended_part + song[end_sec * 1000:]
    return output_song

def process_extension(input_path, output_dir="output", start_sec=None, end_sec=None, auto=False):
    """Main pipeline for extending a track."""
    os.makedirs(output_dir, exist_ok=True)
    song_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{song_name}_extended.mp3")

    if auto:
        info = detect_segments(input_path)
        start_sec, end_sec = info["suggested_segment"]
        print(f"[+] Auto-detected chorus area: {start_sec:.1f}s -> {end_sec:.1f}s")
    
    if start_sec is None or end_sec is None:
        raise ValueError("Must provide start/end times or use --auto.")

    result_audio = extend_music(input_path, start_sec, end_sec)
    
    print(f"[*] Exporting extended track to: {output_path}")
    result_audio.export(output_path, format="mp3", bitrate="192k") # Default to MP3 for space
    print("[+] Extension complete!")
    return output_path