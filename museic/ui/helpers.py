import os
import io
import shutil
import contextlib

from museic.ui.constants import INPUT_DIR


def save_file(file_obj):
    if file_obj is None:
        return None, "No file provided"
    dest = os.path.join(INPUT_DIR, os.path.basename(file_obj.name))
    shutil.copy2(file_obj.name, dest)
    return dest, None


def run_capture(func, *args, **kwargs):
    log_capture = io.StringIO()
    with contextlib.redirect_stdout(log_capture):
        try:
            result = func(*args, **kwargs)
            return result, log_capture.getvalue(), None
        except Exception as e:
            return None, log_capture.getvalue(), str(e)


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
