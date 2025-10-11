import librosa
import numpy as np

def detect_segments(audio_path):
    y, sr = librosa.load(audio_path, mono=True)
    
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    sim_matrix = np.dot(chroma.T, chroma)

    sim_sums = np.sum(sim_matrix, axis=1)
    peak_idx = np.argmax(sim_sums)

    start_sec = max(0, beat_times[peak_idx] - 10)  
    end_sec = min(beat_times[-1], beat_times[peak_idx] + 20)

    return {
        "tempo": tempo,
        "beats_ms": [int(t * 1000) for t in beat_times],
        "suggested_segment": (round(start_sec, 2), round(end_sec, 2))
    }
