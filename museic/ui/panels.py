import gradio as gr

from museic.ui.helpers import save_file, stream_capture, collect_output_files
from museic.ui.guide import render_page, render_tips, total_pages
from museic.core.extender import process_extension
from museic.core.separator import process_separation
from museic.core.extractor import process_extraction
from museic.core.ducker import process_ducking
from museic.core.optimizer import process_optimization
from museic.core.enhancer import process_enhancement
from museic.core.trimmer import process_trimming
from museic.core.vibe import process_vibe


def _stream_outputs(core_func, collector, *args, **kwargs):
    """Yield (log, None) during processing, then (log, files) at end."""
    for log_text, result, error in stream_capture(core_func, *args, **kwargs):
        if error:
            yield f"{log_text}\nError: {error}", None
            return
        yield log_text, None
    files = collector(result) if collector and result else None
    yield log_text, files


def build_extend_panel():
    with gr.Column(visible=True) as panel:
        with gr.Row():
            with gr.Column():
                inp = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                auto = gr.Checkbox(label="Auto-detect loop points", value=True)
                start = gr.Number(label="Start (seconds)", value=0, minimum=0, visible=False)
                end = gr.Number(label="End (seconds)", value=0, minimum=0, visible=False)
                repeat = gr.Number(label="Repeat Count", value=4, minimum=1, maximum=50, step=1)
                btn = gr.Button("Extend Track", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Extended Audio", file_count="single")

        def on_auto_change(val):
            return gr.update(visible=not val), gr.update(visible=not val)
        auto.change(on_auto_change, inputs=auto, outputs=[start, end])

        def process(file, do_auto, s, e, r):
            path, err = save_file(file)
            if err:
                yield err, None
                return
            yield from _stream_outputs(
                process_extension, lambda r: r if r else None,
                input_path=path, start_sec=s, end_sec=e, auto=do_auto, repeat=int(r),
            )
        btn.click(process, inputs=[inp, auto, start, end, repeat], outputs=[log, out])
    return panel


def build_separate_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            with gr.Column():
                inp = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                start = gr.Number(label="Start (seconds)", value=0, minimum=0)
                end = gr.Number(label="End (seconds)", value=10, minimum=1)
                fmt = gr.Radio(label="Export Format", choices=["mp3", "wav", "ogg"], value="mp3")
                btn = gr.Button("Separate Stems", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Stems", file_count="multiple")

        def process(file, s, e, f):
            path, err = save_file(file)
            if err:
                yield err, None
                return
            yield from _stream_outputs(
                process_separation, collect_output_files,
                input_path=path, start_sec=s, end_sec=e, target_format=f,
            )
        btn.click(process, inputs=[inp, start, end, fmt], outputs=[log, out])
    return panel


def build_extract_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            with gr.Column():
                inp = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                length = gr.Slider(label="Clip Length (seconds)", minimum=5, maximum=60, value=30, step=5)
                fmt = gr.Radio(label="Export Format", choices=["mp3", "wav", "ogg"], value="mp3")
                btn = gr.Button("Extract Hook", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Hook", file_count="multiple")

        def process(file, l, f):
            path, err = save_file(file)
            if err:
                yield err, None
                return
            yield from _stream_outputs(
                process_extraction, collect_output_files,
                input_path=path, duration=int(l), export_format=f,
            )
        btn.click(process, inputs=[inp, length, fmt], outputs=[log, out])
    return panel


def build_mix_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            with gr.Column():
                voice = gr.File(label="Voice Track", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                bgm = gr.File(label="Background Music", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                btn = gr.Button("Mix Tracks", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Mixed Audio", file_count="single")

        def process(v, b):
            vpath, err = save_file(v)
            if err:
                yield err, None
                return
            bpath, err = save_file(b)
            if err:
                yield err, None
                return
            yield from _stream_outputs(
                process_ducking, lambda r: r if r else None,
                voice_path=vpath, bgm_path=bpath,
            )
        btn.click(process, inputs=[voice, bgm], outputs=[log, out])
    return panel


def build_optimize_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            with gr.Column():
                inp = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                lufs = gr.Slider(label="Target LUFS", minimum=-30, maximum=-8, value=-14, step=0.5)
                btn = gr.Button("Optimize", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Optimized Audio", file_count="single")

        def process(file, l):
            path, err = save_file(file)
            if err:
                yield err, None
                return
            yield from _stream_outputs(
                process_optimization, lambda r: r if r else None,
                input_path=path, target_lufs=l,
            )
        btn.click(process, inputs=[inp, lufs], outputs=[log, out])
    return panel


def build_enhance_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            with gr.Column():
                inp = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                denoise = gr.Checkbox(label="Denoise (reduce background hiss/hum)", value=True)
                boost = gr.Checkbox(label="Boost voice (compressor + EQ)", value=False)
                btn = gr.Button("Enhance", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Enhanced Audio", file_count="single")

        def process(file, d, b):
            path, err = save_file(file)
            if err:
                yield err, None
                return
            if not d and not b:
                yield "Select at least Denoise or Boost", None
                return
            yield from _stream_outputs(
                process_enhancement, lambda r: r if r else None,
                input_path=path, denoise=d, boost=b,
            )
        btn.click(process, inputs=[inp, denoise, boost], outputs=[log, out])
    return panel


def build_trim_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            with gr.Column():
                inp = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                aggressive = gr.Checkbox(label="Aggressive mode (remove shorter pauses)", value=False)
                btn = gr.Button("Trim Silence", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Trimmed Audio", file_count="single")

        def process(file, agg):
            path, err = save_file(file)
            if err:
                yield err, None
                return
            yield from _stream_outputs(
                process_trimming, lambda r: r if r else None,
                input_path=path, aggressive=agg,
            )
        btn.click(process, inputs=[inp, aggressive], outputs=[log, out])
    return panel


def build_vibe_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            with gr.Column():
                inp = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                mode = gr.Radio(label="Effect", choices=["Slowed", "Slowed + Reverb", "Nightcore"], value="Slowed")
                btn = gr.Button("Apply Effect", variant="primary")
            with gr.Column():
                log = gr.Textbox(label="Log", lines=10)
                out = gr.File(label="Download Modified Audio", file_count="single")

        def process(file, m):
            path, err = save_file(file)
            if err:
                yield err, None
                return
            yield from _stream_outputs(
                process_vibe, lambda r: r if r else None,
                input_path=path, slowed=(m=="Slowed"), slowed_reverb=(m=="Slowed + Reverb"), nightcore=(m=="Nightcore"),
            )
        btn.click(process, inputs=[inp, mode], outputs=[log, out])
    return panel


def build_guide_panel():
    with gr.Column(visible=False) as panel:
        with gr.Row():
            lang = gr.Radio(
                choices=["id", "en", "jp"], value="en",
                label="", show_label=False,
                elem_classes="lang-select",
            )
        content = gr.Markdown(render_page("en", 1), elem_classes="guide-content")
        tips = gr.Markdown(render_tips("en"))
        with gr.Row():
            page_disp = gr.Markdown("**1/8**", scale=0)
            prev = gr.Button("<", size="sm", scale=0, min_width=40)
            next = gr.Button(">", size="sm", scale=0, min_width=40)
    return panel, lang, content, tips, page_disp, prev, next
