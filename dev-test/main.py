from handler import Handler
from observer import ObserverHandler

class Main():
   def __init__(self):
      handler = Handler()
      observer = ObserverHandler()
      observer.initializeObserver(handler.event_handler)
      

if __name__=="__main__":
   Main()


