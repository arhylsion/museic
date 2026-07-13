import os
import wave
import struct
import math
import tempfile
import shutil
import pytest


@pytest.fixture
def output_dir():
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def test_audio_path():
    """Generate a 2-second test WAV file using stdlib (no ffmpeg needed)."""
    sample_rate = 44100
    duration = 2.0
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Mix of 440Hz and 880Hz sine waves with a fade in/out
        val = 0.3 * math.sin(2 * math.pi * 440 * t) + 0.2 * math.sin(2 * math.pi * 880 * t)
        # Apply fade
        fade_len = int(sample_rate * 0.1)
        if i < fade_len:
            val *= i / fade_len
        if i > num_samples - fade_len - 1:
            val *= (num_samples - 1 - i) / fade_len
        samples.append(int(val * 32767 * 0.5))

    path = tempfile.mktemp(suffix='.wav')
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    yield path
    os.unlink(path)


@pytest.fixture
def test_audio_path_stereo(test_audio_path):
    """Convert mono test file to stereo by creating a stereo WAV."""
    import wave
    import struct

    with wave.open(test_audio_path, 'r') as wf:
        frames = wf.readframes(wf.getnframes())
        sample_rate = wf.getframerate()
        n = wf.getnframes()

    path = tempfile.mktemp(suffix='_stereo.wav')
    with wave.open(path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        stereo_frames = b''
        for i in range(0, len(frames), 2):
            stereo_frames += frames[i:i+2] + frames[i:i+2]
        wf.writeframes(stereo_frames)
    yield path
    os.unlink(path)


@pytest.fixture
def two_test_audios(test_audio_path):
    """Return two distinct audio paths for ducking tests."""
    sample_rate = 44100
    duration = 1.0
    num_samples = int(sample_rate * duration)

    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        val = 0.3 * math.sin(2 * math.pi * 220 * t)
        samples.append(int(val * 32767 * 0.5))

    path2 = tempfile.mktemp(suffix='_voice.wav')
    with wave.open(path2, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f'<{len(samples)}h', *samples))
    yield (test_audio_path, path2)
    os.unlink(path2)
