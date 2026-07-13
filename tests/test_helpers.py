import os
import tempfile
import shutil
from museic.ui.helpers import save_file, collect_output_files, stream_capture


class FakeUploadFile:
    """Mimics a Gradio uploaded file object."""
    def __init__(self, path):
        self.name = path


class TestSaveFile:
    def test_no_file(self):
        result, msg = save_file(None)
        assert result is None
        assert msg == "No file provided"

    def test_with_real_file(self):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(b'fake audio content')
            path = f.name
        try:
            fake_file = FakeUploadFile(path)
            result, msg = save_file(fake_file)
            assert msg is None
            assert os.path.exists(result)
            assert result.endswith('.wav')
        finally:
            os.unlink(path)
            if result and os.path.exists(result):
                os.unlink(result)


class TestCollectOutputFiles:
    def test_nonexistent(self):
        assert collect_output_files("/nonexistent/path") is None

    def test_single_file(self):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            path = f.name
        try:
            result = collect_output_files(path)
            assert result == path
        finally:
            os.unlink(path)

    def test_directory(self):
        tmpdir = tempfile.mkdtemp()
        try:
            f1 = os.path.join(tmpdir, "a.wav")
            f2 = os.path.join(tmpdir, "b.wav")
            open(f1, 'w').close()
            open(f2, 'w').close()
            result = collect_output_files(tmpdir)
            assert isinstance(result, list)
            assert len(result) == 2
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


class TestStreamCapture:
    def test_basic_function(self):
        def my_func():
            print("hello")
            return "result"

        outputs = list(stream_capture(my_func))
        assert len(outputs) >= 1
        final_log, result, error = outputs[-1]
        assert result == "result"
        assert error is None
        assert "hello" in final_log

    def test_error_handling(self):
        def failing_func():
            print("before error")
            raise RuntimeError("something bad")

        outputs = list(stream_capture(failing_func))
        final_log, result, error = outputs[-1]
        assert result is None
        assert error == "something bad"
        assert "before error" in final_log

    def test_no_output(self):
        def noop():
            return 42

        outputs = list(stream_capture(noop))
        final_log, result, error = outputs[-1]
        assert result == 42
        assert error is None
