from pydub import AudioSegment
import os
from modules.extender.segment_detector import detect_segments 

def extend_music(input_path, start_sec, end_sec, repeat=2, crossfade_ms=1000):
    song = AudioSegment.from_file(input_path)
    duration_sec = len(song) / 1000
    end_sec = min(end_sec, duration_sec)

    start_ms = start_sec * 1000
    end_ms = end_sec * 1000
    
    part_before = song[:start_ms]
    segment_to_loop = song[start_ms:end_ms]
    part_after = song[end_ms:]

    if len(segment_to_loop) == 0:
        raise ValueError("Segmen kosong. Periksa nilai start dan end.")

    extended_part = segment_to_loop
    for _ in range(repeat - 1):
        extended_part = extended_part.append(segment_to_loop, crossfade=crossfade_ms)
        
    output_song = part_before.append(extended_part, crossfade=crossfade_ms)
    output_song = output_song.append(part_after, crossfade=crossfade_ms)

    return output_song


def process_extend(input_path, output_dir="output", start_sec=30, end_sec=60, repeat=2, crossfade_ms=1000):
    os.makedirs(output_dir, exist_ok=True)
    song_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{song_name}_extended.wav")

    result = extend_music(input_path, start_sec, end_sec, repeat, crossfade_ms)
    result.export(output_path, format="wav")
    return output_path


def auto_extend(audio_path, output_dir="output"):
    info = detect_segments(audio_path)
    start, end = info["suggested_segment"]
    print(f"Detected chorus area: {start:.1f}s → {end:.1f}s")

    extended_path = process_extend(audio_path, output_dir, start_sec=start, end_sec=end, repeat=3)
    return extended_path, info