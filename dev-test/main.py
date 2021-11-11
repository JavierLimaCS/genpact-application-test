from handler import Handler
from observer import ObserverHandler
import pandas
import os

class Main():
   def __init__(self):
      self.handler = Handler()
      self.observer = ObserverHandler()
      self.observer.initializeObserver(self.handler.event_handler)


if __name__=="__main__":
   #-- defines where Processed and Not applicable folder are meant to be
   processed_folder = './data/Processed'
   not_aplicable_folder = './data/Not_applicable'

   #-- create default folder location
   os.makedirs(processed_folder, exist_ok=True)
   os.makedirs(not_aplicable_folder, exist_ok=True)
      
   Main()


