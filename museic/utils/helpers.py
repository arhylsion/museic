import os
import shutil
import subprocess

def get_wsl_path(path):
    if path and ":\\" in path:
        try:
            return subprocess.check_output(["wslpath", path]).decode().strip()
        except Exception:
            drive = path[0].lower()
            remainder = path[3:].replace("\\", "/")
            return f"/mnt/{drive}/{remainder}"
    return path

def nuclear_cleanup(input_path, output_path):
    print(f"[*] Running FFmpeg stream repair...")
    clean_cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-err_detect", "ignore_err", 
        "-i", input_path,
        "-vn", 
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        output_path
    ]
    
    try:
        subprocess.run(clean_cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        print("[!] FFmpeg repair failed. File might be severely corrupted.")
        return False

def cleanup_temp_files(*filepaths):
    for path in filepaths:
        if path and os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                pass