# museic/tui.py
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label, Log
from textual.containers import Vertical, Horizontal
from textual import work

from museic.core.extender import process_extension
from museic.core.separator import process_separation
from museic.utils.helpers import get_wsl_path

class MuseicApp(App):
    # CSS Styling untuk terminal
    CSS = """
    Screen { align: center middle; }
    #main_container { width: 80; height: auto; border: solid green; padding: 1 2; }
    .row { height: auto; margin-bottom: 1; }
    .btn { margin-right: 1; }
    #log_window { height: 12; border: solid gray; margin-top: 1;}
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main_container"):
            yield Label("Museic TUI - Lightweight Audio Manipulation", classes="row")
            yield Input(placeholder="Audio File Path (C:\\music.mp3 or /mnt/c/...)", id="file_path", classes="row")
            
            with Horizontal(classes="row"):
                yield Input(placeholder="Start (sec) e.g., 0", id="start_sec", type="number")
                yield Input(placeholder="End (sec) e.g., 10", id="end_sec", type="number")
            
            with Horizontal(classes="row"):
                yield Button("Auto-Extend", id="btn_extend", variant="success", classes="btn")
                yield Button("Separate Stems", id="btn_separate", variant="warning", classes="btn")
                yield Button("Exit", id="btn_exit", variant="error", classes="btn")
            
            # Log terminal mini di dalam UI
            yield Log(id="log_window")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_exit":
            self.exit()
            return

        raw_path = self.query_one("#file_path", Input).value
        start_val = self.query_one("#start_sec", Input).value
        end_val = self.query_one("#end_sec", Input).value
        logger = self.query_one("#log_window", Log)

        if not raw_path:
            logger.write_line("[!] ERROR: Please input an audio file path.")
            return

        # Handle Windows path to WSL conversion safely
        path = get_wsl_path(raw_path)
        
        # Default target slice is 10 seconds to keep RAM < 100MB
        start_sec = float(start_val) if start_val else 0.0
        end_sec = float(end_val) if end_val else 10.0

        if event.button.id == "btn_extend":
            logger.write_line(f"[*] Running Auto-Extend for: {os.path.basename(path)}")
            self.run_extend(path, start_sec, end_sec)
        
        elif event.button.id == "btn_separate":
            logger.write_line(f"[*] Running Separation (Slice {start_sec}s - {end_sec}s) for: {os.path.basename(path)}")
            logger.write_line("[*] Processing in background, please wait...")
            self.run_separate(path, start_sec, end_sec)

    # Menjalankan proses di thread terpisah agar UI tidak freeze
    @work(thread=True)
    def run_extend(self, path, start, end):
        logger = self.query_one("#log_window", Log)
        try:
            out = process_extension(path, start_sec=start, end_sec=end, auto=True)
            self.call_from_thread(logger.write_line, f"[+] SUCCESS: Saved to {out}")
        except Exception as e:
            self.call_from_thread(logger.write_line, f"[!] FAILED: {e}")

    @work(thread=True)
    def run_separate(self, path, start, end):
        logger = self.query_one("#log_window", Log)
        try:
            process_separation(path, start_sec=start, end_sec=end, target_format="mp3")
            self.call_from_thread(logger.write_line, f"[+] SUCCESS: Stems separated securely.")
        except Exception as e:
            self.call_from_thread(logger.write_line, f"[!] FAILED: {e}")

def run_tui():
    app = MuseicApp()
    app.run()