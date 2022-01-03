#-*- coding: utf-8 -*-

from collections import Counter
import itertools
import json
import os
import pandas as pd
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from common import *
from config import *

ui_wordcount_main = uic.loadUiType(ui_wordcount_generator)[0]

class WordCountMainWindow(QMainWindow, ui_wordcount_main):
    def __init__(self):
        super(WordCountMainWindow, self).__init__()
        self.setupUi(self)

        try:
            # Config
            with open(config_common, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.csv_file = ''
            self.font_file = ''
            self.csv_sep_idx = ''
            self.csv_encoding_idx = ''
            self.csv_columns = ''
            self.stopwords = ''
            self.wordcount_limit = config['WORDCOUNT']['WORDCOUNT_LIMIT']
            self.graph_wordcount_limit = 20
            self.graph_bar_color = 'C0'
            self.csv_sep_dict = csv_sep_dict
            self.csv_encoding_dict = csv_encoding_dict

            # UI Layout: Matplotlib Bar Graph
            self.fig = plt.Figure(figsize=(9, 9))
            self.canvas = FigureCanvas(self.fig)
            self.axes = self.canvas.figure.add_subplot()
            self.axes.axis('off')
            self.wordcloud_canvas.addWidget(self.canvas)


            # UI Layout: 데이터 파일
            self.file_csv_file_ledit.setEnabled(False)
            self.file_csv_file_ledit.textChanged.connect(lambda: self.lineedit_ehandler('csv'))
            self.file_csv_file_btn.setIcon(QIcon(icon_file_open))
            self.file_csv_file_btn.clicked.connect(lambda: self.file_open('csv'))
            self.file_csv_file_columns_cmbbox.addItem("------ Columns ------")
            self.file_csv_file_columns_cmbbox.currentIndexChanged.connect(lambda: self.cmbbox_ehandler('columns'))

                                  
            # UI Layout: 불용어 설정
            self.stopwords_opt_chkbox.stateChanged.connect(lambda: self.chkbox_ehandler('stopwords'))
            self.stopwords_ledit.setEnabled(False)
            self.stopwords_ledit.textChanged.connect(lambda: self.lineedit_ehandler('stopwords'))
            self.stopwords_btn.setIcon(QIcon(icon_file_open))
            self.stopwords_btn.setEnabled(False)
            self.stopwords_btn.clicked.connect(lambda: self.file_open('stopwords'))

            # UI Layout: 그래프 옵션
            self.opt_wordcountlim_sbox.valueChanged.connect(lambda: self.sbox_ehandler('wordcountlim'))
            for line in bar_graph_color_dict.keys():
                self.opt_barcolor_cmbbox.addItem(line)
            self.graph_bar_color = self.opt_barcolor_cmbbox.currentText()
            self.font_family_lst = self.check_font_list()
            for line in self.font_family_lst:
                self.opt_fontfamily_cmbbox.addItem(line)
            self.font_family = self.opt_fontfamily_cmbbox.currentText()
            self.opt_fontfamily_cmbbox.currentIndexChanged.connect(lambda: self.cmbbox_ehandler('fontfamily'))
            self.opt_barcolor_sample_lbl.setStyleSheet("background-color: " + bar_graph_color_dict[self.graph_bar_color])
            self.opt_barcolor_cmbbox.currentIndexChanged.connect(lambda: self.cmbbox_ehandler('barcolor'))

            # UI Layout: 실행
            self.view_preview_table_btn.setEnabled(False)
            self.view_preview_table_btn.clicked.connect(lambda: self.btn_handler('view_preview_table'))
            self.make_bargraph_btn.setEnabled(False)
            self.make_bargraph_btn.clicked.connect(lambda: self.btn_handler('make_bargraph'))
            self.save_preview_table_btn.setEnabled(False)
            self.save_preview_table_btn.clicked.connect(lambda: self.btn_handler('save_preview_table'))
            self.save_bargraph_btn.setEnabled(False)
            self.save_bargraph_btn.clicked.connect(lambda: self.btn_handler('save_bargraph'))
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))
            sys.exit(1)


    ## Event Handler
    # QCheckbox
    def chkbox_ehandler(self, chkbox_type):
        if chkbox_type == 'stopwords':
            if self.stopwords_opt_chkbox.isChecked() == True:
                self.stopwords_ledit.setEnabled(True)
                self.stopwords_btn.setEnabled(True)
            else:
                self.stopwords_ledit.setEnabled(False)
                self.stopwords_ledit.setText('')
                self.stopwords_btn.setEnabled(False)
    
    
    # QCombobox
    def cmbbox_ehandler(self, cmbbox_type):
        if cmbbox_type == "columns":
            self.csv_columns = self.file_csv_file_columns_cmbbox.currentIndex()
        if cmbbox_type == "fontfamily":
            self.font_family = self.opt_fontfamily_cmbbox.currentText()
            self.opt_barcolor_sample_lbl.setStyleSheet("background-color: " + bar_graph_color_dict[self.graph_bar_color])
            self.opt_barcolor_sample_lbl.setFont(QFont(self.font_family))
        if cmbbox_type == "barcolor":
            self.graph_bar_color = self.opt_barcolor_cmbbox.currentText()
            self.opt_barcolor_sample_lbl.setStyleSheet("background-color: " + bar_graph_color_dict[self.graph_bar_color])
            self.opt_barcolor_sample_lbl.setFont(QFont(self.font_family))


    # QFileDialog.getOpenFileName
    def file_open(self, file_type):
        if file_type == 'csv':
            file_path = QFileDialog.getOpenFileName(self, ui_file_dialouge_read_title_kr, filter=ui_file_dialogue_csv_filter_kr)
            if len(file_path[0]) > 0:
                csv_idx = ui_file_dialogue_csv_filter_kr.split(';;').index(file_path[1])
                self.csv_sep_idx = csv_idx%2
                self.csv_encoding_idx = csv_idx//2
                self.file_csv_file_ledit.setText(file_path[0])
                self.raw_df = pd.read_csv(file_path[0], sep=self.csv_sep_dict[self.csv_sep_idx], encoding=self.csv_encoding_dict[self.csv_encoding_idx])
                self.file_csv_file_columns_cmbbox.clear()
                for line in self.raw_df.columns:
                    self.file_csv_file_columns_cmbbox.addItem(line)
                self.view_preview_table_btn.setEnabled(True)
                self.make_bargraph_btn.setEnabled(True)
        elif file_type == 'stopwords':
            file_path = QFileDialog.getOpenFileName(self, ui_file_dialouge_read_title_kr, filter=ui_file_dialogue_csv_filter_kr)
            if len(file_path[0]) > 0:
                stopwords_csv_idx = ui_file_dialogue_csv_filter_kr.split(';;').index(file_path[1])
                stopwords_csv_sep_idx = stopwords_csv_idx%2
                stopwords_csv_encoding_idx = stopwords_csv_idx//2
                self.stopwords_ledit.setText(','.join([x[0] for x in pd.read_csv(file_path[0], sep=self.csv_sep_dict[stopwords_csv_sep_idx], encoding=self.csv_encoding_dict[stopwords_csv_encoding_idx]).iloc[:,:1].values.tolist()]))
    

    # QFileDialog.getSaveFileName
    def file_save(self, file_type):
        if file_type == 'bargraph':
            file_path = QFileDialog.getSaveFileName(self, ui_file_dialouge_save_title_kr, "", ui_file_dialogue_png_filter_kr)
            return file_path[0]
        if file_type == 'preview_table':
            file_path = QFileDialog.getSaveFileName(self, ui_file_dialouge_save_title_kr, "", ui_file_dialogue_csv_universal_filter_kr)
            return file_path[0]


    # QLineEdit
    def lineedit_ehandler(self, lineedit_type):
        if lineedit_type == "csv":
            self.csv_file = self.file_csv_file_ledit.text()
        elif lineedit_type == "fontfile":
            self.font_file = self.file_font_file_ledit.text()
        elif lineedit_type == "background":
            self.background_file = self.opt_background_file_ledit.text()
        elif lineedit_type == "stopwords":
            self.stopwords = self.stopwords_ledit.text()


    # QPushButton
    def btn_handler(self, run_type):
        if run_type == 'view_preview_table':
            self.table_preview(self.stopwords, self.font_family, self.graph_wordcount_limit, self.graph_bar_color, 0)
        elif run_type == 'make_bargraph':
            self.table_preview(self.stopwords, self.font_family, self.graph_wordcount_limit, self.graph_bar_color, 1)
        elif run_type == 'save_preview_table':
            self.save_result()
        elif run_type == 'save_bargraph':
            self.save_graph()


    #QSpinBox
    def sbox_ehandler(self, sbox_type):
        if sbox_type == "wordcountlim":
            self.graph_wordcount_limit = self.opt_wordcountlim_sbox.value()


    # 글꼴 집합 출력   
    def check_font_list(self):
        return [f.name for f in matplotlib.font_manager.fontManager.ttflist]


    # 빈도 분석 dataframe 만들기
    def make_count_df(self, count_lst):
        x_lst = []
        y_lst = []
        for idx in range(len(count_lst)):
            x_lst.append(count_lst[idx][0])
            y_lst.append(count_lst[idx][1])
        return pd.DataFrame.from_records(zip(x_lst, y_lst), columns=['VALUE', 'COUNT'])


    # 테이블 보기
    def table_preview(self, stopwords, font_family, graph_wordcount_limit, graph_bar_color, make_graph_idx):
        try:
            raw_lst = self.raw_df[str(self.raw_df.columns[self.csv_columns])].tolist()
            voca_lst = []
            for s in raw_lst:
                if type(s).__name__=='str':
                    voca_lst.append(s.split(' '))
            voca_lst = list(itertools.chain.from_iterable(voca_lst))
            if len(stopwords)>0:
                stopwords_lst = stopwords.split(',')
                voca_lst = list(filter(lambda x: x not in stopwords_lst, voca_lst))
            voca_cnt = Counter(voca_lst).most_common(self.wordcount_limit)
            self.voca_cnt_df = self.make_count_df(voca_cnt)

            self.table_prev_model = PandasTableModel(self.voca_cnt_df)
            self.preview_tblview.setModel(self.table_prev_model)
            self.preview_tblview.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.save_preview_table_btn.setEnabled(True)
            if make_graph_idx==1:
                self.make_bar_graph(self.voca_cnt_df, font_family, graph_wordcount_limit, graph_bar_color)
        except FileNotFoundError:
            QMessageBox.critical(self, messagebox_error_title_kr, error_bad_csv_file_kr)
        except UnicodeDecodeError:
            QMessageBox.critical(self, messagebox_error_title_kr, error_bad_csv_encoding_kr)
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))


    # 막대 그래프 그리기
    def make_bar_graph(self, voca_cnt_df, font_family, graph_wordcount_limit, graph_bar_color):
        try:
            plt.rc('font', family=str(font_family))
            if graph_wordcount_limit>voca_cnt_df.shape[0]:
                raise ValueError(error_bargraph_bad_limit_size_kr)
            word_lst = voca_cnt_df['VALUE'].tolist()[:graph_wordcount_limit]
            count_lst = voca_cnt_df['COUNT'].tolist()[:graph_wordcount_limit]
            
            self.axes.clear()
            self.axes.bar(word_lst, count_lst, color=graph_bar_color)
            self.canvas.draw()

            self.save_bargraph_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, messagebox_error_title_kr, str(sys.exc_info()[1]))
    

    # 빈도 분석 결과 저장
    def save_result(self):
        output_file = self.file_save('preview_table')
        if(len(output_file)>0):
            self.voca_cnt_df.to_csv(output_file, sep=',', encoding='utf-8-sig', index=False)
            QMessageBox.information(self, messagebox_information_title_kr, information_wordcount_result_file_save_success_kr)


    # 막대 그래프 저장
    def save_graph(self):
        output_file = self.file_save('bargraph')
        if(len(output_file)>0):
            self.axes.figure.savefig(output_file, bbox_inches='tight', transparent=True)
            QMessageBox.information(self, messagebox_information_title_kr, information_wordcount_graph_file_save_success_kr)
        

def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    wordcountMainWindow = WordCountMainWindow()
    wordcountMainWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
