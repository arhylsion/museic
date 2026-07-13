import os
import pytest
from museic.core.trimmer import process_trimming


class TestProcessTrimming:
    def test_basic(self, test_audio_path, output_dir):
        result = process_trimming(test_audio_path, output_dir=output_dir)
        assert os.path.exists(result)

    def test_aggressive(self, test_audio_path, output_dir):
        result = process_trimming(test_audio_path, aggressive=True, output_dir=output_dir)
        assert os.path.exists(result)

    def test_bad_input(self, output_dir):
        with pytest.raises(Exception):
            process_trimming("/nonexistent/file.wav", output_dir=output_dir)
