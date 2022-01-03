#-*- coding: utf-8 -*-

import json
import numpy as np
import os
import pandas as pd
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PIL import Image
from wordcloud import ImageColorGenerator
from wordcloud import WordCloud

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from common import *
from config import *

ui_wordcloud_main = uic.loadUiType(ui_wordcloud_generator)[0]

class WordcloudMainWindow(QMainWindow, ui_wordcloud_main):
    def __init__(self):
        super(WordcloudMainWindow, self).__init__()
        self.setupUi(self)

        try:
            # Config
            with open(config_common, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.csv_file = config['WORDCLOUD']['CSV_FILE']
            self.font_file = config['WORDCLOUD']['FONT_FILE']
            self.csv_sep_idx = config['WORDCLOUD']['CSV_SEP_IDX']
            self.csv_encoding_idx = config['WORDCLOUD']['CSV_ENCODING_IDX']
            self.stopwords = ''
            self.background_file = ''
            self.wordcloud_width = 800
            self.wordcloud_height = 600
            self.wordcloud_minfont = 20
            self.wordcloud_maxfont = 200
            self.csv_sep_dict = csv_sep_dict
            self.csv_encoding_dict = csv_encoding_dict

            # UI Layout: Wordcloud
            self.fig = plt.Figure(figsize=(9, 9))
            self.canvas = FigureCanvas(self.fig)
            self.axes = self.canvas.figure.add_subplot()
            self.axes.axis('off')
            self.wordcloud_canvas.addWidget(self.canvas)

            # UI Layout: 데이터 파일
            self.file_csv_file_ledit.setText(self.csv_file)
            self.file_csv_file_ledit.textChanged.connect(lambda: self.lineedit_ehandler('csv'))
            self.file_csv_file_btn.setIcon(QIcon(icon_file_open))
            self.file_csv_file_btn.clicked.connect(lambda: self.file_open('csv'))
            
            for line in ['쉼표로 분리', '탭으로 분리']:
                self.file_csv_file_sep_cmbbox.addItem(line)
            
            for line in ['UTF-8', 'euc-kr (한국어)', 'cp949 (한국어)', 'latin1 (영어)']:
                self.file_csv_file_encoding_cmbbox.addItem(line)

            self.file_csv_file_sep_cmbbox.currentIndexChanged.connect(lambda: self.cmbbox_ehandler('sep'))
            self.file_csv_file_encoding_cmbbox.currentIndexChanged.connect(lambda: self.cmbbox_ehandler('encoding'))

            # UI Layout: 글꼴 파일
            self.file_font_file_ledit.setText(self.font_file)
            self.file_font_file_ledit.textChanged.connect(lambda: self.lineedit_ehandler('font'))
            self.file_font_file_btn.setIcon(QIcon(icon_file_open))
            self.file_font_file_btn.clicked.connect(lambda: self.file_open('font'))
            
            # UI Layout: 불용어 설정
            self.stopwords_opt_chkbox.stateChanged.connect(lambda: self.chkbox_ehandler('stopwords'))
            self.stopwords_ledit.setEnabled(False)
            self.stopwords_ledit.textChanged.connect(lambda: self.lineedit_ehandler('stopwords'))
            self.stopwords_btn.setIcon(QIcon(icon_file_open))
            self.stopwords_btn.setEnabled(False)
            self.stopwords_btn.clicked.connect(lambda: self.file_open('stopwords'))
            
            # UI Layout: 옵션
            self.opt_width_sbox.valueChanged.connect(lambda: self.sbox_ehandler('width'))
            self.opt_height_sbox.valueChanged.connect(lambda: self.sbox_ehandler('height'))
            self.opt_minfont_sbox.valueChanged.connect(lambda: self.sbox_ehandler('minfont'))
            self.opt_maxfont_sbox.valueChanged.connect(lambda: self.sbox_ehandler('maxfont'))

            # UI Layout: 배경 이미지 설정
            self.opt_background_chkbox.stateChanged.connect(lambda: self.chkbox_ehandler('background'))
            self.opt_background_file_ledit.setEnabled(False)
            self.opt_background_file_ledit.textChanged.connect(lambda: self.lineedit_ehandler('background'))
            self.opt_background_file_btn.setIcon(QIcon(icon_file_open))
            self.opt_background_file_btn.setEnabled(False)
            self.opt_background_file_btn.clicked.connect(lambda: self.file_open('background'))

            # UI Layout: 실행
            self.view_preview_table_btn.clicked.connect(lambda: self.btn_ehandler('view_preview_table'))
            self.make_wordcloud_btn.clicked.connect(lambda: self.btn_ehandler('make_wordcloud'))
            self.save_wordcloud_btn.setEnabled(False)
            self.save_wordcloud_btn.clicked.connect(lambda: self.btn_ehandler('save_wordcloud'))
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))
            sys.exit(1)

    ## Event Handler
    # QCheckbox
    def chkbox_ehandler(self, chkbox_type):
        if chkbox_type == "background":
            if self.opt_background_chkbox.isChecked() == True:
                self.opt_background_file_ledit.setEnabled(True)
                self.opt_background_file_btn.setEnabled(True)
            else:
                self.opt_background_file_ledit.setEnabled(False)
                self.opt_background_file_ledit.setText('')
                self.opt_background_file_btn.setEnabled(False)
        elif chkbox_type == "stopwords":
            if self.stopwords_opt_chkbox.isChecked() == True:
                self.stopwords_ledit.setEnabled(True)
                self.stopwords_btn.setEnabled(True)
            else:
                self.stopwords_ledit.setEnabled(False)
                self.stopwords_ledit.setText('')
                self.stopwords_btn.setEnabled(False)

    
    # QCombobox
    def cmbbox_ehandler(self, cmbbox_type):
        if cmbbox_type == "sep":
            self.csv_sep_idx = self.file_csv_file_sep_cmbbox.currentIndex()
        elif cmbbox_type == "encoding":
            self.csv_encoding_idx = self.file_csv_file_encoding_cmbbox.currentIndex()

    
    # QFileDialog.getOpenFileName
    def file_open(self, file_type):
        if file_type == 'csv':
            file_path = QFileDialog.getOpenFileName(self, ui_file_dialouge_read_title_kr, filter=ui_file_dialogue_csv_filter_kr)
            if len(file_path[0]) > 0:
                csv_idx = ui_file_dialogue_csv_filter_kr.split(';;').index(file_path[1])
                self.csv_sep_idx = csv_idx%2
                self.csv_encoding_idx = csv_idx//2
                self.file_csv_file_sep_cmbbox.setCurrentIndex(self.csv_sep_idx)
                self.file_csv_file_encoding_cmbbox.setCurrentIndex(self.csv_encoding_idx)
            self.file_csv_file_ledit.setText(file_path[0])
        elif file_type == 'font':
            file_path = QFileDialog.getOpenFileName(self, ui_file_dialouge_read_title_kr, filter=ui_file_dialogue_ttf_filter_kr)
            self.file_font_file_ledit.setText(file_path[0])
        elif file_type == 'stopwords':
            file_path = QFileDialog.getOpenFileName(self, ui_file_dialouge_read_title_kr, filter=ui_file_dialogue_csv_filter_kr)
            if len(file_path[0]) > 0:
                stopwords_csv_idx = ui_file_dialogue_csv_filter_kr.split(';;').index(file_path[1])
                stopwords_csv_sep_idx = stopwords_csv_idx%2
                stopwords_csv_encoding_idx = stopwords_csv_idx//2
                self.stopwords_ledit.setText(','.join([x[0] for x in pd.read_csv(file_path[0], sep=self.csv_sep_dict[stopwords_csv_sep_idx], encoding=self.csv_encoding_dict[stopwords_csv_encoding_idx]).iloc[:,:1].values.tolist()]))
        elif file_type == 'background':
            file_path = QFileDialog.getOpenFileName(self, ui_file_dialouge_read_title_kr, filter=ui_file_dialogue_png_jpg_filter_kr)
            self.opt_background_file_ledit.setText(file_path[0])
    

    # QFileDialog.getSaveFileName
    def file_save(self, file_type):
        file_path = QFileDialog.getSaveFileName(self, ui_file_dialouge_save_title_kr, "", ui_file_dialogue_png_filter_kr)
        if file_type == 'wordcloud':
            return file_path[0]
    

    # QLineEdit
    def lineedit_ehandler(self, lineedit_type):
        if lineedit_type == "csv":
            self.csv_file = self.file_csv_file_ledit.text()
        elif lineedit_type == "font":
            self.font_file = self.file_font_file_ledit.text()
        elif lineedit_type == "background":
            self.background_file = self.opt_background_file_ledit.text()
        elif lineedit_type == "stopwords":
            self.stopwords = self.stopwords_ledit.text()

    
    # QPushButton
    def btn_ehandler(self, btn_type):
        if btn_type == 'view_preview_table':
            self.table_preview(self.csv_file, self.font_file, self.csv_sep_idx, self.csv_encoding_idx, self.stopwords, self.wordcloud_width, self.wordcloud_height, self.wordcloud_minfont, self.wordcloud_maxfont, self.background_file, 0)
        elif btn_type == 'make_wordcloud':
            self.table_preview(self.csv_file, self.font_file, self.csv_sep_idx, self.csv_encoding_idx, self.stopwords, self.wordcloud_width, self.wordcloud_height, self.wordcloud_minfont, self.wordcloud_maxfont, self.background_file, 1)
        elif btn_type == 'save_wordcloud':
            self.save_wordcloud()


    #QSpinBox
    def sbox_ehandler(self, sbox_type):
        if sbox_type == "width":
            self.wordcloud_width = self.opt_width_sbox.value()
        elif sbox_type == "height":
            self.wordcloud_height = self.opt_height_sbox.value()
        elif sbox_type == "minfont":
            self.wordcloud_minfont = self.opt_minfont_sbox.value()
        elif sbox_type == "maxfont":
            self.wordcloud_maxfont = self.opt_maxfont_sbox.value()


    # 테이블 보기
    def table_preview(self, csv_file, font_file, csv_sep_idx, csv_encoding_idx, stopwords, wordcloud_width, wordcloud_height, wordcloud_minfont, wordcloud_maxfont, background_file, make_wordcloud_idx):
        try:
            preview_df = pd.read_csv(csv_file, sep=self.csv_sep_dict[csv_sep_idx], encoding=self.csv_encoding_dict[csv_encoding_idx])
            if len(stopwords)>0:
                stopwords_lst = stopwords.split(',')
                for w in stopwords_lst:
                    preview_df = preview_df[~preview_df[str(preview_df.columns[0])].map(lambda x: x == str(w))]

            self.table_prev_model = PandasTableModel(preview_df)
            self.preview_tblview.setModel(self.table_prev_model)
            self.preview_tblview.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
            if make_wordcloud_idx==1:
                self.make_wordcloud(preview_df, font_file, wordcloud_width, wordcloud_height, wordcloud_minfont, wordcloud_maxfont, background_file)
        except FileNotFoundError:
            QMessageBox.critical(self, messagebox_error_title_kr, error_bad_csv_file_kr)
        except UnicodeDecodeError:
            QMessageBox.critical(self, messagebox_error_title_kr, error_bad_csv_encoding_kr)
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))


    # 워드 클라우드 만들기
    def make_wordcloud(self, wordcloud_df, font_file, wordcloud_width, wordcloud_height, wordcloud_minfont, wordcloud_maxfont, background_file):
        try:
            if(wordcloud_maxfont<wordcloud_minfont):
                raise ValueError(error_wordcloud_bad_font_size_kr)
            if(len(font_file)==0):
                QMessageBox.information(self, messagebox_information_title_kr, information_wordcloud_set_default_font)
                font_file = None
            if(len(background_file)):
                mask_image = background_file
                mask = np.array(Image.open(mask_image))
                mask_colors = ImageColorGenerator(mask)
            else:
                mask = None

            self.wordcloud = WordCloud(font_path=font_file, width=wordcloud_width, height=wordcloud_height, min_font_size=wordcloud_minfont, max_font_size=wordcloud_maxfont, background_color="rgba(255, 255, 255, 0)", mode="RGBA", mask=mask)
            self.wordcloud = self.wordcloud.generate_from_frequencies(dict(wordcloud_df.values.tolist()))
            self.axes.clear()
            self.axes.axis('off')
            if(len(background_file)>0):
                self.wordcloud = self.wordcloud.recolor(color_func = mask_colors)
            self.axes.imshow(self.wordcloud, interpolation="bilinear")
            self.canvas.draw()
            self.save_wordcloud_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))
    

    # 워드 클라우드 저장
    def save_wordcloud(self):
        output_file = self.file_save('wordcloud')
        if(len(output_file)>0):
            self.wordcloud.to_file(output_file)
            QMessageBox.information(self, messagebox_information_title_kr, information_wordcloud_file_save_success_kr)
        

def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    wordcloudMainWindow = WordcloudMainWindow()
    wordcloudMainWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
