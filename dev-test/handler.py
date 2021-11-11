from watchdog.events import PatternMatchingEventHandler
import pandas as p
import os
import time

class Handler():
    def __init__(self) -> None:
        self.patterns : list = ['*']
        self.ignore_patterns : list = None
        self.ignore_directories : bool = True
        self.case_sensitive : bool = True
        self.path : str = './data/'
        self.recursive : bool = True
        self.dataframe = p.DataFrame()
        self.event_handler = PatternMatchingEventHandler(self.patterns, self.ignore_patterns, self.ignore_directories, self.case_sensitive)
        self.__setupEventHandler()


    def __setupEventHandler(self):
        self.event_handler.on_created = self.created
        self.event_handler.on_deleted = self.deleted
        self.event_handler.on_modified = self.modified
        self.event_handler.on_moved = self.moved


    def created(self, event):
        files = os.listdir(self.path)
        print(files)
        #-- looping through folder path to find every .xls or .xlsx file
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xls'):  
                try:
                    if self.awaitFileIsDone(event.src_path): #awaits file creation is done at folder
                        excel_file = p.ExcelFile(self.path+file)
                        sheets = excel_file.sheet_names
                        for sheet in sheets: #-- loop through sheets inside an Excel file
                            df = excel_file.parse(sheet_name = sheet)
                            self.dataframe = self.dataframe.append(df, ignore_index=True)
                    self.dataframe.to_excel('master.xlsx')
                except Exception as e:
                    print(e)
            #else:
                #TODO move to Not applicable folder
                #os.rename(event.src_path, './data/Not_applicable/'+file


    def deleted(self, event):
        print(f"{event.src_path} has been deleted!")


    def modified(self, event):
        print(f"{event.src_path} has been modified!")


    def moved(self, event):
        print(f"{event.src_path} has been moved to {event.dest_path}!")

    
    def awaitFileIsDone(self, filename):
        fileSize = -1
        while (fileSize != os.path.getsize(filename)):    
            fileSize = os.path.getsize(filename)
            time.sleep(1)
        print(f"{filename} has been created!")
        return True

