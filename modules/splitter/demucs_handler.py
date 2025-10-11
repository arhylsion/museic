import os
import subprocess
from pathlib import Path
from pydub import AudioSegment

def run_demucs(input_path, output_root="output", model="htdemucs"):
    os.makedirs(output_root, exist_ok=True)

    subprocess.run([
        "demucs",
        "-n", model,
        "-o", output_root,
        input_path
    ], check=True)

    song_name = Path(input_path).stem
    result_dir = Path(output_root) / model / song_name

    if not result_dir.exists():
        raise FileNotFoundError(f"Folder hasil tidak ditemukan: {result_dir}")
    bass_path = result_dir / "bass.wav"
    drums_path = result_dir / "drums.wav"
    other_path = result_dir / "other.wav"
    no_vocals_path = result_dir / "no_vocals.wav"

    if all(p.exists() for p in [bass_path, drums_path, other_path]):
        bass = AudioSegment.from_wav(bass_path)
        drums = AudioSegment.from_wav(drums_path)
        other = AudioSegment.from_wav(other_path)
        combined = bass.overlay(drums).overlay(other)
        combined.export(no_vocals_path, format="wav")

    result = {
        "vocals": str(result_dir / "vocals.wav"),
        "bass": str(result_dir / "bass.wav"),
        "drums": str(result_dir / "drums.wav"),
        "other": str(result_dir / "other.wav"),
        "instrumental": str(result_dir / "no_vocals.wav")
    }

    return result
