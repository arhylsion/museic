import os
from museic.ui.constants import TOOLS, INPUT_DIR, OUTPUT_DIR


class TestTools:
    def test_tools_list_structure(self):
        assert isinstance(TOOLS, list)
        assert len(TOOLS) == 8

    def test_all_tools_are_strings(self):
        for tool in TOOLS:
            assert isinstance(tool, str)

    def test_all_ids_unique(self):
        assert len(TOOLS) == len(set(TOOLS)), "duplicate tool names found"

    def test_expected_tools_present(self):
        expected = {"Extend", "Separate", "Extract", "Mix",
                    "Optimize", "Enhance", "Trim", "Vibe"}
        assert set(TOOLS) == expected


class TestPaths:
    def test_input_dir_is_string(self):
        assert isinstance(INPUT_DIR, str)

    def test_output_dir_is_string(self):
        assert isinstance(OUTPUT_DIR, str)

    def test_directories_exist(self):
        assert os.path.exists(INPUT_DIR)
        assert os.path.exists(OUTPUT_DIR)
