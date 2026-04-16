import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from museic.core.extractor import process_extraction

class AudioHandler(FileSystemEventHandler):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
            print(f"\n[EVENT] New file detected: {os.path.basename(event.src_path)}")
            try:
                time.sleep(1) 
                process_extraction(event.src_path, duration=30, output_dir=self.output_dir)
                print("[EVENT] Processing complete. Watching for new files...")
            except Exception as e:
                print(f"Error processing file: {e}")

def start_watching(input_dir, output_dir="output"):
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    event_handler = AudioHandler(output_dir)
    observer = Observer()
    observer.schedule(event_handler, input_dir, recursive=False)
    observer.start()

    print(f"Watch Mode Active")
    print(f"Monitoring directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print("Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nWatch Mode Terminated")
    observer.join()