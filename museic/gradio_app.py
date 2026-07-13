import os
import sys
import io
import shutil
import contextlib
import tempfile
import gradio as gr

from museic.core.extender import process_extension
from museic.core.separator import process_separation
from museic.core.extractor import process_extraction
from museic.core.ducker import process_ducking
from museic.core.optimizer import process_optimization
from museic.core.enchancer import process_enhancement
from museic.core.trimmer import process_trimming
from museic.core.vibe import process_vibe

INPUT_DIR = os.path.abspath("input")
OUTPUT_DIR = os.path.abspath("output")
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_file(file_obj):
    if file_obj is None:
        return None, "No file provided"
    dest = os.path.join(INPUT_DIR, os.path.basename(file_obj.name))
    shutil.copy2(file_obj.name, dest)
    return dest, None


def run_capture(func, *args, **kwargs):
    log_capture = io.StringIO()
    with contextlib.redirect_stdout(log_capture):
        try:
            result = func(*args, **kwargs)
            return result, log_capture.getvalue(), None
        except Exception as e:
            return None, log_capture.getvalue(), str(e)


def collect_output_files(dir_path):
    if not dir_path or not os.path.exists(dir_path):
        return None
    if os.path.isfile(dir_path):
        return dir_path
    files = []
    for root, _, filenames in os.walk(dir_path):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files if files else dir_path


