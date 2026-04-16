# Museic

A lightweight, cross-platform Command Line Interface utility for advanced audio manipulation. Museic operates at the native system level to execute nine professional audio engineering tasks. Designed with a strict focus on extreme processing speed, seamless transitions, and minimum storage overhead, it guarantees execution within seconds while keeping RAM usage strictly under 100MB.

## Key Features

* **Pure Headless Architecture:** Zero UI overhead guarantees maximum RAM efficiency and raw execution speed.
* **9-in-1 Audio Engine:** Includes modules for separation, seamless looping, vocal extraction, auto-ducking, LUFS optimization, directory watching, noise reduction, silence trimming, and tempo manipulation.
* **Dynamic Plugin Ecosystem:** Extend core capabilities by dropping Python scripts into the plugins directory. Museic automatically registers new commands without altering core code.
* **Ultra-Fast Seamless Looping:** Utilizes Edge Beat-Matching to seamlessly loop tracks without relying on heavy DSP analysis.
* **Targeted Slicing & Extraction:** Processes only specific user-defined timestamps using quantized models (mdx_extra_q). 
* **Broadcast Standard Optimization:** Built-in FFmpeg dynamic range compression and LUFS normalization for broadcast-ready audio.

## System Prerequisites

* Python 3.9 or newer
* FFmpeg (Must be registered in the system PATH)
* Git

## Installation

Execute the following commands to install dependencies and register Museic as a global system command.

```bash
git clone [https://github.com/arhylsion/museic.git](https://github.com/arhylsion/museic.git)
cd museic
python -m venv venv

source venv/bin/activate

pip install -e .
```

## Usage

Museic operates entirely via direct command-line arguments. Run `museic --help` at any time to view the full command list.

### 1. Extend (Seamless Looping)
Automatically detect loop points at the edges of the track and loop it multiple times seamlessly.
```bash
museic extend -i track.mp3 --auto -r 4
```

### 2. Separate (Stem Isolation)
Isolate vocals and instrumental stems for a targeted slice to save memory and time.
```bash
museic separate -i track.mp3 -s 0 -e 30 --export mp3
```

### 3. Extract (Smart Hook Detection)
Automatically locate the most energetic part of a song (the chorus) and extract it.
```bash
museic extract -i track.mp3 --length 30 --export wav
```

### 4. Mix (Auto-Ducker)
Automatically lower background music volume when vocals cross a specific decibel threshold.
```bash
museic mix -v voiceover.wav -b background.mp3
```

### 5. Optimize (Broadcast Leveling)
Normalize audio to standard broadcast loudness (-14.0 LUFS) for streaming platforms.
```bash
museic optimize -i podcast.wav --lufs -14.0
```

### 6. Enhance (Noise Reduction & EQ Boost)
Remove static hiss or boost treble and bass dynamics using acoustic filters.
```bash
museic enhance -i raw_mic.wav --denoise --boost
```

### 7. Trim (Silence Killer)
Automatically detect and remove dead air or long pauses from voice recordings.
```bash
museic trim -i raw_podcast.wav --aggressive
```

### 8. Vibe (Social Media Trends)
Apply dynamic tempo and spatial filters to create specific audio aesthetics.
```bash
museic vibe -i song.mp3 --slowed
```

### 9. Watch (Daemon Mode)
Monitor a specific directory and automatically execute extraction processes when a new audio file is detected.
```bash
museic watch -d ./raw_audio_folder
```

## Plugin Development

Museic supports community-driven extensions. To add a custom command, create a Python file in the `museic/plugins/` directory containing a `register_plugin()` and `execute(args)` function. Museic will automatically parse and add your command to the CLI.