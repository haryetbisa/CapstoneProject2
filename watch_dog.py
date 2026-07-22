
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = self.start()

    def start(self):
        return subprocess.Popen([sys.executable, "main.py"])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Change detected: {event.src_path} — restarting...")
            self.process.kill()
            self.process = self.start()

if __name__ == "__main__":
    handler = RestartHandler()
    observer = Observer()
    observer.schedule(handler, path=".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        handler.process.kill()
    observer.join()