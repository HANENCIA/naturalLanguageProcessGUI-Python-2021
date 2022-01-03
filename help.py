import json
import multiprocessing
import numpy as np
import os
import pandas as pd
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from common import *
from config import *

ui_main = uic.loadUiType(ui_main)[0]

class MainHelpWindow(QMainWindow, ui_main):
    def __init__(self, parent=None):
        super(MainHelpWindow, self).__init__(parent)
        self.setupUi(self)