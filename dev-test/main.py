from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItem
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
    update_progress = pyqtSignal(int)

    def __init__(self, path) -> None:
        super().__init__()
        self.handler = Handler(path)
        self.observer = ObserverHandler(path)

    def run(self):
        if not self.observer.ev:
            self.observer.ev = self.handler.event_handler
        self.observer.observer.schedule(
            self.handler.event_handler, self.observer.path, recursive=self.observer.recursive)
        self.observer.observer.start()
        try:
            while True:
                time.sleep(1)
                self.update_progress.emit(1)
        except Exception as e:
            print("Watcher stopped", e)
            self.observer.observer.stop()
            self.observer.observer.join()

    
    def stop(self):
        print("Watcher stopped because target folder was changed")
        self.observer.observer.stop()
        self.observer.observer.join()


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
        self.model.appendRow(QStandardItem(QtGui.QIcon(
                    './dir.png'),"Processed"))
        self.list2 = self.findChild(QListView, "listView2")
        self.model2 = QtGui.QStandardItemModel()
        self.list2.setModel(self.model2)
        self.model2.appendRow(QStandardItem(QtGui.QIcon(
                    './dir.png'),"Not Applicable"))
        self.worker = None


    def browseFolder(self):
        if self.worker:
            self.worker.stop()
            self.worker.terminate()
        self.folderPath = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Folder')
        self.path.clear()
        self.path.insertPlainText(self.folderPath)
        processed_folder = '/Processed'
        not_aplicable_folder = '/Not_applicable'
        os.makedirs(self.folderPath + processed_folder, exist_ok=True)
        os.makedirs(self.folderPath +not_aplicable_folder, exist_ok=True)


    def watchFolder(self):
        self.showFiles()
        self.worker = WorkerThread(self.folderPath+'/')
        self.worker.start()
        self.worker.update_progress.connect(self.showFiles)


    def showFiles(self):
        self.model.clear()
        self.model2.clear()
        folder1 = self.folderPath + '/Processed'
        folder2 = self.folderPath + '/Not_applicable'
        processedfiles = glob.glob(folder1 + "/*.*")
        notapplicablefiles = glob.glob(folder2 + "/*.*")
        self.model.appendRow(QStandardItem(QtGui.QIcon(
                    './dir.png'), "Processed"))
        self.model2.appendRow(QStandardItem(QtGui.QIcon(
                    './dir.png'), "Not Applicable"))
        for file in processedfiles:
            if '.xls' in file or '.xlsx' in file:
                item = QtGui.QStandardItem(QtGui.QIcon(
                    './icon.png'), file.replace(folder1 + "\\", ""))
                item.setEditable(False)
                self.model.appendRow(item)
        for file in notapplicablefiles:
            item2 = QtGui.QStandardItem(QtGui.QIcon(
                './default.png'), file.replace(folder2 + "\\", ""))
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
