# Museic

Museic is a Flask-based web application designed for advanced audio processing and manipulation. It provides a modern, single-page dashboard interface for separating audio stems (vocals, instruments) and extending audio tracks seamlessly.

## Features

Current Features:
* **Splitter Music:** Utilizes Hybrid Transformer Demucs (`htdemucs`) to separate an audio file into four isolated stems: Vocals, Bass, Drums, and Other. It automatically generates a combined instrumental track.
* **Extender Music:** Allows users to extend an audio track by specifying a start and end point, looping the segment a specified number of times with smooth crossfading using `pydub`.

Planned Features:
* **AI Transcript:** Automated lyrics generation and transcription using OpenAI's Whisper model.
* **Song Identification:** Audio fingerprinting and recognition using the Shazam API.

## Quick Start & Installation

Ensure you have Python 3.8+ installed. Run the following commands sequentially in your terminal to set up and run the application:

```bash
# 1. Install FFmpeg (Choose the command based on your OS)
# Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg -y
# macOS: brew install ffmpeg
# Windows (via choco): choco install ffmpeg

# 2. Clone the repository
git clone [https://github.com/yourusername/museic.git](https://github.com/yourusername/museic.git)
cd museic

# 3. Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
python app.py

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. **Important Note on First Run:** The first time you use the Splitter feature, Demucs will automatically download the pre-trained `htdemucs` model weights. This may take several minutes depending on your internet connection.

## Project Structure

```text
MUSEIC/
├── modules/
│   ├── extender/
│   │   ├── extender_utils.py
│   │   └── segment_detector.py
│   └── splitter/
│       ├── demucs_handler.py
│       └── utils.py
├── output/               # Generated audio files are saved here
├── static/               # CSS, JS, and image assets
├── templates/
│   └── index.html        # Main dashboard UI (Tailwind CSS)
├── uploads/              # Temporary storage for uploaded files
├── .gitignore
├── app.py                # Main Flask application and routing
├── README.md
└── requirements.txt      # Project dependencies

```

## Configuration & Troubleshooting

* **Storage Cleanup:** The `uploads/` and `output/` directories are created automatically. It is highly recommended to implement a cron job to periodically clean these folders in a production environment to save disk space.
* **FFmpeg Error:** `FileNotFoundError: [WinError 2]` indicates that FFmpeg is not installed or not added to your system's PATH variable.
* **Timeout Issues:** Demucs processing is CPU-intensive. On slower machines, the browser might time out waiting for the Flask response.

```

```