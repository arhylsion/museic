import os

TOOLS = ["Extend", "Separate", "Extract", "Mix", "Optimize", "Enhance", "Trim", "Vibe"]

INPUT_DIR = os.path.abspath("input")
OUTPUT_DIR = os.path.abspath("output")
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
