import os
import pytest
from museic.core.vibe import process_vibe


class TestProcessVibe:
    def test_slowed(self, test_audio_path, output_dir):
        result = process_vibe(test_audio_path, slowed=True, output_dir=output_dir)
        assert os.path.exists(result)

    def test_nightcore(self, test_audio_path, output_dir):
        result = process_vibe(test_audio_path, nightcore=True, output_dir=output_dir)
        assert os.path.exists(result)

    def test_slowed_reverb(self, test_audio_path, output_dir):
        result = process_vibe(test_audio_path, slowed_reverb=True, output_dir=output_dir)
        assert os.path.exists(result)

    def test_no_mode(self, test_audio_path, output_dir):
        with pytest.raises(Exception):
            process_vibe(test_audio_path, output_dir=output_dir)

    def test_bad_input(self, output_dir):
        with pytest.raises(Exception):
            process_vibe("/nonexistent/file.wav", slowed=True, output_dir=output_dir)
