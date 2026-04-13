# museic/utils/helpers.py
import os
import shutil
import subprocess
from pydub import AudioSegment

def allowed_file(filename, allowed_ext={"mp3", "wav", "flac", "m4a"}):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext

def convert_to_wav(input_path):
    """Converts supported audio formats to WAV."""
    if input_path.lower().endswith(".wav"):
        return input_path
    
    output_path = os.path.splitext(input_path)[0] + ".wav"
    print(f"[*] Converting {input_path} to WAV format...")
    try:
        AudioSegment.from_file(input_path).export(output_path, format="wav")
        return output_path
    except Exception as e:
        print(f"[!] Error during conversion: {e}")
        raise

def nuclear_cleanup(input_path, output_path):
    """Uses FFmpeg to repair messy or corrupted audio streams."""
    print(f"[*] Running Nuclear Cleanup (FFmpeg repair) on: {input_path}")
    clean_cmd = [
        "ffmpeg", "-y",
        "-err_detect", "ignore_err", 
        "-i", input_path,
        "-vn", # Disable video if any
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        "-max_muxing_queue_size", "1024",
        output_path
    ]
    
    try:
        convert_proc = subprocess.run(clean_cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        error_hint = e.stderr[-300:] if e.stderr else "Unknown FFmpeg Error"
        print(f"[!] FFmpeg repair failed. Hint: {error_hint}")
        return False

def cleanup_temp_files(*filepaths):
    """Safely removes temporary files."""
    for path in filepaths:
        if path and os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                print(f"[!] Failed to remove temp file {path}: {e}")

def get_wsl_path(path):
    """Helper to convert Windows paths to WSL paths dynamically."""
    if path and ":\\" in path:
        try:
            return subprocess.check_output(["wslpath", path]).decode().strip()
        except Exception:
            drive = path[0].lower()
            remainder = path[3:].replace("\\", "/")
            return f"/mnt/{drive}/{remainder}"
    return path