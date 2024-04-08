import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class ScriptRestarter(PatternMatchingEventHandler):
    patterns = ["*.py", "*.env"]  # Add any file patterns to watch

    def __init__(self, command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command
        self.process = None

    def on_any_event(self, event):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen(self.command, shell=True)

def main(script_name):
    command = f'python {script_name}'
    event_handler = ScriptRestarter(command)
    event_handler.process = subprocess.Popen(command, shell=True)

    path = "."  # Directory to watch
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    script_name = sys.argv[1]  # Pass your main script name as an argument
    main(script_name)
