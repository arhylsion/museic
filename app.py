import os
import subprocess
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from modules.splitter.utils import allowed_file
from modules.splitter.demucs_handler import run_demucs
from modules.extender.extender_utils import extend_music, process_extend, auto_extend

app = Flask(__name__)
app.secret_key = "wano"

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
ALLOWED_EXTENSIONS = {"mp3", "wav", "mp4"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# -------------------------
# PAGE ROUTES
# -------------------------
@app.route("/")
def index():
    return render_template("index.html", active_tab="splitter")


# -------------------------
# SPLITTER
# -------------------------
@app.route("/remove", methods=["POST"])
def remove_vocals():
    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Tidak ada file yang dipilih.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Format file tidak didukung (hanya mp3, wav, mp4).")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        subprocess.run(
            ["demucs", "-n", "htdemucs", "-o", OUTPUT_FOLDER, filepath],
            check=True,
        )

        song_name = os.path.splitext(filename)[0]
        result_dir = os.path.join(OUTPUT_FOLDER, "htdemucs", song_name)

        if not os.path.exists(result_dir):
            flash("Proses gagal. Folder hasil tidak ditemukan.")
            return redirect(url_for("index"))

        bass = AudioSegment.from_wav(os.path.join(result_dir, "bass.wav"))
        drums = AudioSegment.from_wav(os.path.join(result_dir, "drums.wav"))
        other = AudioSegment.from_wav(os.path.join(result_dir, "other.wav"))
        instrumental = bass.overlay(drums).overlay(other)
        instrumental.export(os.path.join(result_dir, "no_vocals.wav"), format="wav")

        return render_template(
            "index.html",
            active_tab="splitter",
            has_result=True,
            song=song_name,
            vocals=f"/download/{song_name}/vocals.wav",
            instrumental=f"/download/{song_name}/no_vocals.wav",
            bass=f"/download/{song_name}/bass.wav",
            drums=f"/download/{song_name}/drums.wav",
            other=f"/download/{song_name}/other.wav",
        )

    except subprocess.CalledProcessError:
        flash("Gagal menjalankan Demucs.")
        return redirect(url_for("index"))


@app.route("/download/<song>/<stem>")
def download_file(song, stem):
    folder = os.path.join(OUTPUT_FOLDER, "htdemucs", song)
    return send_from_directory(folder, stem, as_attachment=True)


# -------------------------
# EXTENDER
# -------------------------
@app.route('/extend', methods=['POST'])
def extend_track():
    try:
        if 'file' not in request.files:
            flash("Tidak ada file yang diunggah.")
            return render_template("index.html", active_tab="extender")

        file = request.files['file']
        if file.filename == '':
            flash("Nama file kosong.")
            return render_template("index.html", active_tab="extender")

        filename = secure_filename(file.filename)
        input_path = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(input_path)

        start_sec = float(request.form.get('start_sec', 30))
        end_sec = float(request.form.get('end_sec', 60))
        repeat = int(request.form.get('repeat', 2))
        fade_ms = int(request.form.get('fade_ms', 300))

        output_path = process_extend(
            input_path,
            output_dir="output/",
            start_sec=start_sec,
            end_sec=end_sec,
            repeat=repeat,
            crossfade_ms=fade_ms
        )

        return render_template(
            "index.html",
            active_tab="extender",
            extended=True,
            extended_path="/" + output_path.replace("\\", "/")
        )

    except Exception as e:
        flash(f"Gagal memperpanjang lagu: {str(e)}")
        return render_template("index.html", active_tab="extender")


@app.route("/auto_extend", methods=["POST"])
def auto_extend_route():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    output_path, info = auto_extend(path)
    return render_template(
        "index.html",
        active_tab="extender",
        extended=True,
        extended_path=f"/download_extended/{os.path.basename(output_path)}",
        auto_info=info,
    )


@app.route("/output/<filename>")
def serve_output(filename):
    return send_from_directory(app.config.get("OUTPUT_FOLDER", "output"), filename)

if __name__ == "__main__":
    app.run(debug=True)