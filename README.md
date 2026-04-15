# Museic

A lightweight, cross-platform Command Line Interface utility for advanced audio manipulation. Museic is designed to operate at the native system level to separate instruments and intelligently extend audio tracks, with a strict focus on extreme processing speed, seamless transitions, and minimum storage and memory overhead.

## Key Features

* **Pure Headless Architecture:** Zero UI overhead guarantees maximum RAM efficiency and raw execution speed. 
* **Ultra-Fast Seamless Looping:** Utilizes Edge Beat-Matching to seamlessly loop tracks without relying on heavy DSP analysis, keeping processing times under 30 seconds.
* **Targeted Slicing & Separation:** Processes only specific user-defined timestamps using quantized models (mdx_extra_q). This ensures memory usage remains strictly under the 100MB RAM threshold.
* **Auto-Compression Pipeline:** Automatically converts Demucs output (32-bit WAV) into lightweight MP3 or OGG formats.
* **Nuclear Cleanup & Repair:** Integrated FFmpeg processes repair corrupted audio files prior to processing, while an aggressive garbage collection system removes temp files post-execution.
* **Cross-Platform Ready:** Runs efficiently on Windows, native Linux, and Windows Subsystem for Linux (WSL).

## System Prerequisites

* Python 3.9 or newer
* FFmpeg (Must be registered in the system PATH)
* Git

## Installation

Execute the following commands to install dependencies and register Museic as a global system command.

```bash
git clone https://github.com/arhylsion/museic.git
cd museic
python -m venv venv

source venv/bin/activate

pip install -e .
```

## Usage

Museic operates entirely via direct command-line arguments.

### 1. Audio Extension (Seamless Looping)

Automatically detect loop points at the edges of the track and loop it multiple times seamlessly.

```bash
museic extend -i track.mp3 --auto -r 4
```

Manually extend using specific start and end timestamps.

```bash
museic extend -i track.mp3 -s 30.5 -e 60.0 -r 2
```

### 2. Stem Separation (Vocals & Instruments)

Isolate vocals and instrumental stems for a targeted slice to save memory and time.

```bash
museic separate -i track.mp3 -s 0 -e 30 --export mp3
```

Process the entire track (requires more processing time) and export to an alternative format.

```bash
museic separate -i track.mp3 -s 0 -e 180 --export ogg
```
