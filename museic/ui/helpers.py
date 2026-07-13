import os
import io
import sys
import shutil
import queue
import threading
import contextlib

from museic.ui.constants import INPUT_DIR


def save_file(file_obj):
    if file_obj is None:
        return None, "No file provided"
    dest = os.path.join(INPUT_DIR, os.path.basename(file_obj.name))
    shutil.copy2(file_obj.name, dest)
    return dest, None


def collect_output_files(dir_path):
    if not dir_path or not os.path.exists(dir_path):
        return None
    if os.path.isfile(dir_path):
        return dir_path
    files = []
    for root, _, filenames in os.walk(dir_path):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files if files else dir_path


def stream_capture(func, *args, **kwargs):
    """Generator that yields (log_sofar, result_or_None, error_or_None) in real-time."""
    log_q = queue.Queue()
    result_box = []
    error_box = []

    def worker():
        log_buf = io.StringIO()
        class QWriter(io.IOBase):
            def __init__(self):
                self._buf = log_buf
                self._q = log_q
            def write(self, s):
                self._buf.write(s)
                self._q.put(s)
            def flush(self):
                pass

        writer = QWriter()
        with contextlib.redirect_stdout(writer):
            try:
                result_box.append(func(*args, **kwargs))
            except Exception as e:
                error_box.append(str(e))

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    log_sofar = ""
    while thread.is_alive():
        try:
            text = log_q.get(timeout=0.3)
            log_sofar += text
        except queue.Empty:
            pass
        yield log_sofar, None, None

    while not log_q.empty():
        log_sofar += log_q.get_nowait()

    if error_box:
        yield log_sofar, None, error_box[0]
    elif result_box:
        yield log_sofar, result_box[0], None
    else:
        yield log_sofar, None, None
