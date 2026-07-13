import os
import pytest
from museic.core.enhancer import process_enhancement


class TestProcessEnhancement:
    def test_denoise(self, test_audio_path, output_dir):
        result = process_enhancement(test_audio_path, denoise=True, output_dir=output_dir)
        assert os.path.exists(result)

    def test_boost(self, test_audio_path, output_dir):
        result = process_enhancement(test_audio_path, boost=True, output_dir=output_dir)
        assert os.path.exists(result)

    def test_both(self, test_audio_path, output_dir):
        result = process_enhancement(test_audio_path, denoise=True, boost=True, output_dir=output_dir)
        assert os.path.exists(result)

    def test_no_flags_raises_error(self, test_audio_path, output_dir):
        with pytest.raises(ValueError, match="No enhancement flags"):
            process_enhancement(test_audio_path, output_dir=output_dir)

    def test_bad_input(self, output_dir):
        with pytest.raises(Exception):
            process_enhancement("/nonexistent/file.wav", denoise=True, output_dir=output_dir)
