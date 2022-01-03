#-*- coding: utf-8 -*-

import os

## Dictionary
# CSV
csv_sep_dict = {0: ',', 1: '\t'}
csv_encoding_dict = {0: 'utf-8', 1: 'euc-kr', 2: 'cp949', 3: 'latin1'}

# Matplotlib Colors
bar_graph_color_dict = {"C0": "#1f77b4", "C1": "#ff7f0e", "C2": "#2ca02c", "C3": "#d62728", "C4": "#9467bd", "C5": "#8c564b", "C6": "#e377c2", "C7": "#7f7f7f", "C8": "#bcbd22", "C9": "#17becf"}

## Location
# CONFIG
config_common = os.path.dirname(__file__) + '/config.json'

# ICON
icon_file_open = os.path.dirname(__file__) + "/common/resources/file_open.png"
icon_file_save = os.path.dirname(__file__) + "/common/resources/file_save.png"

## String
# Title
messagebox_error_title_kr = "오류"
messagebox_information_title_kr = "정보"

# Message
error_bad_csv_file_kr = "CSV 파일이 올바르지 않습니다"
error_bad_csv_encoding_kr = "인코딩 설정이 올바르지 않습니다"
error_wordcloud_bad_font_size_kr = "최대 글꼴 크기가 최초 글꼴 크기보다 작습니다"
error_bargraph_bad_limit_size_kr = "표시할 단어의 수가 실제 단어의 수보다 많습니다"
information_wordcloud_file_save_success_kr = "워드 클라우드 파일이 저장되었습니다"
information_wordcount_result_file_save_success_kr = "단어 빈도 분석 결과 파일이 저장되었습니다"
information_wordcount_graph_file_save_success_kr = "단어 빈도 막대 그래프 파일이 저장되었습니다"
information_wordcloud_set_default_font = "글꼴을 설정하지 않았기 때문에 기본 글꼴로 설정됩니다"

## UI Layout
# QT Design File
ui_help_main = os.path.dirname(__file__) + "/ui/help_main.ui"
ui_main = os.path.dirname(__file__) + "/ui/main.ui"
ui_wordcloud_generator = os.path.dirname(__file__) + "/ui/wordcloud_generator.ui"
ui_wordcount_generator = os.path.dirname(__file__) + "/ui/wordcount_generator.ui"

# File Dialogue
ui_file_dialogue_csv_filter_kr = "CSV UTF-8(쉼표로 분리) (*.csv);;CSV UTF-8(탭으로 분리) (*.csv);;CSV EUC-KR(쉼표로 분리) (*.csv);;CSV EUC-KR(탭으로 분리) (*.csv);;CSV CP949(쉼표로 분리) (*.csv);;CSV CP949(탭으로 분리) (*.csv);;CSV ISO-8859-1(쉼표로 분리) (*.csv);;CSV ISO-8859-1(탭으로 분리) (*.csv)"
ui_file_dialogue_csv_universal_filter_kr = "CSV (*.csv)"
ui_file_dialogue_png_jpg_filter_kr = "Portable Network Graphics (*.png);;JPEG Image File (*.jpg)"
ui_file_dialogue_png_filter_kr = "Portable Network Graphics (*.png)"
ui_file_dialogue_ttf_filter_kr = "트루타입 글꼴 파일 (*.ttf)"
ui_file_dialouge_read_title_kr = "파일 열기"
ui_file_dialouge_save_title_kr = "파일 저장"
