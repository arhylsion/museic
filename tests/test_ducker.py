import os
import pytest
from museic.core.ducker import process_ducking


class TestProcessDucking:
    def test_basic_ducking(self, two_test_audios, output_dir):
        voice_path, bgm_path = two_test_audios
        result = process_ducking(voice_path, bgm_path, output_dir=output_dir)
        assert os.path.exists(result)

    def test_custom_db(self, two_test_audios, output_dir):
        voice_path, bgm_path = two_test_audios
        result = process_ducking(voice_path, bgm_path, ducking_db=-10, threshold_db=-30, output_dir=output_dir)
        assert os.path.exists(result)

    def test_bad_voice(self, test_audio_path, output_dir):
        with pytest.raises(Exception):
            process_ducking("/nonexistent/file.wav", test_audio_path, output_dir=output_dir)
