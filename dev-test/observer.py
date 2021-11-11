from watchdog.observers import Observer

class ObserverHandler():
    def __init__(self) -> None:
        self.observer : Observer = Observer()
        self.path : str = '.'
        self.recursive : bool = True


    def initializeObserver(self, my_event_handler):
        self.observer.schedule(my_event_handler, self.path, recursive=self.recursive)
        self.observer.start()


    def updateObserver(self):
        pass

    
    def getPath(self):
        return self.path

    
    def setPath(self, path):
        self.path = path

    
    def getRecursive(self):
        return self.go_recursive


    def setRecursive(self, recursive):
        self.recursive = recursive


