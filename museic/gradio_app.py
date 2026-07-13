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


guide_pages = [
    {
        "EN": ("Extend", "Loop and extend audio tracks seamlessly -- automatically detects beat-aligned loop points or lets you set them manually. Perfect for making background music longer. Supports automatic edge-beat sync or manual start/end markers."),
        "ID": ("Extend (Perpanjang)", "Memperpanjang audio dengan loop point presisi. Auto-deteksi beat atau atur manual start/end. Cocok untuk membuat musik latar yang lebih panjang tanpa jeda."),
        "JP": ("Extend (延长)", "オーディオをシームレスにループ延长。ビートに合わせたループポイントを自動検出または手動設定可能。BGM制作に最適。"),
    },
    {
        "EN": ("Separate", "Isolate vocals and instrumental stems using the Demucs AI engine. Process only a specific time slice to save memory and time. Exports as clean separate files ready for remixing or karaoke."),
        "ID": ("Separate (Pisahkan)", "Pisahkan vokal dan instrumental menggunakan AI Demucs. Proses hanya potongan waktu tertentu untuk hemat memori. Ekspor sebagai file terpisah siap pakai."),
        "JP": ("Separate (分離)", "Demucs AIエンジンを使用してボーカルと楽器を分離。特定の時間範囲のみ処理してメモリと時間を節約。"),
    },
    {
        "EN": ("Extract", "Automatically detect the most energetic part of a song (the hook or chorus) and extract it. Uses Separate internally to produce clean vocal and instrumental stems of the hook."),
        "ID": ("Extract (Ekstrak)", "Deteksi otomatis bagian paling energik dari lagu (hook atau chorus) lalu ekstrak. Menggunakan Separate untuk menghasilkan stem vokal dan instrumental yang bersih."),
        "JP": ("Extract (抽出)", "曲の最も盛り上がる部分（フックまたはサビ）を自動検出して抽出。Separateを使用してクリーンなステムを出力。"),
    },
    {
        "EN": ("Mix", "Auto-ducking: lowers background music when voice is detected, raises it back during silence. Features smooth attack and release for natural-sounding transitions. Ideal for podcasts, voiceovers, and live streaming."),
        "ID": ("Mix (Campur)", "Auto-ducking: musik latar otomatis mengecil saat ada suara vokal, kembali normal saat hening. Dilengkapi transisi halus (attack/release) untuk hasil natural. Cocok untuk podcast, voiceover, dan live streaming."),
        "JP": ("Mix (ミックス)", "オートダッキング：ボーカル検出時にBGMを下げ、無音時に戻す。スムーズなアタック/リリースで自然なトランジション。ポッドキャストや配信に最適。"),
    },
    {
        "EN": ("Optimize", "Normalize audio to broadcast-standard LUFS loudness (default -14 LUFS). Ensures consistent volume levels across platforms like YouTube, Spotify, radio, and podcast directories."),
        "ID": ("Optimize (Optimalkan)", "Normalisasi loudness ke standar broadcast (-14 LUFS default). Volume konsisten di YouTube, Spotify, radio, dan direktori podcast."),
        "JP": ("Optimize (最適化)", "放送規格のLUFSラウドネス（デフォルト-14 LUFS）に正規化。YouTube、Spotify、ラジオで一貫した音量を実現。"),
    },
    {
        "EN": ("Enhance", "Reduce background noise (hiss, hum, ambient room tone) with adaptive filtering. Boost voice clarity using compressor and EQ. One-click cleanup for vocal recordings and field audio."),
        "ID": ("Enhance (Perbaiki)", "Kurangi noise latar (desis, dengung, suara ruangan) dengan filter adaptif. Tingkatkan kejelasan vokal dengan kompresor dan EQ. Pembersihan instan untuk rekaman vokal."),
        "JP": ("Enhance (強化)", "適応フィルターでノイズ（ヒス、ハム、環境音）を低減。コンプレッサーとEQで声を明瞭化。ボーカル録音のワンクリック補正。"),
    },
    {
        "EN": ("Trim", "Automatically detect and remove silence and dead air from recordings. Aggressive mode removes shorter pauses for tighter pacing. Perfect for cleaning up podcasts, voice messages, and interviews."),
        "ID": ("Trim (Potong)", "Deteksi dan hapus hening dan jeda mati dari rekaman secara otomatis. Mode agresif untuk jeda pendek. Cocok untuk merapikan podcast, pesan suara, dan wawancara."),
        "JP": ("Trim (トリム)", "録音から無音部分を自動検出して削除。アグレッシブモードで短い間隔も除去。ポッドキャストやボイスメッセージの整形に最適。"),
    },
    {
        "EN": ("Vibe", "Apply social media audio effects: Slowed (chill, dark atmosphere without reverb), Slowed+Reverb (ethereal with echo ambience), or Nightcore (energetic, pitched up). Ready for TikTok, Reels, and Shorts."),
        "ID": ("Vibe (Suasana)", "Efek audio tren media sosial: Slowed (suasana chill/gelap tanpa reverb), Slowed+Reverb (ethereal dengan gema), atau Nightcore (energik, nada tinggi). Siap untuk TikTok, Reels, dan Shorts."),
        "JP": ("Vibe (雰囲気)", "SNS向けオーディオエフェクト：Slowed（落ち着いた雰囲気、リバーブなし）、Slowed+Reverb（幻想的なエコー）、Nightcore（元気な雰囲気）。TikTok、Reels、Shorts対応。"),
    },
]

