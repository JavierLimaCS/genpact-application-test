from watchdog.observers import Observer
import time

class ObserverHandler():
    def __init__(self, path) -> None:
        self.observer : Observer = Observer()
        self.path : str = path
        self.recursive : bool = True
        self.ev = None


    def initializeObserver(self, my_event_handler):
        if not self.ev:
            self.ev = my_event_handler
        self.observer.schedule(my_event_handler, self.path, recursive=self.recursive)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()



