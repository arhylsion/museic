import os
import pytest
from museic.core.extender import process_extension, find_loop_points


class TestProcessExtension:
    def test_basic_extension(self, test_audio_path, output_dir):
        result = process_extension(test_audio_path, output_dir=output_dir)
        assert os.path.exists(result)

    def test_with_repeat(self, test_audio_path, output_dir):
        result = process_extension(test_audio_path, repeat=3, output_dir=output_dir)
        assert os.path.exists(result)

    def test_custom_start_end(self, test_audio_path, output_dir):
        result = process_extension(test_audio_path, start_sec=0.5, end_sec=1.0, output_dir=output_dir)
        assert os.path.exists(result)

    def test_bad_input(self, output_dir):
        with pytest.raises(Exception):
            process_extension("/nonexistent/file.wav", output_dir=output_dir)


class TestFindLoopPoints:
    def test_returns_floats(self, test_audio_path):
        first, last = find_loop_points(test_audio_path)
        assert isinstance(first, (int, float))
        assert isinstance(last, (int, float))
        assert first >= 0
        assert last >= first
