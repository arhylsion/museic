import os
import pytest
from museic.core.extractor import find_the_hook, process_extraction


class TestFindTheHook:
    def test_returns_floats(self, test_audio_path):
        start, end = find_the_hook(test_audio_path)
        assert isinstance(start, float)
        assert isinstance(end, float)
        assert start >= 0
        assert end >= start

    def test_custom_duration(self, test_audio_path):
        start, end = find_the_hook(test_audio_path, duration_sec=5)
        assert end - start <= 5.1


class TestProcessExtraction:
    @pytest.mark.slow
    def test_extraction(self, test_audio_path, output_dir):
        result = process_extraction(test_audio_path, output_dir=output_dir)
        assert os.path.exists(result)

    def test_bad_input(self, output_dir):
        with pytest.raises(Exception):
            process_extraction("/nonexistent/file.wav", output_dir=output_dir)
