# Museic

A lightweight, cross-platform Command Line Interface (CLI) and Terminal User Interface (TUI) utility for advanced audio manipulation. Museic is designed to operate at the native system level to separate instruments (vocals, bass, drums) and intelligently extend audio tracks, with a strong focus on processing speed and storage efficiency.

## Key Features

* **Native CLI Wrapper:** Access Museic globally from any terminal using the `museic` command, eliminating the need to invoke Python manually.
* **Targeted Audio Slicing:** Specify exact timestamps (start/end) to process only specific segments. This drastically saves RAM and accelerates processing time.
* **Auto-Compression Pipeline:** Automatically converts Demucs output (32-bit WAV) into lightweight MP3 or OGG formats (2-5 MB).
* **Nuclear Cleanup & Repair:** Integrated FFmpeg processes repair corrupted audio files prior to processing, while an automated cleanup system removes large cache files post-execution.
* **Cross-Platform Ready:** Runs seamlessly on Windows, native Linux, and Windows Subsystem for Linux (WSL).

## System Prerequisites

* Python 3.9 or newer
* FFmpeg (Must be registered in the system PATH)

## Installation (Development Mode)

Use the following commands to install dependencies and register Museic as a global system command.

```bash
git clone https://github.com/username/museic-tui.git
cd museic-tui
python -m venv venv

# Activate Virtual Environment
# Linux/WSL: source venv/bin/activate
# Windows: venv\Scripts\activate

# Install and register the CLI wrapper
pip install -e .
```

## Usage

Museic can be utilized via direct command-line arguments or through the interactive terminal interface.

**Interactive Mode (TUI):**
```bash
museic tui
```

**Direct Command Line Mode (CLI):**

1. Automatic Audio Extension
```bash
museic extend --file song.mp3 --auto
```

2. Manual Audio Extension (Specific timestamps)
```bash
museic extend --file song.mp3 --start 30 --end 60
```

3. Fast Vocal & Instrument Separation (Targeted Slicing)
```bash
museic separate --file song.mp3 --start 60 --end 120 --export mp3
```
