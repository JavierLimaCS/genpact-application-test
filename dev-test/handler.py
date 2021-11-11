from watchdog.events import PatternMatchingEventHandler
import os

class Handler():
    def __init__(self) -> None:
        self.patterns : list = ['*']
        self.ignore_patterns : list = None
        self.ignore_directories : bool = True
        self.case_sensitive : bool = True
        self.path : str = '.'
        self.recursive : bool = True
        self.event_handler = PatternMatchingEventHandler(self.patterns, self.ignore_patterns, self.ignore_directories, self.case_sensitive)
        self.__setupEventHandler()


    def __setupEventHandler(self):
        self.event_handler.on_created = self.created
        self.event_handler.on_deleted = self.deleted
        self.event_handler.on_modified = self.modified
        self.event_handler.on_moved = self.moved

    def created(self, event):
        if self.path == '.':
            files = os.listdir(self.path+'/data')
        else:
            files = os.listdir(self.path)
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):  
                print('.xls founded')
        print(f"{event.src_path} has been created!")


    def deleted(self, event):
        print(f"{event.src_path} has been deleted!")


    def modified(self, event):
        print(f"{event.src_path} has been modified!")


    def moved(self, event):
        print(f"{event.src_path} has been moved to {event.dest_path}!")

