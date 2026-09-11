import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def watch(folder, pattern, callback):
    class Handler(PatternMatchingEventHandler):
        def __init__(self):
            super().__init__(patterns=[pattern])

        def on_modified(self, event):
            callback(event.src_path)

    observer = Observer()
    observer.schedule(Handler(), folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
