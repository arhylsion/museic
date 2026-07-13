import gradio as gr

from museic.ui.constants import TOOLS
from museic.ui.helpers import save_file, collect_output_files
from museic.ui.guide import render_page, render_tips, total_pages
from museic.ui.panels import (
    build_extend_panel,
    build_separate_panel,
    build_extract_panel,
    build_mix_panel,
    build_optimize_panel,
    build_enhance_panel,
    build_trim_panel,
    build_vibe_panel,
    build_guide_panel,
)

CSS = """
.sidebar-col, .sidebar-col .block { width: 100% !important; }
.sidebar-radio, .sidebar-radio .wrap { width: 100%; }
.sidebar-radio label { width: 100%; min-height: 38px; display: flex; align-items: center; }
.sidebar-divider { margin: 4px 0; }
.sidebar-guide-btn { width: 100%; min-height: 38px; border: none !important; box-shadow: none !important; justify-content: flex-start; padding: 0 12px; font-weight: 400; font-size: 14px; background: transparent !important; cursor: pointer; }
.sidebar-guide-btn:hover { background: rgba(128,128,128,0.1) !important; }
.lang-select .wrap { border: none !important; box-shadow: none !important; background: transparent !important; gap: 0 !important; padding: 0 !important; }
.lang-select label { border: none !important; box-shadow: none !important; padding: 2px 8px !important; margin: 0 !important; background: transparent !important; font-size: 13px; font-weight: 500; text-transform: lowercase; }
.lang-select input:checked + span { font-weight: 700; text-decoration: underline; }
.lang-select input[type="radio"] { position: absolute !important; opacity: 0 !important; width: 0 !important; height: 0 !important; }
.guide-content { min-height: 280px; }
@media (max-width: 768px) {
  .sidebar-col { min-width: 100% !important; max-width: 100% !important; }
  .sidebar-radio, .sidebar-radio .wrap { width: 100% !important; }
  .sidebar-radio label { flex: 1 1 auto; }
  .sidebar-guide-btn { width: 100% !important; }
}
"""

with gr.Blocks(title="Museic") as demo:
    gr.Markdown("## Museic Audio Engineering Toolkit")
    gr.Markdown("Upload audio, adjust parameters, and process all locally on your device.")

    with gr.Row(equal_height=True):
        with gr.Column(scale=0, min_width=150, elem_classes="sidebar-col"):
            tool_radio = gr.Radio(
                choices=TOOLS, value="Extend",
                label="", show_label=False,
                elem_classes="sidebar-radio",
            )
            gr.Markdown("---", elem_classes="sidebar-divider")
            guide_btn = gr.Button("Guide", elem_classes="sidebar-guide-btn", variant="secondary")

        with gr.Column(scale=1):
            extend_panel = build_extend_panel()
            separate_panel = build_separate_panel()
            extract_panel = build_extract_panel()
            mix_panel = build_mix_panel()
            optimize_panel = build_optimize_panel()
            enhance_panel = build_enhance_panel()
            trim_panel = build_trim_panel()
            vibe_panel = build_vibe_panel()
            guide_panel, guide_lang, guide_content, guide_tips, guide_page_disp, guide_prev, guide_next = build_guide_panel()

    gr.Markdown("---")
    gr.Markdown("Museic by Arhylsion (https://github.com/arhylsion/museic)")
    gr.Markdown("All processing runs locally. Your audio never leaves your device.")

    panels = [extend_panel, separate_panel, extract_panel, mix_panel, optimize_panel, enhance_panel, trim_panel, vibe_panel, guide_panel]

    def switch_tab(tool):
        return tuple([gr.update(visible=(t == tool)) for t in TOOLS] + [gr.update(visible=False)])

    def show_guide():
        return tuple([gr.update(visible=False)] * 8 + [gr.update(visible=True)])

    tool_radio.change(switch_tab, inputs=tool_radio, outputs=panels)
    guide_btn.click(show_guide, outputs=panels)

    guide_page = gr.State(1)

    def update_guide(lang, page):
        return render_page(lang, page)

    def update_tips(lang):
        return render_tips(lang)

    def change_page(lang, page, delta):
        new_page = max(1, min(page + delta, total_pages))
        return new_page, f"**{new_page}/{total_pages}**", render_page(lang, new_page)

    guide_lang.change(update_guide, inputs=[guide_lang, guide_page], outputs=guide_content)
    guide_lang.change(update_tips, inputs=guide_lang, outputs=guide_tips)
    guide_page.change(update_guide, inputs=[guide_lang, guide_page], outputs=guide_content)
    guide_prev.click(change_page, inputs=[guide_lang, guide_page, gr.State(-1)], outputs=[guide_page, guide_page_disp, guide_content])
    guide_next.click(change_page, inputs=[guide_lang, guide_page, gr.State(1)], outputs=[guide_page, guide_page_disp, guide_content])


def main():
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft(), head=f"<style>{CSS}</style>")


if __name__ == "__main__":
    main()
