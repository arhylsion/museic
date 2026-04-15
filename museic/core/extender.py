import os
import librosa
from pydub import AudioSegment
from tqdm import tqdm

def find_loop_points(audio_path, edge_duration=5.0):
    total_duration = librosa.get_duration(path=audio_path)
    
    if total_duration < edge_duration * 2:
        return 0, total_duration 

    y_start, sr = librosa.load(audio_path, sr=22050, duration=edge_duration)
    onsets_start = librosa.onset.onset_detect(y=y_start, sr=sr, units='time')
    
    y_end, _ = librosa.load(audio_path, sr=22050, offset=total_duration - edge_duration)
    onsets_end = librosa.onset.onset_detect(y=y_end, sr=sr, units='time')

    first_beat = onsets_start[0] if len(onsets_start) > 0 else 0.0
    last_beat = (total_duration - edge_duration) + onsets_end[-1] if len(onsets_end) > 0 else total_duration

    return first_beat, last_beat

def process_extension(input_path, start_sec=0, end_sec=0, auto=False, repeat=2, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    song_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{song_name}_extended.mp3")

    print("Loading track into memory")
    song = AudioSegment.from_file(input_path)

    if auto:
        print("Running Edge Beat Sync")
        first_beat, last_beat = find_loop_points(input_path)
        
        start_ms = int(first_beat * 1000)
        end_ms = int(last_beat * 1000)
        song_core = song[start_ms:end_ms]
        
        crossfade_ms = 4500 
    else:
        song_core = song
        crossfade_ms = 0

    print("Linking track")
    
    extended_song = song_core
    song_core_faded = song_core.fade_in(crossfade_ms).fade_out(crossfade_ms)
    
    for _ in tqdm(range(repeat - 1), desc="Looping", bar_format="{l_bar}{bar} {n_fmt} {total_fmt}"):
        extended_song = extended_song.append(song_core_faded, crossfade=crossfade_ms)

    extended_song = extended_song.fade_out(3000)

    print("Exporting audio")
    extended_song.export(
        output_path, 
        format="mp3", 
        bitrate="192k",
        parameters=["-threads", "4", "-preset", "ultrafast"] 
    )
    
    return output_path