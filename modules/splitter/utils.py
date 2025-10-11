import os
from pydub import AudioSegment

def allowed_file(filename, allowed_ext={"mp3", "wav", "flac", "m4a"}):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext

def convert_to_wav(input_path):
    if input_path.lower().endswith(".wav"):
        return input_path

    output_path = os.path.splitext(input_path)[0] + ".wav"
    AudioSegment.from_file(input_path).export(output_path, format="wav")
    return output_path

def cleanup_old_outputs(folder="output"):
    if not os.path.exists(folder):
        return

    for root, dirs, files in os.walk(folder):
        for f in files:
            try:
                os.remove(os.path.join(root, f))
            except Exception as e:
                print(f"Gagal hapus {f}: {e}")
