import os
from pydub import AudioSegment
from tqdm import tqdm

def process_ducking(voice_path, bgm_path, output_dir="output", ducking_db=-15, threshold_db=-40):
    os.makedirs(output_dir, exist_ok=True)
    song_name = os.path.splitext(os.path.basename(voice_path))[0]
    output_path = os.path.join(output_dir, f"{song_name}_mixed.mp3")

    print("Loading audio tracks")
    voice = AudioSegment.from_file(voice_path)
    bgm = AudioSegment.from_file(bgm_path)

    if len(bgm) < len(voice):
        loops = (len(voice) // len(bgm)) + 1
        bgm = bgm * loops

    bgm = bgm[:len(voice)]

    print("Applying Auto-Ducking")
    chunk_size = 50
    mixed_chunks = []
    current_reduction = 0.0
    attack = 0.3
    release = 0.05

    for i in tqdm(range(0, len(voice), chunk_size), desc="Mixing", bar_format="{l_bar}{bar} {n_fmt} {total_fmt}"):
        v_chunk = voice[i:i+chunk_size]
        b_chunk = bgm[i:i+chunk_size]

        target = abs(ducking_db) if v_chunk.dBFS > threshold_db else 0
        if target > current_reduction:
            current_reduction = current_reduction * (1 - attack) + target * attack
        else:
            current_reduction = current_reduction * (1 - release) + target * release

        if current_reduction > 0.5:
            b_chunk = b_chunk - current_reduction

        mixed_chunks.append(v_chunk.overlay(b_chunk))

    final_mix = sum(mixed_chunks)

    print("Exporting mixed audio")
    final_mix.export(output_path, format="mp3", bitrate="192k")
    return output_path