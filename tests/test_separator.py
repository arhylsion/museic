import os
import pytest
from museic.core.separator import process_separation, _sanitize_name


class TestSanitizeName:
    def test_preserves_spaces(self):
        assert _sanitize_name("hello world") == "hello world"

    def test_replaces_special_chars(self):
        assert _sanitize_name("a/b:c*d?e") == "a_b_c_d_e"

    def test_empty(self):
        assert _sanitize_name("") == ""


class TestProcessSeparation:
    @pytest.mark.slow
    def test_separation(self, test_audio_path, output_dir):
        result = process_separation(test_audio_path, output_dir=output_dir)
        assert os.path.exists(result)

    def test_bad_input(self, output_dir):
        with pytest.raises(Exception):
            process_separation("/nonexistent/file.wav", output_dir=output_dir)
