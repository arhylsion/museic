"""Audit script: test all Museic tools inside Docker container."""
import subprocess, sys, os

IN = "/workspace/input/test_long.mp3"

print("=== Generating test audio ===")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
    "-f", "lavfi", "-i", "sine=frequency=440:duration=20", "-ac", "1", "-ar", "44100", IN], check=True)
print("test_long.mp3 ready")

os.chdir("/workspace")
sys.path.insert(0, "/workspace")

from museic.core.extender import process_extension
from museic.core.separator import process_separation
from museic.core.extractor import process_extraction
from museic.core.ducker import process_ducking
from museic.core.optimizer import process_optimization
from museic.core.enchancer import process_enhancement
from museic.core.trimmer import process_trimming
from museic.core.vibe import process_vibe

def test(name, fn, **kwargs):
    try:
        result = fn(**kwargs)
        print(f"  {name}: completed fine")
    except Exception as e:
        print(f"  {name}: ERROR -> {e}")

tests = [
    ("Extend", process_extension, dict(input_path=IN, auto=True, repeat=2)),
    ("Separate", process_separation, dict(input_path=IN, start_sec=0, end_sec=10)),
    ("Extract", process_extraction, dict(input_path=IN, duration=5)),
    ("Mix", process_ducking, dict(voice_path=IN, bgm_path=IN)),
    ("Optimize", process_optimization, dict(input_path=IN)),
    ("Enhance", process_enhancement, dict(input_path=IN, denoise=True, boost=False)),
    ("Trim", process_trimming, dict(input_path=IN, aggressive=False)),
    ("Vibe/Slowed", process_vibe, dict(input_path=IN, slowed=True)),
    ("Vibe/Slowed+Reverb", process_vibe, dict(input_path=IN, slowed_reverb=True)),
    ("Vibe/Nightcore", process_vibe, dict(input_path=IN, nightcore=True)),
]

for name, fn, kwargs in tests:
    test(name, fn, **kwargs)

print("\n=== Audit complete ===")
