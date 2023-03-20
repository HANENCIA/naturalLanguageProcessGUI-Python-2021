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

import help
import wordcount_generator
import wordcloud_generator

ui_main = uic.loadUiType(ui_main)[0]


class NLPMainWindow(QMainWindow, ui_main):
    def __init__(self, parent=None):
        super(NLPMainWindow, self).__init__(parent)
        self.setupUi(self)

        try:
            # Config
            self.csv_sep_dict = csv_sep_dict
            self.csv_encoding_dict = csv_encoding_dict

            # UI Layout: Menu Bar
            self.menu_action_open.triggered.connect(self.file_open)
            self.menu_action_wordcount.triggered.connect(lambda: self.action_ehandler('wordcount'))
            self.menu_action_wordcloud.triggered.connect(lambda: self.action_ehandler('wordcloud'))
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))
            sys.exit(1)

    ## Event Handler
    # closeEvent
    def closeEvent(self, QCloseEvent):
        self.p.terminate()
        sys.exit(0)

    # QAction
    def action_ehandler(self, app_type):
        if app_type == 'wordcount':
            self.p = WordcountModule()
            self.p.Daemon = True
            self.p.start()
        elif app_type == 'wordcloud':
            self.p = WordcloudModule()
            self.p.Daemon = True
            self.p.start()

    # QFileDialog.getOpenFileName
    def file_open(self):
        file_path = QFileDialog.getOpenFileName(self, ui_file_dialouge_read_title_kr,
                                                filter=ui_file_dialogue_csv_filter_kr)
        if len(file_path[0]) > 0:
            csv_idx = ui_file_dialogue_csv_filter_kr.split(';;').index(file_path[1])
            csv_sep_idx = csv_idx % 2
            csv_encoding_idx = csv_idx // 2
            self.table_rawdata(file_path[0], csv_sep_idx, csv_encoding_idx)

    def table_rawdata(self, csv_file, csv_sep_idx, csv_encoding_idx):
        try:
            rawdata_df = pd.read_csv(csv_file, sep=self.csv_sep_dict[csv_sep_idx],
                                     encoding=self.csv_encoding_dict[csv_encoding_idx])
            self.table_rawdata_model = PandasTableModel(rawdata_df)
            self.rawdata_tblview.setModel(self.table_rawdata_model)
            self.rawdata_tblview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except FileNotFoundError:
            QMessageBox.critical(self, messagebox_error_title_kr, "CSV 파일이 올바르지 않습니다")
        except UnicodeDecodeError:
            QMessageBox.critical(self, messagebox_error_title_kr, "인코딩 설정이 올바르지 않습니다")
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))


# 단어 빈도 분석
class WordcountModule(multiprocessing.Process):
    def __init__(self):
        super(WordcountModule, self).__init__()

    def run(self):
        wordcount_generator.main()


# 워드 클라우드
class WordcloudModule(multiprocessing.Process):
    def __init__(self):
        super(WordcloudModule, self).__init__()

    def run(self):
        wordcloud_generator.main()


def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    nlpMainWindow = NLPMainWindow()
    nlpMainWindow.show()
    app.exec_()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