with gr.Blocks(title="Museic") as demo:
    gr.Markdown(
        """
        # Museic Audio Engineering Toolkit
        Upload audio, adjust parameters, and process — all locally on your device.
        """
    )

    gr.Markdown("## Extend")
    with gr.Row():
        with gr.Column():
            extend_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            extend_auto = gr.Checkbox(label="Auto-detect loop points", value=True)
            extend_start = gr.Number(label="Start (seconds)", value=0, minimum=0, visible=False)
            extend_end = gr.Number(label="End (seconds)", value=0, minimum=0, visible=False)
            extend_repeat = gr.Number(label="Repeat Count", value=4, minimum=1, maximum=50, step=1)
            extend_btn = gr.Button("Extend Track", variant="primary")
        with gr.Column():
            extend_log = gr.Textbox(label="Log", lines=10)
            extend_output = gr.File(label="Download Extended Audio", file_count="single")

    def on_extend_auto_change(val):
        return gr.update(visible=not val), gr.update(visible=not val)
    extend_auto.change(on_extend_auto_change, inputs=extend_auto, outputs=[extend_start, extend_end])

    def process_extend(file, auto, start, end, repeat):
        path, err = save_file(file)
        if err:
            return err, None
        result, log, err = run_capture(process_extension, input_path=path, start_sec=start, end_sec=end, auto=auto, repeat=int(repeat))
        if err:
            return f"{log}\nError: {err}", None
        return log, result if result else None
    extend_btn.click(process_extend, inputs=[extend_input, extend_auto, extend_start, extend_end, extend_repeat], outputs=[extend_log, extend_output])

    gr.Markdown("## Separate (Stem Isolation)")
    with gr.Row():
        with gr.Column():
            separate_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            separate_start = gr.Number(label="Start (seconds)", value=0, minimum=0)
            separate_end = gr.Number(label="End (seconds)", value=10, minimum=1)
            separate_format = gr.Radio(label="Export Format", choices=["mp3", "wav", "ogg"], value="mp3")
            separate_btn = gr.Button("Separate Stems", variant="primary")
        with gr.Column():
            separate_log = gr.Textbox(label="Log", lines=10)
            separate_output = gr.File(label="Download Stems", file_count="multiple")

    def process_separate(file, start, end, fmt):
        path, err = save_file(file)
        if err:
            return err, None
        result, log, err = run_capture(process_separation, input_path=path, start_sec=start, end_sec=end, target_format=fmt)
        if err:
            return f"{log}\nError: {err}", None
        files = collect_output_files(result)
        return log, files
    separate_btn.click(process_separate, inputs=[separate_input, separate_start, separate_end, separate_format], outputs=[separate_log, separate_output])

    gr.Markdown("## Extract (Smart Hook Detection)")
    with gr.Row():
        with gr.Column():
            extract_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            extract_length = gr.Slider(label="Clip Length (seconds)", minimum=5, maximum=60, value=30, step=5)
            extract_format = gr.Radio(label="Export Format", choices=["mp3", "wav", "ogg"], value="mp3")
            extract_btn = gr.Button("Extract Hook", variant="primary")
        with gr.Column():
            extract_log = gr.Textbox(label="Log", lines=10)
            extract_output = gr.File(label="Download Hook", file_count="multiple")

    def process_extract(file, length, fmt):
        path, err = save_file(file)
        if err:
            return err, None
        result, log, err = run_capture(process_extraction, input_path=path, duration=int(length), export_format=fmt)
        if err:
            return f"{log}\nError: {err}", None
        files = collect_output_files(result)
        return log, files
    extract_btn.click(process_extract, inputs=[extract_input, extract_length, extract_format], outputs=[extract_log, extract_output])

    gr.Markdown("## Mix (Auto-Ducker)")
    with gr.Row():
        with gr.Column():
            mix_voice = gr.File(label="Voice Track", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            mix_bgm = gr.File(label="Background Music", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            mix_btn = gr.Button("Mix Tracks", variant="primary")
        with gr.Column():
            mix_log = gr.Textbox(label="Log", lines=10)
            mix_output = gr.File(label="Download Mixed Audio", file_count="single")

    def process_mix(voice, bgm):
        voice_path, err = save_file(voice)
        if err:
            return err, None
        bgm_path, err = save_file(bgm)
        if err:
            return err, None
        result, log, err = run_capture(process_ducking, voice_path=voice_path, bgm_path=bgm_path)
        if err:
            return f"{log}\nError: {err}", None
        return log, result if result else None
    mix_btn.click(process_mix, inputs=[mix_voice, mix_bgm], outputs=[mix_log, mix_output])

    gr.Markdown("## Optimize (Broadcast Leveling)")
    with gr.Row():
        with gr.Column():
            optimize_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            optimize_lufs = gr.Slider(label="Target LUFS", minimum=-30, maximum=-8, value=-14, step=0.5)
            optimize_btn = gr.Button("Optimize", variant="primary")
        with gr.Column():
            optimize_log = gr.Textbox(label="Log", lines=10)
            optimize_output = gr.File(label="Download Optimized Audio", file_count="single")

    def process_optimize(file, lufs):
        path, err = save_file(file)
        if err:
            return err, None
        result, log, err = run_capture(process_optimization, input_path=path, target_lufs=lufs)
        if err:
            return f"{log}\nError: {err}", None
        return log, result if result else None
    optimize_btn.click(process_optimize, inputs=[optimize_input, optimize_lufs], outputs=[optimize_log, optimize_output])

    gr.Markdown("## Enhance (Noise Reduction & EQ)")
    with gr.Row():
        with gr.Column():
            enhance_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            enhance_denoise = gr.Checkbox(label="Denoise", value=True)
            enhance_boost = gr.Checkbox(label="Boost (compressor + EQ)", value=False)
            enhance_btn = gr.Button("Enhance", variant="primary")
        with gr.Column():
            enhance_log = gr.Textbox(label="Log", lines=10)
            enhance_output = gr.File(label="Download Enhanced Audio", file_count="single")

    def process_enhance(file, denoise, boost):
        path, err = save_file(file)
        if err:
            return err, None
        if not denoise and not boost:
            return "Select at least Denoise or Boost", None
        result, log, err = run_capture(process_enhancement, input_path=path, denoise=denoise, boost=boost)
        if err:
            return f"{log}\nError: {err}", None
        return log, result if result else None
    enhance_btn.click(process_enhance, inputs=[enhance_input, enhance_denoise, enhance_boost], outputs=[enhance_log, enhance_output])

    gr.Markdown("## Trim (Silence Removal)")
    with gr.Row():
        with gr.Column():
            trim_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            trim_aggressive = gr.Checkbox(label="Aggressive mode", value=False)
            trim_btn = gr.Button("Trim Silence", variant="primary")
        with gr.Column():
            trim_log = gr.Textbox(label="Log", lines=10)
            trim_output = gr.File(label="Download Trimmed Audio", file_count="single")

    def process_trim(file, aggressive):
        path, err = save_file(file)
        if err:
            return err, None
        result, log, err = run_capture(process_trimming, input_path=path, aggressive=aggressive)
        if err:
            return f"{log}\nError: {err}", None
        return log, result if result else None
    trim_btn.click(process_trim, inputs=[trim_input, trim_aggressive], outputs=[trim_log, trim_output])

    gr.Markdown("## Vibe (Social Media Effects)")
    with gr.Row():
        with gr.Column():
            vibe_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
            vibe_mode = gr.Radio(label="Effect", choices=["Slowed", "Nightcore"], value="Slowed")
            vibe_btn = gr.Button("Apply Effect", variant="primary")
        with gr.Column():
            vibe_log = gr.Textbox(label="Log", lines=10)
            vibe_output = gr.File(label="Download Modified Audio", file_count="single")

    def process_vibe_fn(file, mode):
        path, err = save_file(file)
        if err:
            return err, None
        slowed = mode == "Slowed"
        nightcore = mode == "Nightcore"
        result, log, err = run_capture(process_vibe, input_path=path, slowed=slowed, nightcore=nightcore)
        if err:
            return f"{log}\nError: {err}", None
        return log, result if result else None
    vibe_btn.click(process_vibe_fn, inputs=[vibe_input, vibe_mode], outputs=[vibe_log, vibe_output])

    gr.Markdown("---")
    gr.Markdown("All processing runs locally. Your audio never leaves your device.")


def main():
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())


if __name__ == "__main__":
    main()
