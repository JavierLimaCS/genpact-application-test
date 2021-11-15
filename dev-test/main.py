from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItem
from watchdog import observers
from handler import Handler
from observer import ObserverHandler
import time
import os
import sys
import glob
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QListView, QMainWindow, QPlainTextEdit, QPushButton


class WorkerThread(QThread):
   def __init__(self,) -> None:
       super().__init__()
       self.handler = Handler()
       self.observer = ObserverHandler()

   def run(self):
      if not self.observer.ev:
            self.observer.ev = self.handler.event_handler
      self.observer.observer.schedule(
      self.handler.event_handler, self.observer.path, recursive=self.observer.recursive)
      self.observer.observer.start()
      try:
         while True:
            time.sleep(1)
      except KeyboardInterrupt:
            print("Watcher detenido")
            self.observer.stop()
            self.observer.join()


class Main(QMainWindow):
   def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('./main_window.ui', self)
        self.path = self.findChild(QPlainTextEdit, "textEditFolder")
        self.console = self.findChild(QPlainTextEdit, "textEditConsole")
        self.btnBrowse = self.findChild(QPushButton, "buttonBrowse")
        self.btnBrowse.clicked.connect(self.browseFolder)
        self.btnWatch = self.findChild(QPushButton, "buttonWatch")
        self.btnWatch.clicked.connect(self.watchFolder)
        self.list = self.findChild(QListView, "listView")
        self.model = QtGui.QStandardItemModel()
        self.list.setModel(self.model)
        self.model.appendRow(QStandardItem("Processed"))
        self.list2 = self.findChild(QListView, "listView2")
        self.model2 = QtGui.QStandardItemModel()
        self.list2.setModel(self.model2)
        self.model2.appendRow(QStandardItem("Not Applicable"))


   def browseFolder(self):
        self.folderPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Folder')
        self.path.clear()
        self.path.insertPlainText(self.folderPath)
        self.showFiles()
        raise KeyboardInterrupt


   def watchFolder(self):
        self.showFiles()
        self.worker = WorkerThread()
        self.worker.start()

   
   def showFiles(self):
        self.model.clear()
        self.model2.clear()
        onlyfiles = glob.glob(self.folderPath + "/*.*")
        for file in onlyfiles:
            if '.xls' in file or '.xlsx' in file:
                print(file.replace(self.folderPath + "\\", ""))
                item = QtGui.QStandardItem(QtGui.QIcon(
                    './icon.png'), file.replace(self.folderPath + "\\", ""))
                item.setEditable(False)
                self.model.appendRow(item)
            else:
                print(file.replace(self.folderPath + "\\", ""))
                item2 = QtGui.QStandardItem(QtGui.QIcon(
                    './default.png'), file.replace(self.folderPath + "\\", ""))
                item2.setEditable(False)
                self.model2.appendRow(item2)


if __name__ == "__main__":
    # -- defines where Processed and Not applicable folder are meant to be
    processed_folder = './data/Processed'
    not_aplicable_folder = './data/Not_applicable'
    cwd = os.getcwd()
    cwd = cwd.replace('\\', '/')
    cwd += '/data'
    # -- create default folder location
    os.makedirs(processed_folder, exist_ok=True)
    os.makedirs(not_aplicable_folder, exist_ok=True)

    app = QApplication(sys.argv)
    mainWindow = Main()
    mainWindow.folderPath = cwd
    mainWindow.path.insertPlainText(cwd)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedWidth(789)
    widget.setFixedHeight(533)
    widget.setWindowTitle("Folder Watcher")
    widget.show()
    sys.exit(app.exec_())