tips = {
    "EN": "Tips\n- Upload any audio file (.mp3, .wav, .ogg, .m4a, .flac)\n- Processed files appear in the right column -- click to download\n- All processing runs locally on your device -- nothing leaves your computer",
    "ID": "Tips\n- Upload file audio (.mp3, .wav, .ogg, .m4a, .flac)\n- File hasil muncul di kolom kanan -- klik untuk download\n- Semua proses berjalan lokal di perangkat Anda -- tidak ada yang diunggah ke cloud",
    "JP": "Tips\n- オーディオファイル(.mp3, .wav, .ogg, .m4a, .flac)をアップロード\n- 処理結果は右側に表示 -- クリックしてダウンロード\n- すべての処理はローカルデバイス上で実行 -- クラウドに送信されません",
}

author_text = {
    "EN": "Museic is created by Arhylsion (https://github.com/arhylsion)",
    "ID": "Museic dibuat oleh Arhylsion (https://github.com/arhylsion)",
    "JP": "Museic is created by Arhylsion (https://github.com/arhylsion)",
}

total_pages = len(guide_pages)


def render_page(lang, page):
    page = max(1, min(page, total_pages))
    entry = guide_pages[page - 1]
    title, desc = entry[lang]
    return f"### Page {page} / {total_pages}\n\n**{title}**\n\n{desc}"


def render_tips(lang):
    return f"### {tips[lang]}\n\n---\n### Author\n{author_text[lang]}"


with gr.Blocks(title="Museic") as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("# Museic Audio Engineering Toolkit")
        with gr.Column(scale=0, min_width=80):
            guide_btn = gr.Button("Guide", size="sm", variant="secondary")

    gr.Markdown("Upload audio, adjust parameters, and process -- all locally on your device.")

    guide_panel = gr.Column(visible=False)
    with guide_panel:
        gr.Markdown("## Guide / Panduan / ガイド")
        with gr.Row():
            guide_lang = gr.Radio(label="Language / Bahasa / 言語", choices=["EN", "ID", "JP"], value="EN", scale=0)
            guide_page = gr.Number(label="Page", value=1, minimum=1, maximum=total_pages, step=1, scale=0)
        guide_content = gr.Markdown(render_page("EN", 1))
        guide_tips = gr.Markdown(render_tips("EN"))
        with gr.Row():
            guide_prev = gr.Button("Previous", size="sm", scale=0)
            guide_next = gr.Button("Next", size="sm", scale=0)
            guide_close = gr.Button("Close", size="sm", variant="secondary", scale=0)

    guide_visible = gr.State(False)

    def toggle_guide(visible):
        return gr.update(visible=not visible), not visible

    def close_guide():
        return gr.update(visible=False), False

    guide_btn.click(toggle_guide, inputs=guide_visible, outputs=[guide_panel, guide_visible])
    guide_close.click(close_guide, outputs=[guide_panel, guide_visible])

    def update_guide(lang, page):
        return render_page(lang, page)

    def change_page(lang, page, delta):
        new_page = max(1, min(page + delta, total_pages))
        return new_page, render_page(lang, new_page)

    guide_lang.change(update_guide, inputs=[guide_lang, guide_page], outputs=guide_content)
    guide_page.change(update_guide, inputs=[guide_lang, guide_page], outputs=guide_content)
    guide_lang.change(lambda l: render_tips(l), inputs=guide_lang, outputs=guide_tips)
    guide_prev.click(change_page, inputs=[guide_lang, guide_page, gr.State(-1)], outputs=[guide_page, guide_content])
    guide_next.click(change_page, inputs=[guide_lang, guide_page, gr.State(1)], outputs=[guide_page, guide_content])

    gr.Markdown("---")

    with gr.Tabs():
        with gr.Tab("Extend"):
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

        with gr.Tab("Separate"):
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

        with gr.Tab("Extract"):
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

        with gr.Tab("Mix"):
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

        with gr.Tab("Optimize"):
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

        with gr.Tab("Enhance"):
            with gr.Row():
                with gr.Column():
                    enhance_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                    enhance_denoise = gr.Checkbox(label="Denoise (reduce background hiss/hum)", value=True)
                    enhance_boost = gr.Checkbox(label="Boost voice (compressor + EQ)", value=False)
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

        with gr.Tab("Trim"):
            with gr.Row():
                with gr.Column():
                    trim_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                    trim_aggressive = gr.Checkbox(label="Aggressive mode (remove shorter pauses)", value=False)
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

        with gr.Tab("Vibe"):
            with gr.Row():
                with gr.Column():
                    vibe_input = gr.File(label="Audio File", file_types=[".mp3", ".wav", ".ogg", ".m4a", ".flac"])
                    vibe_mode = gr.Radio(label="Effect", choices=["Slowed", "Slowed + Reverb", "Nightcore"], value="Slowed")
                    vibe_btn = gr.Button("Apply Effect", variant="primary")
                with gr.Column():
                    vibe_log = gr.Textbox(label="Log", lines=10)
                    vibe_output = gr.File(label="Download Modified Audio", file_count="single")

            def process_vibe_fn(file, mode):
                path, err = save_file(file)
                if err:
                    return err, None
                result, log, err = run_capture(process_vibe, input_path=path, slowed=(mode=="Slowed"), slowed_reverb=(mode=="Slowed + Reverb"), nightcore=(mode=="Nightcore"))
                if err:
                    return f"{log}\nError: {err}", None
                return log, result if result else None
            vibe_btn.click(process_vibe_fn, inputs=[vibe_input, vibe_mode], outputs=[vibe_log, vibe_output])

    gr.Markdown("All processing runs locally. Your audio never leaves your device.")


def main():
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())


if __name__ == "__main__":
    main()
