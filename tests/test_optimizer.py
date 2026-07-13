import os
import pytest
from museic.core.optimizer import process_optimization


class TestProcessOptimization:
    def test_basic(self, test_audio_path, output_dir):
        result = process_optimization(test_audio_path, output_dir=output_dir)
        assert os.path.exists(result)

    def test_target_loudness(self, test_audio_path, output_dir):
        result = process_optimization(test_audio_path, target_lufs=-16.0, output_dir=output_dir)
        assert os.path.exists(result)

    def test_bad_input(self, output_dir):
        with pytest.raises(Exception):
            process_optimization("/nonexistent/file.wav", output_dir=output_dir)
