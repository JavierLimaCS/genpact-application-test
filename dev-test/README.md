# FOLDER WATCHER

## Programming Language

- Python --version 3.9.2

## Getting Started

Before running the app, first, be sure that Python its installed.

```shell
# Returns python version
$ python --version

# Output: Python v.v.v
```

Now, be sure to install all the libraries and modules the app needs to run correctly.

```shell
# Checks for every package included in 'requirements.txt' file, and install it.
$ pip install -r requirements.txt
```

If any package is misssing when running, please install it.
```shell
# Basic Python package install
$ pip install 'packagename'
```

## Modules and Packages required
### Pandas
- Version: 1.3.3
- Summary: Powerful data structures for data analysis, time series, and statistics
- Home-page: https://pandas.pydata.org
### Watchdog
- Version: 2.1.6
- Summary: Filesystem events monitoring
- Home-page: https://github.com/gorakhargosh/watchdog
### Openpyxl
- Version: 3.0.9
- Summary: A Python library to read/write Excel 2010 xlsx/xlsm files
- Home-page: https://openpyxl.readthedocs.io
### PyQt5 
- Version: 5.15.4
- Summary: Python bindings for the Qt cross platform application toolkit
- Home-page: https://www.riverbankcomputing.com/software/pyqt/

## Classes
- WorkerThread : class that allows the watcher to run within the UI.
- Main : class defined for setup app's UI. 
- ObserverHandler : class defined for an watchdog observer object for constantly 'watchiing' the indicated folder.
- Handler : class defined for events handling of the files in the folder indicated.