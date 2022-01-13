import sys
from typing import DefaultDict
# 표 생성 함수
# QMainWindow: 상태표시줄, 메뉴 추가 / QAction: 메뉴 액션 추가 / QMenu: menu sub group 추가 / qApp: 앱 종료 함수 사용
# from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox, QMainWindow, QAction, QMenu, qApp,
# QVBoxLayout, QHBoxLayout)
from PyQt5.QtWidgets import *
# 이벤트 처리. 슬롯으로 연결해줌(connect).
from PyQt5.QtCore import QCoreApplication, QLine, Qt
# table Read only mode
from PyQt5 import QtGui
from PyQt5.QtGui import *
# Tree view에 나열되는 내용을 담당.
# from PyQt5.QtGui import QStandardItemModel

from pymysql import NULL

from database import DB

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from datetime import datetime
import datetime

import os
import shutil

from PIL import Image

from automation import Automation

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

class report(QWidget):
    global db
    global auto

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("경기도청 보고 데이터")
        self.setWindowIcon(QIcon("D:\\Master\\PythonWorkspace\\NYNOA\\Icons\\남양노아요양보호사.jpg"))
        self.doc_type = ""

    """
    def onActivated(self):
        self.previous_text = self.current_text
        self.current_text = self.combobox_T.currentText()

        if self.previous_text in self.time_list and self.current_text in self.time_list:
            # not type changed
            pass
        elif self.previous_text == self.current_text:
            # not changed
            pass
        else:
            self.combobox_N.clear()
            self.combobox_N.addItem("선택")
            self.class_num_list.clear()

            if self.current_text == "대체실습":
                rs = db.main.dbPrograms.SELECT("classNumber", "temptraining", orderBy="classNumber *1")
            else:
                rs = db.main.dbPrograms.SELECT("classNumber", "lecture", orderBy="classNumber *1")

            if rs == "error":
                QMessageBox.information(self, "ERROR", "class batchUpdate returns error", QMessageBox.Yes, QMessageBox.Yes)
            else:
                for row in rs:
                    if not row[0] in self.class_num_list:
                        self.class_num_list.append(row[0])
                
                self.combobox_N.addItems(self.class_num_list)
        """

    def initUI(self):
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.box.addLayout(self.hbox1)
        self.box.addLayout(self.hbox2)

        self.label_number = QLabel("기수", self)
        self.hbox1.addWidget(self.label_number)
        self.combobox_N = QComboBox(self)
        self.combobox_N.setFixedWidth(100)
        self.hbox1.addWidget(self.combobox_N)

        self.label_time = QLabel("반", self)
        self.label_time.setFixedWidth(48)
        # self.label_time.setAlignment(Qt.AlignVCenter)
        self.label_time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # self.label_time.setStyleSheet("text-align: right;")
        self.hbox1.addWidget(self.label_time)
        self.combobox_T = QComboBox(self)
        self.combobox_T.setFixedWidth(100)
        self.hbox1.addWidget(self.combobox_T)

        self.hbox2.addStretch(1)
        self.btn_create = QPushButton("생성", self)
        self.hbox2.addWidget(self.btn_create)
        self.btn_cancel = QPushButton("취소", self)
        self.hbox2.addWidget(self.btn_cancel)

        self.btn_create.clicked.connect(self.getData)
        self.btn_cancel.clicked.connect(self.close)

    def getData(self):
        class_number = self.combobox_N.currentText()
        class_time = self.combobox_T.currentText()

        ans = QMessageBox.question(self, "확인", "{}기 {} {} 데이터를 생성합니다.".format(class_number, class_time, self.doc_type), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            QMessageBox.about(self, "안내", "OK버튼을 눌러 작업을 진행해 주세요.\n생성이 완료되면 엑셀 파일이 열립니다.")
            auto.report(self.doc_type, class_number, class_time)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        
        elif e.key() == Qt.Key_Enter:
            self.getData()

    def showEvent(self, QShowEvent):
        self.setWindowTitle("경기도청 " + self.doc_type)
        self.combobox_N.clear()
        self.combobox_T.clear()
        self.class_num_list = []

        """
        개강보고
        대체실습 실시보고
        대체실습 수료보고
        """

        if self.doc_type == "개강보고":
            self.label_time.setText("반")
            self.combobox_T.setEnabled(True)
            self.combobox_N.addItem("선택")
            self.combobox_T.addItem("선택")
            self.combobox_T.addItem("주간")
            self.combobox_T.addItem("야간")
            rs = db.main.dbPrograms.SELECT("classNumber", "lecture", orderBy="classNumber *1")

        else:
            self.label_time.setText("대체실습")
            self.combobox_T.setEnabled(False)
            rs = db.main.dbPrograms.SELECT("classNumber", "temptraining", orderBy="classNumber *1")
        
        if rs == "error":
            QMessageBox.information(self, "ERROR", "class batchUpdate returns error", QMessageBox.Yes, QMessageBox.Yes)
        else:
            for row in rs:
                if not row[0] in self.class_num_list:
                    self.class_num_list.append(row[0])
            
            self.combobox_N.addItems(self.class_num_list)
        
        


class scanFile(QWidget):
    global db

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("파일 스캔")
        self.setWindowIcon(QIcon("D:\\Master\\PythonWorkspace\\NYNOA\\Icons\\남양노아요양보호사.jpg"))
        self.file_list = []
        self.file_index = 0
        
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.target_table = "user"
        cnt_row = 5
        cnt_col = 7
        self.resize(600, 400)

        self.labelImg = QLabel(self)
        self.labelImg.setFixedSize(500, 600)
        self.grid.addWidget(self.labelImg, 0, 0, cnt_row, 1)
        self.label_id_user = QLabel("ID", self)
        self.label_id_user.setFixedWidth(90)
        self.label_id_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_id_user, 0, 1)
        self.text_id_user = QLineEdit()
        self.grid.addWidget(self.text_id_user, 0, 2)
        self.label_name_user = QLabel("이름", self)
        self.label_name_user.setFixedWidth(90)
        self.label_name_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_name_user, 0, 3)
        self.text_name_user = QLineEdit()
        self.grid.addWidget(self.text_name_user, 0, 4)
        self.label_licen_user = QLabel("자격증", self)
        self.label_licen_user.setFixedWidth(90)
        self.label_licen_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_licen_user, 0, 5)
        self.text_licen_user = QLineEdit()
        self.grid.addWidget(self.text_licen_user, 0, 6)

        self.label_clsN_user = QLabel("기수", self)
        self.label_clsN_user.setFixedWidth(90)
        self.label_clsN_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_clsN_user, 1, 1)
        self.text_clsN_user = QLineEdit()
        self.grid.addWidget(self.text_clsN_user, 1, 2)
        self.label_clsT_user = QLabel("반", self)
        self.label_clsT_user.setFixedWidth(90)
        self.label_clsT_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_clsT_user, 1, 3)
        self.text_clsT_user = QLineEdit()
        self.grid.addWidget(self.text_clsT_user, 1, 4)
        self.label_temp = QLabel("대체실습", self)
        self.label_temp.setFixedWidth(90)
        self.label_temp.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_temp, 1, 5)
        self.text_temp = QLineEdit()
        self.grid.addWidget(self.text_temp, 1, 6)

        self.label_RRN = QLabel("주민등록번호", self)
        self.label_RRN.setFixedWidth(90)
        self.label_RRN.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_RRN, 2, 1)
        self.text_RRN = QLineEdit()
        self.grid.addWidget(self.text_RRN, 2, 2, 1, 2)
        self.label_phone = QLabel("전화번호", self)
        self.label_phone.setFixedWidth(90)
        self.label_phone.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_phone, 2, 4)
        self.text_phone = QLineEdit()
        self.grid.addWidget(self.text_phone, 2, 5, 1, 2)
        
        
        self.label_adr = QLabel("주소", self)
        self.label_adr.setFixedWidth(90)
        self.label_adr.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_adr, 3, 1)
        self.text_adr = QLineEdit()
        self.grid.addWidget(self.text_adr, 3, 2, 1, 5)
        self.label_origin_adr = QLabel("본적주소", self)
        self.label_origin_adr.setFixedWidth(90)
        self.label_origin_adr.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid.addWidget(self.label_origin_adr, 4, 1)
        self.text_origin_adr = QLineEdit()
        self.grid.addWidget(self.text_origin_adr, 4, 2, 1, 5)

        self.btn_insert = QPushButton("Insert", self)
        self.btn_insert.clicked.connect(self.scanner)
        self.btn_cancel = QPushButton("Close", self)
        self.btn_cancel.clicked.connect(self.close)

        self.grid.addWidget(self.btn_insert, cnt_row, cnt_col - 2)
        self.grid.addWidget(self.btn_cancel, cnt_row, cnt_col - 1)

    def refreshUI(self):
        print("self.file_list")
        print(self.file_list)

        file_name = self.file_list[self.file_index]
        pixmap = QPixmap(file_name)
        pixmap = pixmap.scaledToWidth(500)

        self.labelImg.setPixmap(QPixmap(pixmap))
        self.text_id_user.clear()
        self.text_name_user.clear()
        self.text_licen_user.clear()
        self.text_clsN_user.clear()
        self.text_clsT_user.clear()
        self.text_temp.clear()
        self.text_RRN.clear()
        self.text_phone.clear()
        self.text_adr.clear()
        self.text_origin_adr.clear()

        doc_type = "주민등록등본"
        name = "name"
        adr = "주소"
        origin_adr = "본적주소"

        self.text_name_user.setText(name)
        self.text_adr.setText(adr)
        self.text_origin_adr.setText(origin_adr)

        print("self.text_id_user.text()")
        print("\"" + self.text_id_user.text() + "\"")
        print(type(self.text_id_user.text()))
        print("self.text_name_user.text()")
        print("\"" + self.text_name_user.text() + "\"")
        print(type(self.text_name_user.text()))
        print("self.text_licen_user.text()")
        print("\"" + self.text_licen_user.text() + "\"")
        print(type(self.text_licen_user.text()))
        print("self.text_clsN_user.text()")
        print("\"" + self.text_clsN_user.text() + "\"")
        print(type(self.text_clsN_user.text()))
        print("self.text_clsT_user.text()")
        print("\"" + self.text_clsT_user.text() + "\"")
        print(type(self.text_clsT_user.text()))
        print("self.text_temp.text()")
        print("\"" + self.text_temp.text() + "\"")
        print(type(self.text_temp.text()))
        print("self.text_RRN.text()")
        print("\"" + self.text_RRN.text() + "\"")
        print(type(self.text_RRN.text()))
        print("self.text_phone.text()")
        print("\"" + self.text_phone.text() + "\"")
        print(type(self.text_phone.text()))
        print("self.text_adr.text()")
        print("\"" + self.text_adr.text() + "\"")
        print(type(self.text_adr.text()))
        print("self.text_origin_adr.text()")
        print("\"" + self.text_origin_adr.text() + "\"")
        print(type(self.text_origin_adr.text()))

    def scanner(self):
        rs = db.main.dbPrograms.SELECT("*", "user", "name='' and RRN=''")
        print("rs")
        print("\"" + str(rs) + "\"")

        self.file_index += 1
        self.refreshUI()

    def showEvent(self, QShowEvent):
        self.file_index = 0
        self.refreshUI()
        return
        """
        doc_name, name, adr, origin_adr 받아서 text.setText 하기!
        """
        self.file = file_name
        img_origin = Image.open(r"C:\Users\David\Desktop\SKM_C364e21121319310_0002.jpg")
        # img_origin.show() file open
        print(img_origin.size)

        #((left, up, right, bottom))
        img_cropped = img_origin.crop((0, 580, 800, 700))
        # img_cropped.show()

        import pytesseract

        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

        image = img_cropped
        gibon = pytesseract.image_to_string(image, lang="kor", config="preserve_interword_spaces=1 --psm 4")
        print(gibon)
        str_arr = gibon.split(' ')
        print("print str_arr before")
        print(str_arr)
        res = []

        for string in str_arr:
            if '\n' in string:
                imsi = string.split('\n')
                for substr in imsi:
                    if substr != '':
                        res.append(substr)

            else:
                res.append(string)

        del res[0]
        del res[-1]
        print("res")
        print(res)

        

        

        

"""
* 일괄 변경 창 추가하기!
일괄 변경 창 클릭 -> 기수, 반 선택 후 바꿀 column 선택 -> 값 입렵 ==> 일괄변경 처리 !

"""
class batchUpdate(QWidget):
    global db

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("시험 회차 변경")
        self.setWindowIcon(QIcon("D:\\Master\\PythonWorkspace\\NYNOA\\Icons\\남양노아요양보호사.jpg"))

    def initUI(self):
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        box_top = QHBoxLayout()
        box_middle = QHBoxLayout()
        box_bottom = QHBoxLayout()

        self.box.addLayout(box_top)
        self.box.addLayout(box_middle)
        self.box.addLayout(box_bottom)
        
        self.label_N = QLabel("기수", self)
        self.label_T = QLabel("반", self)

        self.combobox_N = QComboBox(self)
        self.combobox_N.setFixedWidth(100)
        self.combobox_T = QComboBox(self)
        self.combobox_T.setFixedWidth(100)

        box_top.addWidget(self.label_N)
        box_top.addWidget(self.combobox_N)
        box_top.addWidget(self.label_T)
        box_top.addWidget(self.combobox_T)

        self.label_exam = QLabel("시험 회차")
        box_middle.addWidget(self.label_exam)
        self.text_exam = QLineEdit(self)
        box_middle.addWidget(self.text_exam)
        self.text_exam.returnPressed.connect(self.batch)

        self.btn_update = QPushButton("일괄 변경", self)
        self.btn_update.clicked.connect(self.batch)
        self.btn_cancel = QPushButton("취소", self)
        self.btn_cancel.clicked.connect(self.close)
        box_bottom.addStretch(1)
        box_bottom.addWidget(self.btn_update)
        box_bottom.addWidget(self.btn_cancel)

    def batch(self):
        if self.combobox_N.currentText() == "선택" or self.combobox_T.currentText() == "선택" or not(self.text_exam.text().isdigit()) or self.text_exam.text() == "":
            QMessageBox.warning(self, "오류", "입력값 오류")
            return

        query = "exam={}".format(self.text_exam.text())
        where = "classNumber='{}' and classTime='{}'".format(self.combobox_N.currentText(), self.combobox_T.currentText())

        db.main.dbPrograms.UPDATE("user", query, where)
        QMessageBox.about(self, "완료", "데이터를 성공적으로 수정했습니다.")
        db.main.showTable(Refresh=True)
        db.main.textInfo.clear()

    def showEvent(self, QShowEvent):
        self.combobox_N.clear()
        self.combobox_T.clear()
        self.text_exam.clear()
        self.class_num_list = []
        
        self.combobox_N.addItem("선택")
        self.combobox_T.addItem("선택")
        self.combobox_T.addItem("주간")
        self.combobox_T.addItem("야간")

        rs = db.main.dbPrograms.SELECT("classNumber, classTime", "lecture", orderBy="classNumber *1")
        if rs == "error":
            QMessageBox.information(self, "ERROR", "class batchUpdate returns error", QMessageBox.Yes, QMessageBox.Yes)
        else:
            for row in rs:
                if not row[0] in self.class_num_list:
                    self.class_num_list.append(row[0])
            
            self.combobox_N.addItems(self.class_num_list)

class UPDATE(QWidget):
    # 새 창을 띄우기 위해 서로 global로 연결
    global db

    def __init__(self):
        super().__init__()
        self.initUI()
        self.target_table = ""
        self.base_path = "D:\\남양노아요양보호사교육원\\교육생관리"
        self.setWindowIcon(QIcon("D:\\Master\\PythonWorkspace\\NYNOA\\Icons\\남양노아요양보호사.jpg"))

    def initUI(self):
        self.setWindowTitle("데이터 수정")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

    def generateDirectory(self, number, time, name):
        path = self.base_path + "\\{}\\{}{}".format(number, number, time)
        if not os.path.exists(path):
            os.makedirs(path)
        
        path = path + "\\{}".format(name)

        if not os.path.exists(path):
            os.makedirs(path)

    def moveDirectory(self, name, before_number, before_time, after_number, after_time):
        before_path = self.base_path + "\\{}\\{}{}\\{}".format(before_number, before_number, before_time, name)
        after_path = self.base_path + "\\{}\\{}{}".format(after_number, after_number, after_time)

        if not os.path.exists(after_path):
            os.makedirs(after_path)

        if os.path.exists(before_path):
            shutil.move(before_path, after_path)

        else:
            if not os.path.exists(after_path):
                self.generateDirectory(after_number, after_time, name)

    def dataUpdate(self):
        if self.target_table == "user":
            if self.text_id_user.text().strip() == "" or self.text_name_user.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return
            
            user_list = []
            user_list.append(self.text_id_user.text().strip())
            user_list.append(self.text_name_user.text().strip())
            user_list.append(self.text_RRN.text().strip())
            user_list.append(self.text_phone.text().strip())
            user_list.append(self.text_licen_user.text().strip())
            user_list.append(self.text_adr.text().strip())
            user_list.append(self.text_origin_adr.text().strip())
            user_list.append(self.text_clsN_user.text().strip())
            user_list.append(self.text_clsT_user.text().strip())
            # 총 이수, 이론, 실기, 실습 시간으로 NULL값 추가
            try:
                total_Hour = str(int(self.text_theory_time.text().strip()) + int(self.text_practice_time.text().strip()) + int(self.text_training_time.text().strip()))
            except:
                total_Hour = NULL
            user_list.append(total_Hour)
            user_list.append(self.text_theory_time.text().strip())
            user_list.append(self.text_practice_time.text().strip())
            user_list.append(self.text_training_time.text().strip())
            user_list.append(self.text_temp.text().strip())
            user_list.append(self.text_exam.text().strip())

            query_list = ["id", "name", "RRN", "phoneNumber", "license", "address", "originAddress", "classNumber", "classTime", \
                "totalCreditHour", "theoryCreditHour", "practicalCreditHour", "trainingCreditHour", "temporaryClassNumber", "exam"]

            where = "id = '{}' and name = '{}'".format(self.key_dict["ID"], self.key_dict["name"])
            query = ""
            for i in range(len(user_list)):
                query += query_list[i] + "="

                # 값이 없거나 NULL값인 경우는 그냥('없이) query문에 들어가고, 아닌 경우는 '를 붙혀서 query문에 넣는다!
                if user_list[i] == "" or user_list[i] == NULL:
                    user_list[i] = NULL
                    query += user_list[i]

                else:
                    query += "'" + user_list[i] + "'"

                if i != len(user_list) - 1:
                    query += ", "
            
            ask = "ID: {}\t이름: {}\t주민등록번호: {}\n전화번호: {}\t자격증: {}\n주소: {}\n본적주소: {}\n기수: {}\t반: {}\t 대체실습: {}\n총 이수시간: {}\t이론이수: {}\t실습이수: {}\t실기이수: {}\n시험회차: {}회"\
                .format(user_list[0], user_list[1], user_list[2], user_list[3], user_list[4], user_list[5], user_list[6], user_list[7], user_list[8], user_list[13], user_list[9], user_list[10], user_list[11], user_list[12], user_list[14])
            ask += "\n해당 정보로 업데이트합니다."
                
        elif self.target_table == "lecture":
            if self.text_clsN_lecture.text().strip() == "" or self.text_clsT_lecture.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 반을 입력해야 합니다!")
                return

            lect_list = []
            lect_list.append(self.text_clsN_lecture.text().strip())
            lect_list.append(self.text_clsT_lecture.text().strip())
            lect_list.append(self.text_startD_lecture.text().strip())
            lect_list.append(self.text_endD_lecture.text().strip())

            query_list = ["classNumber", "classTime", "startDate", "endDate"]

            where = "classNumber = '{}' and classTime = '{}'".format(self.key_dict["기수"], self.key_dict["반"])

            query = ""
            for i in range(len(lect_list)):
                query += query_list[i] + "="

                if lect_list[i] == "" or lect_list[i] == NULL:
                    lect_list[i] = NULL
                    query += lect_list[i]

                else:
                    query += "'" + lect_list[i] + "'"

                if i != len(lect_list) - 1:
                    query += ", "

            ask = "기수: {}\t반: {}\n시작일: {}\n종료일: {}\n".format(lect_list[0], lect_list[1], lect_list[2], lect_list[3])
            ask += "\n해당 정보로 업데이트합니다."

        elif self.target_table == "teacher":
            if self.text_id_teacher.text().strip() == "" or self.text_name_teacher.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return
            
            teach_list = []
            teach_list.append(self.text_id_teacher.text().strip())
            teach_list.append(self.text_category.text().strip())
            teach_list.append(self.text_name_teacher.text().strip())
            teach_list.append(self.text_DOB.text().strip())
            teach_list.append(self.text_licen_teacher.text().strip())
            teach_list.append(self.text_min_career.text().strip())
            teach_list.append(self.text_ACK.text().strip())

            query_list = ["id", "category", "name", "dateOfBirth", "license", "minCareer", "ACKDate"]

            where = "id = '{}' and name = '{}'".format(self.key_dict["ID"], self.key_dict["name"])

            query = ""
            for i in range(len(teach_list)):
                query += query_list[i] + "="

                if teach_list[i] == "" or teach_list[i] == NULL:
                    teach_list[i] = NULL
                    query += teach_list[i]

                else:
                    query += "'" + teach_list[i] + "'"

                if i != len(teach_list) - 1:
                    query += ", "

            ask = "ID: {}\t이름: {}\t자격증: {}\n생년월일: {}\t구분: {}\n최소경력: {}\n도 승인일자: {}\n"\
                .format(teach_list[0], teach_list[1], teach_list[2], teach_list[3], teach_list[4], teach_list[5], teach_list[6])
            ask += "\n해당 정보로 업데이트합니다."

        elif self.target_table == "temptraining":
            if self.text_clsN_temp_training.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수를 입력해야 합니다!")
                return

            temp_list = []
            temp_list.append(self.text_clsN_temp_training.text().strip())
            temp_list.append(self.text_startD_temp_training.text().strip())
            temp_list.append(self.text_endD_temp_training.text().strip())
            temp_list.append(self.text_awardD.text().strip())

            query_list = ["classNumber", "startDate", "endDate", "awardDate"]

            where = "classNumber = '{}'".format(self.key_dict["기수"])

            query = ""
            for i in range(len(temp_list)):
                query += query_list[i] + "="

                if temp_list[i] == "" or temp_list[i] == NULL:
                    temp_list[i] = NULL
                    query += temp_list[i]

                else:
                    query += "'" + temp_list[i] + "'"

                if i != len(temp_list) - 1:
                    query += ", "

            ask = "기수: {}\n시작일: {}\n종료일: {}\n수여일: {}\n".format(temp_list[0], temp_list[1], temp_list[2], temp_list[3])
            ask += "\n해당 정보로 업데이트합니다."

        elif self.target_table == "temptrainingteacher":
            if self.text_clsN_temp_training_teacher.text().strip() == "" or self.text_teacher.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 담당강사를 입력해야 합니다!")
                return

            temp_training_teacher_list = []
            temp_training_teacher_list.append(self.text_clsN_temp_training_teacher.text().strip())
            temp_training_teacher_list.append(self.text_teacher.text().strip())

            query_list = ["classNumber", "teacherName"]

            where = "classNumber = '{}' and teacherName = '{}'".format(self.key_dict["기수"], self.key_dict["강사"])

            query = ""
            for i in range(len(temp_training_teacher_list)):
                query += query_list[i] + "="
                if temp_training_teacher_list[i] == "" or temp_training_teacher_list[i] == NULL:
                    temp_training_teacher_list[i] = NULL
                    query += temp_training_teacher_list[i]

                else:
                    query += "'" + temp_training_teacher_list[i] + "'"

                if i != len(temp_training_teacher_list) - 1:
                    query += ", "

            ask = "기수: {}\n강사: {}\n".format(temp_training_teacher_list[0], temp_training_teacher_list[1])
            ask += "\n해당 정보로 업데이트합니다."

        ans = QMessageBox.question(self, "데이터 수정 확인", ask, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            db.main.dbPrograms.UPDATE(self.target_table, query, where)
            QMessageBox.about(self, "완료", "데이터를 성공적으로 수정했습니다.")
            db.main.showTable(Refresh=True)
            db.main.textInfo.clear()

            if self.target_table == "user":
                name = self.text_name_user.text().strip()
                number = self.text_clsN_user.text().strip()
                time = self.text_clsT_user.text().strip()

                if not (self.key_dict["기수"] == number and self.key_dict["반"] == time):
                    if not (number == "" or time == ""):
                        if (self.key_dict["기수"] == "" or self.key_dict["반"] == ""):
                            self.generateDirectory(number, time, name)
                        elif (self.key_dict["기수"] != "" and self.key_dict["반"] != ""):
                            self.moveDirectory(name, self.key_dict["기수"], self.key_dict["반"], number, time)
            self.close()
        else:
            pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        
        elif e.key() == Qt.Key_Enter:
            self.dataUpdate()

    def showEvent(self, QShowEvent):
        self.key_dict = {}
        cnt_row = 0
        cnt_col = 0
        # 1. 기존에 있던 label과 Line Edit 삭제
        for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().deleteLater()
                # self.grid.itemAt(i).widget().hide()

        # 2. 공통으로 들어갈 insert 버튼과 close 버튼 생성
        self.btn_update = QPushButton("Update", self)
        self.btn_update.clicked.connect(self.dataUpdate)
        self.btn_cancel = QPushButton("Close", self)
        self.btn_cancel.clicked.connect(self.close)
        
        # 3. 현재 테이블에 맞는 label 및 Line Edit 생성 및 추가
        if db.main.current_table == "user":
            self.target_table = "user"
            self.setWindowTitle("데이터 수정 - 수강생")
            cnt_row = 7
            cnt_col = 6
            self.resize(600, 400)

            self.label_id_user = QLabel("ID", self)
            self.label_id_user.setFixedWidth(90)
            self.label_id_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_id_user, 0, 0)
            self.text_id_user = QLineEdit()
            self.grid.addWidget(self.text_id_user, 0, 1)
            self.label_name_user = QLabel("이름", self)
            self.label_name_user.setFixedWidth(90)
            self.label_name_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_name_user, 0, 2)
            self.text_name_user = QLineEdit()
            self.grid.addWidget(self.text_name_user, 0, 3)
            self.label_licen_user = QLabel("자격증", self)
            self.label_licen_user.setFixedWidth(90)
            self.label_licen_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_licen_user, 0, 4)
            self.text_licen_user = QLineEdit()
            self.grid.addWidget(self.text_licen_user, 0, 5)

            self.label_clsN_user = QLabel("기수", self)
            self.label_clsN_user.setFixedWidth(90)
            self.label_clsN_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_user, 1, 0)
            self.text_clsN_user = QLineEdit()
            self.grid.addWidget(self.text_clsN_user, 1, 1)
            self.label_clsT_user = QLabel("반", self)
            self.label_clsT_user.setFixedWidth(90)
            self.label_clsT_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsT_user, 1, 2)
            self.text_clsT_user = QLineEdit()
            self.grid.addWidget(self.text_clsT_user, 1, 3)
            self.label_temp = QLabel("대체실습", self)
            self.label_temp.setFixedWidth(90)
            self.label_temp.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_temp, 1, 4)
            self.text_temp = QLineEdit()
            self.grid.addWidget(self.text_temp, 1, 5)

            self.label_RRN = QLabel("주민등록번호", self)
            self.label_RRN.setFixedWidth(90)
            self.label_RRN.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_RRN, 2, 0)
            self.text_RRN = QLineEdit()
            self.grid.addWidget(self.text_RRN, 2, 1, 1, 2)
            self.label_phone = QLabel("전화번호", self)
            self.label_phone.setFixedWidth(90)
            self.label_phone.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_phone, 2, 3)
            self.text_phone = QLineEdit()
            self.grid.addWidget(self.text_phone, 2, 4, 1, 2)
            
            
            self.label_adr = QLabel("주소", self)
            self.label_adr.setFixedWidth(90)
            self.label_adr.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_adr, 3, 0)
            self.text_adr = QLineEdit()
            self.grid.addWidget(self.text_adr, 3, 1, 1, 5)
            self.label_origin_adr = QLabel("본적주소", self)
            self.label_origin_adr.setFixedWidth(90)
            self.label_origin_adr.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_origin_adr, 4, 0)
            self.text_origin_adr = QLineEdit()
            self.grid.addWidget(self.text_origin_adr, 4, 1, 1, 5)

            self.label_total_time = QLabel("총 이수시간은 이론 + 실기 + 실습 이수시간으로 입력됩니다.")
            self.grid.addWidget(self.label_total_time, 5, 0, 1, 6)

            self.label_theory_time = QLabel("이론이수")
            self.label_theory_time.setFixedWidth(90)
            self.label_theory_time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_theory_time, 6, 0)
            self.text_theory_time = QLineEdit()
            self.grid.addWidget(self.text_theory_time, 6, 1)

            self.label_practice_time = QLabel("실기이수")
            self.label_practice_time.setFixedWidth(90)
            self.label_practice_time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_practice_time, 6, 2)
            self.text_practice_time = QLineEdit()
            self.grid.addWidget(self.text_practice_time, 6, 3)

            self.label_training_time = QLabel("실습이수")
            self.label_training_time.setFixedWidth(90)
            self.label_training_time.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_training_time, 6, 4)
            self.text_training_time = QLineEdit()
            self.grid.addWidget(self.text_training_time, 6, 5)

            self.label_exam = QLabel("시험회차")
            self.label_exam.setFixedWidth(90)
            self.label_exam.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_exam, 7, 0)
            self.text_exam = QLineEdit()
            self.grid.addWidget(self.text_exam, 7, 1)

            input_user = []
            for i in range(15):
                input_user.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_user[i] == "NULL":
                    input_user[i] = ""

            self.text_id_user.setText(str(input_user[0]))
            self.text_name_user.setText(str(input_user[1]))
            self.text_licen_user.setText(str(input_user[4]))
            self.text_clsN_user.setText(str(input_user[7]))
            self.text_clsT_user.setText(str(input_user[8]))
            self.text_temp.setText(str(input_user[13]))
            self.text_RRN.setText(str(input_user[2]))
            self.text_phone.setText(str(input_user[3]))
            self.text_adr.setText(str(input_user[5]))
            self.text_origin_adr.setText(str(input_user[6]))
            self.text_theory_time.setText(str(input_user[10]))
            self.text_practice_time.setText(str(input_user[11]))
            self.text_training_time.setText(str(input_user[12]))
            self.text_exam.setText(str(input_user[14]))

            self.key_dict["ID"] = str(input_user[0])
            self.key_dict["name"] = str(input_user[1])
            self.key_dict["기수"] = str(input_user[7])
            self.key_dict["반"] = str(input_user[8])
            self.key_dict["자격증"] = str(input_user[4])

        elif db.main.current_table == "lecture":
            self.target_table = "lecture"
            self.setWindowTitle("데이터 수정 - 기수")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.label_clsN_lecture = QLabel("기수", self)
            self.label_clsN_lecture.setFixedWidth(90)
            self.label_clsN_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_lecture, 0, 0)
            self.text_clsN_lecture = QLineEdit()
            self.text_clsN_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_clsN_lecture, 0, 1)
            self.label_clsT_lecture = QLabel("반", self)
            self.label_clsT_lecture.setFixedWidth(90)
            self.label_clsT_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsT_lecture, 0, 2)
            self.text_clsT_lecture = QLineEdit()
            self.text_clsT_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_clsT_lecture, 0, 3)
            self.label_startD_lecture = QLabel("시작일", self)
            self.label_startD_lecture.setFixedWidth(90)
            self.label_startD_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_startD_lecture, 1, 0)
            self.text_startD_lecture = QLineEdit()
            self.text_startD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_startD_lecture, 1, 1)
            self.label_endD_lecture = QLabel("종료일", self)
            self.label_endD_lecture.setFixedWidth(90)
            self.label_endD_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_endD_lecture, 1, 2)
            self.text_endD_lecture = QLineEdit()
            self.text_endD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_endD_lecture, 1, 3)

            input_lecture = []
            for i in range(4):
                input_lecture.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_lecture[i] == "NULL":
                    input_lecture[i] = ""

            self.text_clsN_lecture.setText(str(input_lecture[0]))
            self.text_clsT_lecture.setText(str(input_lecture[1]))
            self.text_startD_lecture.setText(str(input_lecture[2]))
            self.text_endD_lecture.setText(str(input_lecture[3]))

            self.key_dict["기수"] = str(input_lecture[0])
            self.key_dict["반"] = str(input_lecture[1])

        elif db.main.current_table == "teacher":
            self.target_table = "teacher"
            self.setWindowTitle("데이터 수정 - 강사")
            cnt_row = 3
            cnt_col = 6
            self.resize(400, 200)
            self.label_id_teacher = QLabel("ID", self)
            self.label_id_teacher.setFixedWidth(90)
            self.label_id_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_id_teacher, 0, 0)
            self.text_id_teacher = QLineEdit()
            self.grid.addWidget(self.text_id_teacher, 0, 1)
            self.label_name_teacher = QLabel("이름", self)
            self.label_name_teacher.setFixedWidth(90)
            self.label_name_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_name_teacher, 0, 2)
            self.text_name_teacher = QLineEdit()
            self.grid.addWidget(self.text_name_teacher, 0, 3)
            self.label_licen_teacher = QLabel("자격증", self)
            self.label_licen_teacher.setFixedWidth(90)
            self.label_licen_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_licen_teacher, 0, 4)
            self.text_licen_teacher = QLineEdit()
            self.grid.addWidget(self.text_licen_teacher, 0, 5)
            self.label_DOB = QLabel("생년월일", self)
            self.label_DOB.setFixedWidth(90)
            self.label_DOB.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_DOB, 1, 0)
            self.text_DOB = QLineEdit()
            self.grid.addWidget(self.text_DOB, 1, 1, 1, 2)
            self.label_category = QLabel("전임/외래", self)
            self.label_category.setFixedWidth(90)
            self.label_category.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_category, 1, 3)
            self.text_category = QLineEdit()
            self.grid.addWidget(self.text_category, 1, 4, 1, 2)
            self.label_min_career = QLabel("최소경력", self)
            self.label_min_career.setFixedWidth(90)
            self.label_min_career.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_min_career, 2, 0)
            self.text_min_career = QLineEdit()
            self.grid.addWidget(self.text_min_career, 2, 1, 1, 2)
            self.label_ACK = QLabel("도 승인일자")
            self.label_ACK.setFixedWidth(90)
            self.label_ACK.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_ACK, 2, 3)
            self.text_ACK = QLineEdit()
            self.grid.addWidget(self.text_ACK, 2, 4, 1, 2)

            input_teacher = []
            for i in range(7):
                input_teacher.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_teacher[i] == "NULL":
                    input_teacher[i] = ""

            self.text_id_teacher.setText(str(input_teacher[0]))
            self.text_name_teacher.setText(str(input_teacher[2]))
            self.text_licen_teacher.setText(str(input_teacher[4]))
            self.text_DOB.setText(str(input_teacher[3]))
            self.text_category.setText(str(input_teacher[1]))
            self.text_min_career.setText(str(input_teacher[5]))
            self.text_ACK.setText(str(input_teacher[6]))

            self.key_dict["ID"] = str(input_teacher[0])
            self.key_dict["name"] = str(input_teacher[2])

        elif db.main.current_table == "temptraining":
            self.target_table = "temptraining"
            self.setWindowTitle("데이터 수정 - 대체실습")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.label_clsN_temp_training = QLabel("기수", self)
            self.label_clsN_temp_training.setFixedWidth(90)
            self.label_clsN_temp_training.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_temp_training, 0, 0)
            self.text_clsN_temp_training = QLineEdit()
            self.text_clsN_temp_training.setFixedWidth(120)
            self.grid.addWidget(self.text_clsN_temp_training, 0, 1)
            self.label_startD_temp_training = QLabel("시작일", self)
            self.label_startD_temp_training.setFixedWidth(90)
            self.label_startD_temp_training.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_startD_temp_training, 0, 2)
            self.text_startD_temp_training = QLineEdit()
            self.text_startD_temp_training.setFixedWidth(120)
            self.grid.addWidget(self.text_startD_temp_training, 0, 3)
            self.label_endD_temp_training = QLabel("종료일", self)
            self.label_endD_temp_training.setFixedWidth(90)
            self.label_endD_temp_training.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_endD_temp_training, 1, 0)
            self.text_endD_temp_training = QLineEdit()
            self.text_endD_temp_training.setFixedWidth(120)
            self.grid.addWidget(self.text_endD_temp_training, 1, 1)
            self.label_awardD = QLabel("수여일", self)
            self.label_awardD.setFixedWidth(90)
            self.label_awardD.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_awardD, 1, 2)
            self.text_awardD = QLineEdit()
            self.text_awardD.setFixedWidth(120)
            self.grid.addWidget(self.text_awardD, 1, 3)

            input_temp_training = []
            for i in range(4):
                input_temp_training.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_temp_training[i] == "NULL":
                    input_temp_training[i] = ""

            self.text_clsN_temp_training.setText(str(input_temp_training[0]))
            self.text_startD_temp_training.setText(str(input_temp_training[1]))
            self.text_endD_temp_training.setText(str(input_temp_training[2]))
            self.text_awardD.setText(str(input_temp_training[3]))

            self.key_dict["기수"] = str(input_temp_training[0])

        elif db.main.current_table == "temptrainingteacher":
            self.target_table = "temptrainingteacher"
            self.setWindowTitle("데이터 수정 - 대체실습 강사")
            cnt_row = 2
            cnt_col = 2
            self.resize(300, 200)
            self.label_clsN_temp_training_teacher = QLabel("기수", self)
            self.label_clsN_temp_training_teacher.setFixedWidth(90)
            self.label_clsN_temp_training_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_temp_training_teacher, 0, 0)
            self.text_clsN_temp_training_teacher = QLineEdit()
            self.text_clsN_temp_training_teacher.setFixedWidth(90)
            self.grid.addWidget(self.text_clsN_temp_training_teacher, 0, 1)
            self.label_teacher = QLabel("강사", self)
            self.label_teacher.setFixedWidth(90)
            self.label_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_teacher, 1, 0)
            self.text_teacher = QLineEdit()
            self.text_teacher.setFixedWidth(90)
            self.grid.addWidget(self.text_teacher, 1, 1)

            input_temp_training_teacher = []
            for i in range(2):
                input_temp_training_teacher.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())
                
                if input_temp_training_teacher[i] == "NULL":
                    input_temp_training_teacher[i] = ""

            self.text_clsN_temp_training_teacher.setText(str(input_temp_training_teacher[0]))
            self.text_teacher.setText(str(input_temp_training_teacher[1]))

            self.key_dict["기수"] = str(input_temp_training_teacher[0])
            self.key_dict["강사"] = str(input_temp_training_teacher[1])
        
        # 4. 재생성된 버튼 추가
        self.grid.addWidget(self.btn_update, cnt_row, cnt_col - 2)
        self.grid.addWidget(self.btn_cancel, cnt_row, cnt_col - 1)


class INSERT(QWidget):
    # 새 창을 띄우기 위해 서로 global로 연결
    global db

    def __init__(self):
        super().__init__()
        self.initUI()
        self.target_table = ""
        self.base_path = "D:\\남양노아요양보호사교육원\\교육생관리"
        self.setWindowIcon(QIcon("D:\\Master\\PythonWorkspace\\NYNOA\\Icons\\남양노아요양보호사.jpg"))

    def initUI(self):
        self.setWindowTitle("데이터 삽입")

        # 총 이수, 이론 이수, 실기, 실습 이수시간은 삽입에서 넣지 않고, NULL값을 일단 너놓자! Update에서 구현하기
        # self.labelTotalH = QLabel("총 이수시간", self)
        # grid.addWidget(self.labelTotalH, 9, 0)
        # self.textTotalH = QLineEdit()
        # grid.addWidget(self.textTotalH, 9, 1)

        # btn = QPushButton("수강생 관리", self)
        # btn.resize(btn.sizeHint())
        # btn.move(50, 50)
        # btn.clicked.connect(QCoreApplication.instance().quit)

        self.grid = QGridLayout()
        self.setLayout(self.grid)

    def generateDirectory(self, number, time, name):
        path = self.base_path + "\\{}\\{}{}".format(number, number, time)
        if not os.path.exists(path):
            os.makedirs(path)
        
        path = path + "\\{}".format(name)

        if not os.path.exists(path):
            os.makedirs(path)

    def dataInsert(self):
        if self.target_table == "user":
            if self.text_id_user.text().strip() == "" or self.text_name_user.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return

            user_list = []
            user_list.append(self.text_id_user.text().strip())
            user_list.append(self.text_name_user.text().strip())
            user_list.append(self.text_RRN.text().strip())
            user_list.append(self.text_phone.text().strip())
            user_list.append(self.text_licen_user.text().strip())
            user_list.append(self.text_adr.text().strip())
            user_list.append(self.text_origin_adr.text().strip())
            user_list.append(self.text_clsN_user.text().strip())
            user_list.append(self.text_clsT_user.text().strip())
            # 총 이수, 이론, 실기, 실습 시간으로 NULL값 추가
            user_list.append(NULL)
            user_list.append(NULL)
            user_list.append(NULL)
            user_list.append(NULL)
            user_list.append(self.text_temp.text().strip())
            # 시험 회차 정보는 데이터 수정에서 입력
            user_list.append(NULL)

            query = ""
            for i in range(len(user_list)):
                # 값이 없거나 NULL값인 경우는 그냥('없이) query문에 들어가고, 아닌 경우는 '를 붙혀서 query문에 넣는다!
                if user_list[i] == "" or user_list[i] == NULL:
                    user_list[i] = NULL
                    query += user_list[i]

                else:
                    query += "'" + user_list[i] + "'"

                if i != len(user_list) - 1:
                    query += ", "
            
            ask = "ID: {}\t이름: {}\t주민등록번호: {}\n전화번호: {}\t자격증: {}\n주소: {}\n본적주소: {}\n기수: {}\t반: {}\t 대체실습: {}\n총 이수시간: {}\t이론이수: {}\t실습이수: {}\t 실기이수: {}\n"\
                .format(user_list[0], user_list[1], user_list[2], user_list[3], user_list[4], user_list[5], user_list[6], user_list[7], user_list[8], user_list[13], user_list[9], user_list[10], user_list[11], user_list[12])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."
                
        elif self.target_table == "lecture":
            if self.text_clsN_lecture.text().strip() == "" or self.text_clsT_lecture.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 반을 입력해야 합니다!")
                return

            lect_list = []
            lect_list.append(self.text_clsN_lecture.text().strip())
            lect_list.append(self.text_clsT_lecture.text().strip())
            lect_list.append(self.text_startD_lecture.text().strip())
            lect_list.append(self.text_endD_lecture.text().strip())

            query = ""
            for i in range(len(lect_list)):
                if lect_list[i] == "" or lect_list[i] == NULL:
                    lect_list[i] = NULL
                    query += lect_list[i]

                else:
                    query += "'" + lect_list[i] + "'"

                if i != len(lect_list) - 1:
                    query += ", "

            ask = "기수: {}\t반: {}\n시작일: {}\n종료일: {}\n".format(lect_list[0], lect_list[1], lect_list[2], lect_list[3])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."

        elif self.target_table == "teacher":
            if self.text_id_teacher.text().strip() == "" or self.text_name_teacher.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return
            
            teach_list = []
            teach_list.append(self.text_id_teacher.text().strip())
            teach_list.append(self.text_category.text().strip())
            teach_list.append(self.text_name_teacher.text().strip())
            teach_list.append(self.text_DOB.text().strip())
            teach_list.append(self.text_licen_teacher.text().strip())
            teach_list.append(self.text_min_career.text().strip())
            teach_list.append(self.text_ACK.text().strip())

            query = ""
            for i in range(len(teach_list)):
                if teach_list[i] == "" or teach_list[i] == NULL:
                    teach_list[i] = NULL
                    query += teach_list[i]

                else:
                    query += "'" + teach_list[i] + "'"

                if i != len(teach_list) - 1:
                    query += ", "

            ask = "ID: {}\t이름: {}\t자격증: {}\n생년월일: {}\t구분: {}\n최소경력: {}\n도 승인일자: {}\n"\
                .format(teach_list[0], teach_list[1], teach_list[2], teach_list[3], teach_list[4], teach_list[5], teach_list[6])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."

        elif self.target_table == "temptraining":
            if self.text_clsN_temp_training.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수를 입력해야 합니다!")
                return

            temp_list = []
            temp_list.append(self.text_clsN_temp_training.text().strip())
            temp_list.append(self.text_startD_temp_training.text().strip())
            temp_list.append(self.text_endD_temp_training.text().strip())
            temp_list.append(self.text_awardD.text().strip())

            query = ""
            for i in range(len(temp_list)):
                if temp_list[i] == "" or temp_list[i] == NULL:
                    temp_list[i] = NULL
                    query += temp_list[i]

                else:
                    query += "'" + temp_list[i] + "'"

                if i != len(temp_list) - 1:
                    query += ", "

            ask = "기수: {}\n시작일: {}\n종료일: {}\n수여일: {}\n".format(temp_list[0], temp_list[1], temp_list[2], temp_list[3])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."

        elif self.target_table == "temptrainingteacher":
            if self.text_clsN_temp_training_teacher.text().strip() == "" or self.text_teacher.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 담당강사를 입력해야 합니다!")
                return

            temp_training_teacher_list = []
            temp_training_teacher_list.append(self.text_clsN_temp_training_teacher.text().strip())
            temp_training_teacher_list.append(self.text_teacher.text().strip())

            query = ""
            for i in range(len(temp_training_teacher_list)):
                if temp_training_teacher_list[i] == "" or temp_training_teacher_list[i] == NULL:
                    temp_training_teacher_list[i] = NULL
                    query += temp_training_teacher_list[i]

                else:
                    query += "'" + temp_training_teacher_list[i] + "'"

                if i != len(temp_training_teacher_list) - 1:
                    query += ", "

            ask = "기수: {}\n강사: {}\n".format(temp_training_teacher_list[0], temp_training_teacher_list[1])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."


        ans = QMessageBox.question(self, "데이터 삽입 확인", ask, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            db.main.dbPrograms.INSERT(self.target_table, query)
            QMessageBox.about(self, "완료", "데이터를 성공적으로 추가했습니다.")
            if self.target_table == "user":
                name = self.text_name_user.text().strip()
                number = self.text_clsN_user.text().strip()
                time = self.text_clsT_user.text().strip()

                if not (number == "" or time == ""):
                    self.generateDirectory(number, time, name)

            db.main.showTable(Refresh=True)
            db.main.textInfo.clear()
            self.close()
        else:
            pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        
        elif e.key() == Qt.Key_Enter:
            self.dataInsert()

    def showEvent(self, QShowEvent):

        cnt_row = 0
        cnt_col = 0
        # 1. 기존에 있던 label과 Line Edit 삭제
        for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().deleteLater()
                # self.grid.itemAt(i).widget().hide()

        # 2. 공통으로 들어갈 insert 버튼과 close 버튼 생성
        self.btn_insert = QPushButton("Insert", self)
        self.btn_insert.clicked.connect(self.dataInsert)
        self.btn_cancel = QPushButton("Close", self)
        self.btn_cancel.clicked.connect(self.close)
        
        # 3. 현재 테이블에 맞는 label 및 Line Edit 생성 및 추가
        if db.main.current_table == "user":
            self.target_table = "user"
            self.setWindowTitle("데이터 삽입 - 수강생")
            cnt_row = 5
            cnt_col = 6
            self.resize(600, 400)

            self.label_id_user = QLabel("ID", self)
            self.label_id_user.setFixedWidth(90)
            self.label_id_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_id_user, 0, 0)
            self.text_id_user = QLineEdit()
            next_id = str(int(db.main.dbPrograms.SELECT("id", "user", orderBy="id desc limit 1")[0][0]) + 1)
            self.text_id_user.setText(next_id)
            self.grid.addWidget(self.text_id_user, 0, 1)
            self.label_name_user = QLabel("이름", self)
            self.label_name_user.setFixedWidth(90)
            self.label_name_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_name_user, 0, 2)
            self.text_name_user = QLineEdit()
            self.grid.addWidget(self.text_name_user, 0, 3)
            self.label_licen_user = QLabel("자격증", self)
            self.label_licen_user.setFixedWidth(90)
            self.label_licen_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_licen_user, 0, 4)
            self.text_licen_user = QLineEdit()
            self.grid.addWidget(self.text_licen_user, 0, 5)

            self.label_clsN_user = QLabel("기수", self)
            self.label_clsN_user.setFixedWidth(90)
            self.label_clsN_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_user, 1, 0)
            self.text_clsN_user = QLineEdit()
            self.grid.addWidget(self.text_clsN_user, 1, 1)
            self.label_clsT_user = QLabel("반", self)
            self.label_clsT_user.setFixedWidth(90)
            self.label_clsT_user.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsT_user, 1, 2)
            self.text_clsT_user = QLineEdit()
            self.grid.addWidget(self.text_clsT_user, 1, 3)
            self.label_temp = QLabel("대체실습", self)
            self.label_temp.setFixedWidth(90)
            self.label_temp.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_temp, 1, 4)
            self.text_temp = QLineEdit()
            self.grid.addWidget(self.text_temp, 1, 5)

            self.label_RRN = QLabel("주민등록번호", self)
            self.label_RRN.setFixedWidth(90)
            self.label_RRN.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_RRN, 2, 0)
            self.text_RRN = QLineEdit()
            self.grid.addWidget(self.text_RRN, 2, 1, 1, 2)
            self.label_phone = QLabel("전화번호", self)
            self.label_phone.setFixedWidth(90)
            self.label_phone.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_phone, 2, 3)
            self.text_phone = QLineEdit()
            self.grid.addWidget(self.text_phone, 2, 4, 1, 2)
            
            
            self.label_adr = QLabel("주소", self)
            self.label_adr.setFixedWidth(90)
            self.label_adr.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_adr, 3, 0)
            self.text_adr = QLineEdit()
            self.grid.addWidget(self.text_adr, 3, 1, 1, 5)
            self.label_origin_adr = QLabel("본적주소", self)
            self.label_origin_adr.setFixedWidth(90)
            self.label_origin_adr.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_origin_adr, 4, 0)
            self.text_origin_adr = QLineEdit()
            self.grid.addWidget(self.text_origin_adr, 4, 1, 1, 5)

            self.text_id_user.setFocus()

        elif db.main.current_table == "lecture":
            self.target_table = "lecture"
            self.setWindowTitle("데이터 삽입 - 기수")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.label_clsN_lecture = QLabel("기수", self)
            self.label_clsN_lecture.setFixedWidth(90)
            self.label_clsN_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_lecture, 0, 0)
            self.text_clsN_lecture = QLineEdit()
            self.text_clsN_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_clsN_lecture, 0, 1)
            self.label_clsT_lecture = QLabel("반", self)
            self.label_clsT_lecture.setFixedWidth(90)
            self.label_clsT_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsT_lecture, 0, 2)
            self.text_clsT_lecture = QLineEdit()
            self.text_clsT_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_clsT_lecture, 0, 3)
            self.label_startD_lecture = QLabel("시작일", self)
            self.label_startD_lecture.setFixedWidth(90)
            self.label_startD_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_startD_lecture, 1, 0)
            self.text_startD_lecture = QLineEdit()
            self.text_startD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_startD_lecture, 1, 1)
            self.label_endD_lecture = QLabel("종료일", self)
            self.label_endD_lecture.setFixedWidth(90)
            self.label_endD_lecture.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_endD_lecture, 1, 2)
            self.text_endD_lecture = QLineEdit()
            self.text_endD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.text_endD_lecture, 1, 3)

        elif db.main.current_table == "teacher":
            self.target_table = "teacher"
            self.setWindowTitle("데이터 삽입 - 강사")
            cnt_row = 3
            cnt_col = 6
            self.resize(400, 200)
            self.label_id_teacher = QLabel("ID", self)
            self.label_id_teacher.setFixedWidth(90)
            self.label_id_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_id_teacher, 0, 0)
            self.text_id_teacher = QLineEdit()
            next_id = str(int(db.main.dbPrograms.SELECT("id", "teacher", orderBy="id desc limit 1")[0][0]) + 1)
            self.text_id_teacher.setText(next_id)
            self.grid.addWidget(self.text_id_teacher, 0, 1)
            self.label_name_teacher = QLabel("이름", self)
            self.label_name_teacher.setFixedWidth(90)
            self.label_name_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_name_teacher, 0, 2)
            self.text_name_teacher = QLineEdit()
            self.grid.addWidget(self.text_name_teacher, 0, 3)
            self.label_licen_teacher = QLabel("자격증", self)
            self.label_licen_teacher.setFixedWidth(90)
            self.label_licen_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_licen_teacher, 0, 4)
            self.text_licen_teacher = QLineEdit()
            self.grid.addWidget(self.text_licen_teacher, 0, 5)
            self.label_DOB = QLabel("생년월일", self)
            self.label_DOB.setFixedWidth(90)
            self.label_DOB.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_DOB, 1, 0)
            self.text_DOB = QLineEdit()
            self.grid.addWidget(self.text_DOB, 1, 1, 1, 2)
            self.label_category = QLabel("전임/외래", self)
            self.label_category.setFixedWidth(90)
            self.label_category.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_category, 1, 3)
            self.text_category = QLineEdit()
            self.grid.addWidget(self.text_category, 1, 4, 1, 2)
            self.label_min_career = QLabel("최소경력", self)
            self.label_min_career.setFixedWidth(90)
            self.label_min_career.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_min_career, 2, 0)
            self.text_min_career = QLineEdit()
            self.grid.addWidget(self.text_min_career, 2, 1, 1, 2)
            self.label_ACK = QLabel("도 승인일자")
            self.label_ACK.setFixedWidth(90)
            self.label_ACK.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_ACK, 2, 3)
            self.text_ACK = QLineEdit()
            self.grid.addWidget(self.text_ACK, 2, 4, 1, 2)

        elif db.main.current_table == "temptraining":
            self.target_table = "temptraining"
            self.setWindowTitle("데이터 삽입 - 대체실습")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.label_clsN_temp_training = QLabel("기수", self)
            self.label_clsN_temp_training.setFixedWidth(90)
            self.label_clsN_temp_training.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_temp_training, 0, 0)
            self.text_clsN_temp_training = QLineEdit()
            self.text_clsN_temp_training.setFixedWidth(120)
            self.grid.addWidget(self.text_clsN_temp_training, 0, 1)
            self.label_startD_temp_training = QLabel("시작일", self)
            self.label_startD_temp_training.setFixedWidth(90)
            self.label_startD_temp_training.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_startD_temp_training, 0, 2)
            self.text_startD_temp_training = QLineEdit()
            self.text_startD_temp_training.setFixedWidth(120)
            self.grid.addWidget(self.text_startD_temp_training, 0, 3)
            self.label_endD_temp_training = QLabel("종료일", self)
            self.label_endD_temp_training.setFixedWidth(90)
            self.label_endD_temp_training.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_endD_temp_training, 1, 0)
            self.text_endD_temp_training = QLineEdit()
            self.text_endD_temp_training.setFixedWidth(120)
            self.grid.addWidget(self.text_endD_temp_training, 1, 1)
            self.label_awardD = QLabel("수여일", self)
            self.label_awardD.setFixedWidth(90)
            self.label_awardD.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_awardD, 1, 2)
            self.text_awardD = QLineEdit()
            self.text_awardD.setFixedWidth(120)
            self.grid.addWidget(self.text_awardD, 1, 3)
            
        elif db.main.current_table == "temptrainingteacher":
            self.target_table = "temptrainingteacher"
            self.setWindowTitle("데이터 삽입 - 대체실습 강사")
            cnt_row = 2
            cnt_col = 2
            self.resize(300, 200)
            self.label_clsN_temp_training_teacher = QLabel("기수", self)
            self.label_clsN_temp_training_teacher.setFixedWidth(90)
            self.label_clsN_temp_training_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_clsN_temp_training_teacher, 0, 0)
            self.text_clsN_temp_training_teacher = QLineEdit()
            self.text_clsN_temp_training_teacher.setFixedWidth(90)
            self.grid.addWidget(self.text_clsN_temp_training_teacher, 0, 1)
            self.label_teacher = QLabel("강사", self)
            self.label_teacher.setFixedWidth(90)
            self.label_teacher.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid.addWidget(self.label_teacher, 1, 0)
            self.text_teacher = QLineEdit()
            self.text_teacher.setFixedWidth(90)
            self.grid.addWidget(self.text_teacher, 1, 1)

        # 4. 버튼을 추가하기 위한 row와 column check
        # 이거 왜 자꾸 증가하냐;
        # totalRow = self.grid.rowCount()
        # totalCol = self.grid.columnCount()
        
        # 5. 재생성된 버튼 추가
        self.grid.addWidget(self.btn_insert, cnt_row, cnt_col - 2)
        self.grid.addWidget(self.btn_cancel, cnt_row, cnt_col - 1)

    # def closeEvent(self, QCloseEvent):
    #     ans = QMessageBox.question(self, "삽입 취소", "데이터 삽입을 취소하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
    #     if ans == QMessageBox.Yes:
    #         QCloseEvent.accept()
    #     else:
    #         QCloseEvent.ignore()



class mainLayout(QWidget, DB):
    def __init__(self):
        super(mainLayout, self).__init__()
        self.dbPrograms = DB()

        self.select_list_user = ["ID", "이름", "주민등록번호", "전화번호", "자격증", "주소", "본적주소", "기수", "반", "총 이수시간", "이론", "실기", "실습", "대체실습", "시험회차"]
        self.select_list_lecture = ["기수", "반", "시작일", "종료일"]
        self.select_list_teacher = ["ID", "분류", "이름", "생년월일", "자격증", "경력", "도 승인날짜"]
        self.select_list_temptraining = ["기수", "시작일", "종료일", "수여일"]
        self.select_list_temptrainingteacher = ["기수", "강사"]

        self.today = datetime.date.today()

        vbox = QVBoxLayout()
        first_hbox = QHBoxLayout()

        self.R_category = QComboBox(self)
        self.R_category.setFixedWidth(100)
        self.R_category.addItem("선택")

        self.R_searchBox = QLineEdit(self)
        self.R_searchBox.returnPressed.connect(self.search)

        self.R_searchBtn = QPushButton("검색", self)
        self.R_searchBtn.clicked.connect(self.search)

        first_hbox.addWidget(self.R_category)
        first_hbox.addWidget(self.R_searchBox)
        first_hbox.addWidget(self.R_searchBtn)

        second_hbox = QHBoxLayout()

        self.current_table = ""

        self.table = QTreeView(self)
        self.table.setAlternatingRowColors(True)
        self.table.setRootIsDecorated(False)
        # self.table.setFixedSize(800, 700)
        # QTreeView set read only
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.readDB = QtGui.QStandardItemModel(0, 1, self)
        # Qt.Horizontal: 수평값. 기본적으로 넣어야 함.
        self.readDB.setHeaderData(0, Qt.Horizontal, "선택")

        self.table.setModel(self.readDB)
        self.table.clicked.connect(self.selected)

        self.layoutInfo = QVBoxLayout()
        self.labelInfo = QLabel("선택된 객체의 정보가 표시됩니다.")
        self.textInfo = QTextEdit()
        self.textInfo.setReadOnly(True)
        self.textInfo.setFixedWidth(400)
        # self.textInfo.setFontPointSize(12)
        self.textInfo.setCurrentFont(QtGui.QFont("맑은 고딕"))
        self.layoutInfo.addWidget(self.labelInfo)
        self.layoutInfo.addWidget(self.textInfo)

        # self.gridInfo = QGridLayout()
        
        # 마지막 인자 1 왜넘겨주는지 모르겠음.
        # self.readDB.insertRows(self.readDB.rowCount(), 1)
        # # 삽입된 정보는 read only로 바꿔줘야 함.
        # self.readDB.setData(self.readDB.index(0, 0), self.readDB.rowCount())
        # self.readDB.setData(self.readDB.index(0, 1), "이영민")
        # self.readDB.setData(self.readDB.index(0, 2), "990728-1234567")
        # self.readDB.setData(self.readDB.index(0, 3), "010-1234-5678")
        # self.readDB.setData(self.readDB.index(0, 4), "일반")
        # self.readDB.insertRows(self.readDB.rowCount(), 1)
        # self.readDB.insertRows(self.readDB.rowCount(), 1)
        # self.readDB.insertRows(self.readDB.rowCount(), 1)
        # self.readDB.insertRows(self.readDB.rowCount(), 1)

        second_hbox.addWidget(self.table)
        second_hbox.addLayout(self.layoutInfo)

        # second_hbox.addLayout(self.gridInfo)

        vbox.addLayout(first_hbox)
        vbox.addLayout(second_hbox)

        self.setLayout(vbox)
        self.checkTodoList()

    def checkTodoList(self):
        schedule_lecture = {}
        schedule_temporary = {}
        schedule_exam = {}

        check_deadline = {"lecture":{}, "temporary":{}, "exam":{}}

        rs = self.dbPrograms.SELECT("classNumber, classTime, startDate, endDate", "lecture")
        for rows in rs:
            diff_start = (self.today - rows[2]).days
            diff_end = (self.today - rows[3]).days
            if diff_end < 0:
                continue
            schedule_lecture[str(rows[0]) + str(rows[1])] = {"시작일":rows[2], "종료일":rows[3], "start d-day":diff_start, "end d-day":diff_end}
            if diff_start <= 7 and diff_start >= 0:
                check_deadline["lecture"]

        rs = self.dbPrograms.SELECT("classNumber, startDate, endDate", "temptraining")
        for rows in rs:
            diff_start = (self.today - rows[1]).days
            diff_end = (self.today - rows[2]).days
            if diff_end < 0:
                continue
            schedule_temporary["대체실습 " + str(rows[0])] = {"시작일":rows[1], "종료일":rows[2], "start d-day":diff_start, "end d-day":diff_end}

        rs = self.dbPrograms.SELECT("round, startAcceptance, endAcceptance, passDate", "exam")
        for rows in rs:
            diff_accept_start = (self.today - rows[1]).days
            diff_accept_end = (self.today - rows[2]).days
            diff_pass = (self.today - rows[3]).days
            if diff_pass < 0:
                continue
            schedule_exam[str(rows[0]) + "회"] = {"응시원서 접수시작":rows[1], "응시원서 접수종료":rows[2], "합격자 발표":rows[3], "accept start d-day":diff_accept_start, "accept end d-day":diff_accept_end, "pass d-day":diff_accept_pass}
        


        

    def selected(self):
        if self.current_table == "user":
            self.textInfo.clear()

            ID = "ID: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            name = "이름: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            RRN = "주민등록번호: " + str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            phone = "전화번호: " + str(self.readDB.index(self.table.currentIndex().row(), 3).data())
            licen = "자격증: " + str(self.readDB.index(self.table.currentIndex().row(), 4).data())
            adr = "주소: " + str(self.readDB.index(self.table.currentIndex().row(), 5).data())
            oAdr = "본적주소: " + str(self.readDB.index(self.table.currentIndex().row(), 6).data())
            clsN = "기수: " + str(self.readDB.index(self.table.currentIndex().row(), 7).data())
            clsT = "반: " + str(self.readDB.index(self.table.currentIndex().row(), 8).data())
            totalH = "총 이수시간: " + str(self.readDB.index(self.table.currentIndex().row(), 9).data())
            theH = "이론: " + str(self.readDB.index(self.table.currentIndex().row(), 10).data())
            pracH = "실기: " + str(self.readDB.index(self.table.currentIndex().row(), 11).data())
            trainH = "실습: " + str(self.readDB.index(self.table.currentIndex().row(), 12).data())
            tempC = "대체실습: " + str(self.readDB.index(self.table.currentIndex().row(), 13).data())
            exam = "시험회차: " + str(self.readDB.index(self.table.currentIndex().row(), 14).data())

            send_string = ID + "\n\n" + name + "\n\n" + RRN + "\n\n" + phone + "\n\n" + licen + "\n\n" + adr + "\n\n" + oAdr + "\n\n" +\
                clsN + "\n\n" + clsT + "\n\n" + totalH + "\n\n" + theH + "\n\n" + pracH + "\n\n" + trainH + "\n\n" + tempC + "\n\n" + exam

        elif self.current_table == "lecture":
            self.textInfo.clear()

            clsN = "기수: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            clsT = "반: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            startD = "시작일: " + str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            endD = "종료일: " + str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            send_string = clsN + "\n\n" + clsT + "\n\n" + startD + "\n\n" + endD
            
        elif self.current_table == "teacher":
            self.textInfo.clear()
            
            ID = "ID: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            categ = "분류: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            name = "이름: " + str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            DOB = "생년월일: " + str(self.readDB.index(self.table.currentIndex().row(), 3).data())
            licen = "자격증: " + str(self.readDB.index(self.table.currentIndex().row(), 4).data())
            career = "경력: " + str(self.readDB.index(self.table.currentIndex().row(), 5).data())
            ACKDate = "도 승인일자: " + str(self.readDB.index(self.table.currentIndex().row(), 6).data())

            send_string = ID + "\n\n" + categ + "\n\n" + DOB + "\n\n" + licen + "\n\n" + career + "\n\n" + ACKDate

        elif self.current_table == "temptraining":
            self.textInfo.clear()

            clsN = "기수: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            startD = "시작일: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            endD = "종료일: " + str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            awardD = "수여일: " + str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            send_string = clsN + "\n\n" + startD + "\n\n" + endD + "\n\n" + awardD
            
        elif self.current_table == "temptrainingteacher":
            self.textInfo.clear()

            clsN = "기수: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            teacher = "반: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())

            send_string = clsN + "\n\n" + teacher

        self.textInfo.setText(send_string)

    def selectTable(self):
        if self.current_table == "user":
            self.readDB.setColumnCount(15)
            self.readDB.setHorizontalHeaderLabels(self.select_list_user)

        elif self.current_table == "lecture":
            self.readDB.setColumnCount(4)
            self.readDB.setHorizontalHeaderLabels(self.select_list_lecture)

        elif self.current_table == "teacher":
            self.readDB.setColumnCount(7)
            self.readDB.setHorizontalHeaderLabels(self.select_list_teacher)

        elif self.current_table == "temptraining":
            self.readDB.setColumnCount(4)
            self.readDB.setHorizontalHeaderLabels(self.select_list_temptraining)

        elif self.current_table == "temptrainingteacher":
            self.readDB.setColumnCount(2)
            self.readDB.setHorizontalHeaderLabels(self.select_list_temptrainingteacher)

    def showTable(self, Refresh=False):
        source = self.sender()
        self.changeCategory(Refresh=Refresh)
        self.readDB.clear()
        self.R_searchBox.clear()

        if Refresh == False:
            if source.text() == "수강생 관리":
                self.current_table = "user"
                order = "classNumber *1, FIELD(classTime, '주간', '야간'), FIELD(license, '일반', '사회복지사', '간호조무사', '간호사', '물리치료사'), id *1"

                self.readDB.setColumnCount(15)
                self.readDB.setHorizontalHeaderLabels(self.select_list_user)

            elif source.text() == "기수 관리":
                self.current_table = "lecture"
                order = "FIELD(classTime, '주간', '야간'), classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_lecture)

            elif source.text() == "강사 관리":
                self.current_table = "teacher"
                order = "id"

                self.readDB.setColumnCount(7)
                self.readDB.setHorizontalHeaderLabels(self.select_list_teacher)


            elif source.text() == "대체실습":
                self.current_table = "temptraining"
                order = "classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptraining)

            elif source.text() == "대체실습 담당강사":
                self.current_table = "temptrainingteacher"
                order = "classNumber"

                self.readDB.setColumnCount(2)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptrainingteacher)

        elif Refresh == True:
            if self.current_table == "user":
                order = "classNumber *1, FIELD(classTime, '주간', '야간'), FIELD(license, '일반', '사회복지사', '간호조무사', '간호사', '물리치료사'), id *1"

                self.readDB.setColumnCount(15)
                self.readDB.setHorizontalHeaderLabels(self.select_list_user)

            elif self.current_table == "lecture":
                order = "FIELD(classTime, '주간', '야간'), classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_lecture)

            elif self.current_table == "teacher":
                order = "id"

                self.readDB.setColumnCount(7)
                self.readDB.setHorizontalHeaderLabels(self.select_list_teacher)

            elif self.current_table == "temptraining":
                order = "classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptraining)

            elif self.current_table == "temptrainingteacher":
                order = "classNumber"

                self.readDB.setColumnCount(2)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptrainingteacher)

        order += " *1"
        rs = self.dbPrograms.SELECT("*", self.current_table, orderBy=order)

        if rs == "error":
            QMessageBox.information(self, "SQL query Error", "SQL query returns error!", QMessageBox.Yes, QMessageBox.Yes)
        else:
            cols = self.readDB.columnCount()
            for i in range(len(rs)):
                self.readDB.insertRows(self.readDB.rowCount(), 1)
                for j in range(cols):
                    string = str(rs[i][j])
                    if string == "None":
                        string = NULL
                    self.readDB.setData(self.readDB.index(i, j), string)

    def changeCategory(self, Refresh=False):
        source = self.sender()
        self.R_category.clear()
        if Refresh == False:
            if source.text() == "수강생 관리":
                self.R_category.addItem("ID")
                self.R_category.addItem("이름")
                self.R_category.addItem("자격증")
                self.R_category.addItem("기수/반")
                self.R_category.addItem("대체실습")
                self.R_category.addItem("시험회차")
                self.R_category.addItem("SQL")

            elif source.text() == "기수 관리":
                self.R_category.addItem("기수/반")
                self.R_category.addItem("SQL")

            elif source.text() == "강사 관리":
                self.R_category.addItem("ID")
                self.R_category.addItem("이름")
                self.R_category.addItem("자격증")
                self.R_category.addItem("SQL")

            elif source.text() == "대체실습":
                self.R_category.addItem("기수")
                # 시작일은 검색어 "이후"의 날짜들 모두, 종료일은 검색어 "이전"의 날짜들 모두
                # (시작일을 2022-01-01로 검색할 경우 1월 1일 이후에 시작하는 기수 검색)
                # (종료일을 2022-01-01로 검색할 경우 1월 1일 이전에 종료된 기수 검색)
                self.R_category.addItem("시작일")
                self.R_category.addItem("종료일")
                self.R_category.addItem("수여일")
                self.R_category.addItem("SQL")

            elif source.text() == "대체실습 담당강사":
                self.R_category.addItem("기수")
                self.R_category.addItem("강사")
                self.R_category.addItem("SQL")

        elif Refresh == True:
            if self.current_table == "user":
                self.R_category.addItem("ID")
                self.R_category.addItem("이름")
                self.R_category.addItem("자격증")
                self.R_category.addItem("기수/반")
                self.R_category.addItem("대체실습")
                self.R_category.addItem("시험회차")
                self.R_category.addItem("SQL")

            elif self.current_table == "lecture":
                self.R_category.addItem("기수/반")
                self.R_category.addItem("SQL")

            elif self.current_table == "teacher":
                self.R_category.addItem("ID")
                self.R_category.addItem("이름")
                self.R_category.addItem("자격증")
                self.R_category.addItem("SQL")

            elif self.current_table == "temptraining":
                self.R_category.addItem("기수")
                # 시작일은 검색어 "이후"의 날짜들 모두, 종료일은 검색어 "이전"의 날짜들 모두
                # (시작일을 2022-01-01로 검색할 경우 1월 1일 이후에 시작하는 기수 검색)
                # (종료일을 2022-01-01로 검색할 경우 1월 1일 이전에 종료된 기수 검색)
                self.R_category.addItem("시작일")
                self.R_category.addItem("종료일")
                self.R_category.addItem("수여일")
                self.R_category.addItem("SQL")

            elif self.current_table == "temptrainingteacher":
                self.R_category.addItem("기수")
                self.R_category.addItem("강사")
                self.R_category.addItem("SQL")

    def search(self):
        order = None
        keyWord = self.R_searchBox.text()
        if keyWord == "":
            QMessageBox.information(self, "검색어 오류", "검색어가 존재하지 않습니다!", QMessageBox.Yes, QMessageBox.Yes)
            return

        current_table = self.current_table
        current_category = self.R_category.currentText()

        if current_category == "ID":
            current_category = "id"

        elif current_category == "이름":
            current_category = "name"

        elif current_category == "자격증":
            current_category = "license"

        elif current_category == "기수/반":
            words = keyWord.split(" ")
            if len(words) == 1:
                if keyWord[-1] == "간":
                    current_category = "classTime"

                else:
                    current_category = "classNumber"
            
            elif len(words) == 2:
                if words[0][-1] == "간":
                    current_category = "classTime = '{}' and classNumber".format(words[0])
                    keyWord = words[1]

                else:
                    current_category = "classNumber = '{}' and classTime".format(words[0])
                    keyWord = words[1]

            if current_table == "user":
                order = "classNumber *1, FIELD(classTime, '주간', '야간'), FIELD(license, '일반', '사회복지사', '간호조무사', '간호사', '물리치료사'), id *1"
            else:
                order = "classNumber *1, FIELD(classTime, '주간', '야간')"

        elif current_category == "대체실습":
            current_category = "temporaryClassNumber"

        elif current_category == "시험회차":
            current_category = "exam"
            order = "classNumber *1, FIELD(classTime, '주간', '야간'), FIELD(license, '일반', '사회복지사', '간호조무사', '간호사', '물리치료사'), id *1"
            
        elif current_category == "시작일":
            current_category = "startDate"
            
        elif current_category == "종료일":
            current_category = "endDate"
            
        elif current_category == "수여일":
            current_category = "awardDate"
            
        elif current_category == "강사":
            current_category = "teacherName"

        elif current_category == "SQL":
            ans = QMessageBox.question(self, "SQL query문 전달", "SQL query문을 전달합니다.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ans == QMessageBox.Yes:
                res = self.dbPrograms.SQL(keyWord)
                if res != "error":
                    QMessageBox.about(self, "완료", "query를 성공적으로 전달했습니다.")
                else:
                    QMessageBox.information(self, "SQL query Error", "SQL query returns error!", QMessageBox.Yes, QMessageBox.Yes)

                self.showTable(Refresh=True)
                self.textInfo.clear()
                return
            else:
                return
            
        else:
            QMessageBox.information(self, "Category Error", "error!", QMessageBox.Yes, QMessageBox.Yes)
            return

        try:
            self.readDB.clear()
            self.selectTable()
            if current_category == "name" or current_category == "teacherName":
                rs = self.dbPrograms.SELECT("*", current_table, where=f"{current_category} LIKE '%{keyWord}%'", orderBy=order)
            else:
                rs = self.dbPrograms.SELECT("*", current_table, where=f"{current_category} = '{keyWord}'", orderBy=order)
                
            if rs == "error":
                QMessageBox.information(self, "SQL query Error", "SQL query returns error!", QMessageBox.Yes, QMessageBox.Yes)
            else:
                search_result = "{}, \"{}\" 검색 결과\n{}개의 검색 결과가 존재합니다.".format(self.R_category.currentText(), self.R_searchBox.text(), len(rs))
                self.textInfo.setText(search_result)
                cols = self.readDB.columnCount()
                for i in range(len(rs)):
                    self.readDB.insertRows(self.readDB.rowCount(), 1)
                    for j in range(cols):
                        string = str(rs[i][j])
                        if string == "None":
                            string = NULL
                        self.readDB.setData(self.readDB.index(i, j), string)
        except:
            QMessageBox.information(self, "검색 오류", "잘못된 검색입니다.", QMessageBox.Yes, QMessageBox.Yes)
            return

    def DELETE(self):
        target_table = ""
        check = ""
        if self.current_table == "user":
            target_table = "user"
            ID = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            name = str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            RRN = str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            phone = str(self.readDB.index(self.table.currentIndex().row(), 3).data())
            licen = str(self.readDB.index(self.table.currentIndex().row(), 4).data())
            adr = str(self.readDB.index(self.table.currentIndex().row(), 5).data())
            oAdr = str(self.readDB.index(self.table.currentIndex().row(), 6).data())
            clsN = str(self.readDB.index(self.table.currentIndex().row(), 7).data())
            clsT =  str(self.readDB.index(self.table.currentIndex().row(), 8).data())
            totalH = str(self.readDB.index(self.table.currentIndex().row(), 9).data())
            theH = str(self.readDB.index(self.table.currentIndex().row(), 10).data())
            pracH = str(self.readDB.index(self.table.currentIndex().row(), 11).data())
            trainH = str(self.readDB.index(self.table.currentIndex().row(), 12).data())
            tempC = str(self.readDB.index(self.table.currentIndex().row(), 13).data())

            query = "id = '{}' and name = '{}'".format(ID, name)

            check = "ID: {}\t이름: {}\t주민등록번호: {}\n전화번호: {}\t자격증: {}\n주소: {}\n본적주소: {}\n기수: {}\t반: {}\t 대체실습: {}\n총 이수시간: {}\t이론이수: {}\t실습이수: {}\t 실기이수: {}\n"\
                .format(ID, name, RRN, phone, licen, adr, oAdr, clsN, clsT, tempC, totalH, theH, pracH, trainH)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."

        elif self.current_table == "lecture":
            target_table = "lecture"
            clsN = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            clsT = str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            startD = str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            endD = str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            query = "classNumber = '{}' and classTime = '{}'".format(clsN, clsT)

            check = "기수: {}\t반: {}\n시작일: {}\n종료일: {}\n".format(clsN, clsT, startD, endD)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."
            
        elif self.current_table == "teacher":
            target_table = "teacher"
            ID = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            categ = str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            name = str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            DOB = str(self.readDB.index(self.table.currentIndex().row(), 3).data())
            licen = str(self.readDB.index(self.table.currentIndex().row(), 4).data())
            career = str(self.readDB.index(self.table.currentIndex().row(), 5).data())
            ACKDate = str(self.readDB.index(self.table.currentIndex().row(), 6).data())

            query = "name = '{}'".format(name)

            check = "ID: {}\t이름: {}\t자격증: {}\n생년월일: {}\t구분: {}\n최소경력: {}\n도 승인일자: {}\n"\
                .format(ID, name, licen, DOB, categ, career, ACKDate)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."

        elif self.current_table == "temptraining":
            target_table = "temptraining"
            clsN = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            startD = str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            endD = str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            awardD = str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            check = "기수: {}\n시작일: {}\n종료일: {}\n수여일: {}\n".format(clsN, startD, endD, awardD)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."

            query = "classNumber = '{}'".format(clsN)
            
        elif self.current_table == "temptrainingteacher":
            target_table = "temptrainingteacher"
            clsN = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            teacher = str(self.readDB.index(self.table.currentIndex().row(), 1).data())

            query = "classNumber = '{}' and teacherName = '{}'".format(clsN, teacher)

            check = "기수: {}\n강사: {}\n".format(clsN, teacher)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."


        ans = QMessageBox.question(self, "데이터 삭제 확인", check, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            db.main.dbPrograms.DELETE(target_table, query)
            QMessageBox.about(self, "완료", "데이터를 성공적으로 삭제했습니다.")
            self.showTable(Refresh=True)
            self.textInfo.clear()
        else:
            pass

    def isNULL(self):
        self.changeCategory(Refresh=True)
        self.readDB.clear()
        self.R_searchBox.clear()
        self.selectTable()

        if self.current_table == "":
            QMessageBox.information(self, "객체 오류", "테이블을 먼저 선택해주세요.", QMessageBox.Yes, QMessageBox.Yes)
            return

        elif self.current_table == "user":
            query = "id IS null or name IS null or RRN IS null or phoneNumber IS null or license IS null or address IS null or originAddress IS null or classNumber IS null or classTime IS null or totalCreditHour IS null or theoryCreditHour IS null or practicalCreditHour IS null or trainingCreditHour IS null or temporaryClassNumber IS null or exam IS null"
            order = "id"
            
        elif self.current_table == "lecture":
            query = "classNumber IS null or classTime IS null or startDate IS null or endDate IS null"
            order = "classNumber"

        elif self.current_table == "teacher":
            query = "id IS null or category IS null or name IS null or dateOfBirth IS null or license IS null or minCareer IS null or ACKDate IS null"
            order = "id"

        elif self.current_table == "temptraining":
            query = "classNumber IS null or startDate IS null or endDate IS null or awardDate IS null"
            order = "classNumber"

        elif self.current_table == "temptrainingteacher":
            query = "classNumber IS null or teacherName IS null"
            order = "classNumber"

        order += " *1"
        rs = self.dbPrograms.SELECT("*", self.current_table, where=query, orderBy=order)
        if rs == "error":
            QMessageBox.information(self, "SQL query Error", "SQL query returns error!", QMessageBox.Yes, QMessageBox.Yes)
        else:
            cols = self.readDB.columnCount()
            for i in range(len(rs)):
                self.readDB.insertRows(self.readDB.rowCount(), 1)
                for j in range(cols):
                    string = str(rs[i][j])
                    if string == "None":
                        string = NULL
                    self.readDB.setData(self.readDB.index(i, j), string)

    def readFiles(self):
        """
        type. 1
        1. pre_file, next_file 같이 읽어서, 이름을 찾는다.
        2. 2-1. 이름이 같으면 등본에서 이름, 현주소, 주민등록번호를, 기본증명서에서 등록기준지를 가져온다.
        2. 2-2. 이름이 다르다 -> 
        이름이 같은지 확인하는 방법? 알고리즘 여러개 따보자!
        1) image -> string -> list 변환 후 check each value's length -> 3 <= len(list[i]) <=5(?) ==> 이름으로 판단한다!

        type. 2
        1. read_file -> 이미지를 읽어서 우측에 작은 화면으로 띄운다.(win+-> or 방법 있으면 사용)
        2. read_file의 제목을 읽어 주민등록 등본인지, 기본증명서인지 check
        3. insert 창을 active 시키고, 제목에 따라 [이름, 주민번호 == 공통] and ([현주소 == 등본] or [본적주소 == 기본증명서])
            를 읽어서 LineEdit에 먼저 값을 넣는다.
        4. insert 창에는 '데이터 입력', '건너뛰기', '삽입', '취소' 버튼이 존재한다.
        5. '데이터 입력' 클릭 시, read_file의 제목에 따라 [이름, 주민번호 == 공통] and ([현주소 == 등본] or [본적주소 == 기본증명서])
            를 읽어서 LineEdit에 값을 추가한다.(등본 입력 후 기본증명서 입력 시 사용. LineEdit value != ""일 경우에 추가입력.)
        6. '건너뛰기' 클릭 시 데이터 추가를 하지 않고, 다음 파일로 건너 뛴다. 이미지 창을 닫고 다음 이미지를 같은 크기로 active.
        7. '삽입' 클릭 시 입력된 데이터를 기반으로 Database에 추가하고, 파일 명을 변경하여 해당 수강생의 폴더로 옮긴다.
        8. '취소' 입력 시 함수를 return하고 함수를 종료한다.
        """
        file_path = ""  # scan file path
        file_type = ""  # 주민등록등본 or 기본증명서
        name = ""
        RRN = ""
        adr = ""
        oAdr = ""

        pass

    def backupToExcel(self):
        # print(self.readDB.rowCount()) row 개수. 1개면 1
        # IDF = str(self.readDB.index(1, 0).data()) row 접근 인덱스는 0 ~ rowCount() - 1
        # IDL = str(self.readDB.index(242, 0).data())
        # print("IDF:", IDF, "\nIDL:", IDL)

        today = datetime.today().strftime("%Y%m%d")
        today = today[2:]
        file_name = ""
        self.backUpWbook = Workbook()
        ws = self.backUpWbook.active
        col = []
        dimension_lst = []

        if self.current_table == "":
            QMessageBox.information(self, "오류", "테이블을 먼저 선택해주세요.", QMessageBox.Yes, QMessageBox.Yes)
            return

        if self.current_table == "user":
            col = self.select_list_user
            dimension_lst = [9, 10, 20, 20, 15, 73, 63, 10, 10, 10, 5, 5, 5, 10, 9]
            file_name = "수강생DB"

        elif self.current_table == "lecture":
            col = self.select_list_lecture
            dimension_lst = [10, 10, 15, 15]
            file_name = "기수,반DB"

        elif self.current_table == "teacher":
            col = self.select_list_teacher
            dimension_lst = [9, 12, 10, 15, 15, 15, 15]
            file_name = "강사DB"

        elif self.current_table == "temptraining":
            col = self.select_list_temptraining
            dimension_lst = [10, 15, 15, 15]
            file_name = "대체실습DB"

        elif self.current_table == "temptrainingteacher":
            col = self.select_list_temptrainingteacher
            dimension_lst = [10, 10]
            file_name = "대체실습 강사DB"

        for i, val in enumerate(col, start=1):
            ws.cell(row=1, column=i).value = val
            ws.column_dimensions[get_column_letter(i)].width = dimension_lst[i - 1]

        if self.current_table == "user":
            for i in range(self.readDB.rowCount()):
                for j in range(len(col)):
                    if str(self.readDB.index(i, j).data()) == "NULL":
                        continue
                    else:
                        ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())

        elif self.current_table == "lecture":
            for i in range(self.readDB.rowCount()):
                for j in range(len(col)):
                    if str(self.readDB.index(i, j).data()) == "NULL":
                        continue
                    else:
                        ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())
            
        elif self.current_table == "teacher":
            for i in range(self.readDB.rowCount()):
                for j in range(len(col)):
                    if str(self.readDB.index(i, j).data()) == "NULL":
                        continue
                    else:
                        ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())

        elif self.current_table == "temptraining":
            for i in range(self.readDB.rowCount()):
                for j in range(len(col)):
                    if str(self.readDB.index(i, j).data()) == "NULL":
                        continue
                    else:
                        ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())
            
        elif self.current_table == "temptrainingteacher":
            for i in range(self.readDB.rowCount()):
                for j in range(len(col)):
                    if str(self.readDB.index(i, j).data()) == "NULL":
                        continue
                    else:
                        ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())

        save_path = f"D:\\남양노아요양보호사교육원\\데이터베이스 백업\\{today}_{file_name}.xlsx"

        ans = QMessageBox.question(self, "Back up", f"{file_name}를 Excel 파일로 생성합니다.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if ans == QMessageBox.Yes:
            self.backUpWbook.save(save_path)
            QMessageBox.about(self, "완료", "데이터를 성공적으로 수정했습니다.\n경로: {}".format(save_path))
        else:
            QMessageBox.about(self, "취소", "데티어 백업을 취소했습니다.")


class DBMS(QMainWindow):
    # 새 창을 띄우기 위해 서로 global로 연결
    global insert
    global update
    global batch
    global report_gov

    global scanner

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NYNOA DBMS")
        self.setWindowIcon(QIcon("D:\\Master\\PythonWorkspace\\NYNOA\\Icons\\남양노아요양보호사.jpg"))
        self.resize(1200, 800)
        # self.setFixedSize(1200, 800)

        # status Bar
        # self.statusBar()
        self.statusBar().showMessage("상태바")
        self.main = mainLayout()

        self.setCentralWidget(self.main)

        self.menuOpt()

        self.show()

    # 상단 menu
    def menuOpt(self):
        # menu Bar
        menuBar = self.menuBar()    # menu 생성
        menu_file = menuBar.addMenu("File") # group 생성
        menu_edit = menuBar.addMenu("Edit")
        menu_view = menuBar.addMenu("View")

        menu_stu = menuBar.addAction("수강생 관리")
        menu_lecture = menuBar.addAction("기수 관리")
        menu_teach = menuBar.addAction("강사 관리")
        menu_temp = menuBar.addAction("대체실습")
        menu_tempTeach = menuBar.addAction("대체실습 담당강사")
        menu_isNULL = menuBar.addAction("미입력 데이터")

        menu_isNULL.setStatusTip("데이터가 입력되지 않은 컬럼들을 찾습니다.")
        menu_isNULL.setShortcut("Ctrl+Shift+Q")

        file_exit = QAction('Exit', self)   # menu 객체 생성
        file_exit.setShortcut("Ctrl+Q")
        file_exit.setStatusTip("나가기")
        # file_exit.triggered.connect(QCoreApplication.instance().quit)   # 종료 기능 추가 / self.close()로도 종료 가능
        file_exit.triggered.connect(self.close)      # 위와 같은 기능. 메서드를 전달하는 것이기 때문에 ()없이!

        file_new = QMenu("New", self)   # sub menu 객체 생성
        new_data = QAction("데이터 추가", self)
        new_data.setShortcut("Ctrl+N")
        new_data.setStatusTip("선택된 테이블에 새로운 데이터를 추가합니다.")

        file_new.addAction(new_data)

        file_scan = QMenu("Scan", self)
        read_data = QAction("파일 스캔", self)

        file_scan.addAction(read_data)

        file_backUp = QAction("Back up", self)
        file_backUp.setStatusTip("현재 선택된 데이터베이스 테이블을 엑셀 파일로 생성해 백업합니다.")
        file_backUp.triggered.connect(self.main.backupToExcel)

        file_report = QMenu("경기도청", self)
        beginning_lecture = QAction("개강보고", self)
        implement_temp_class = QAction("대체실습 실시보고", self)
        complete_temp_class = QAction("대체실습 수료보고", self)

        file_report.addAction(beginning_lecture)
        file_report.addAction(implement_temp_class)
        file_report.addAction(complete_temp_class)

        beginning_lecture.triggered.connect(self.report_gov_show)
        implement_temp_class.triggered.connect(self.report_gov_show)
        complete_temp_class.triggered.connect(self.report_gov_show)
        
        # menu에 addAction 할 경우, 이렇게 하면 안되고, 함수를 따로 생성해서 넘겨주어야 한다. 이유는 모름.
        # new_data.triggered.connect(insert.show())
        new_data.triggered.connect(self.INSERT_show)
        read_data.setShortcut("Ctrl+F")
        read_data.setStatusTip("폴더를 스켄하여 데이터베이스에 데이터를 삽입합니다.")
        read_data.triggered.connect(self.scan_show)
        
        batch_data = QAction("시험회차 일괄 수정", self)
        batch_data.setShortcut("Ctrl+Shift+D")
        batch_data.setStatusTip("특정 기수, 반의 시험 회차를 일괄적으로 설정합니다.")
        batch_data.triggered.connect(self.batch_show)

        mod_data = QAction("데이터 수정", self)
        mod_data.setShortcut("Ctrl+D")
        mod_data.setStatusTip("테이블에서 선택된 데이터를 수정합니다.")
        mod_data.triggered.connect(self.UPDATE_show)

        del_data = QAction("데이터 삭제", self)
        del_data.setShortcut(Qt.Key_Delete)
        del_data.setStatusTip("테이블에서 선택된 데이터를 삭제합니다.")
        del_data.triggered.connect(self.main.DELETE)

        view_stat = QAction("가이드 표시", self, checkable=True)
        view_stat.setChecked(True)
        view_stat.triggered.connect(self.triState)

        menu_file.addAction(file_backUp)
        menu_file.addMenu(file_report)
        menu_file.addMenu(file_scan)
        menu_file.addMenu(file_new)     # sub menu 등록
        menu_file.addAction(file_exit)  # menu 등록(액션 추가)
        menu_view.addAction(view_stat)

        menu_edit.addAction(batch_data)
        menu_edit.addAction(mod_data)
        menu_edit.addAction(del_data)

        menu_stu.triggered.connect(self.main.showTable)
        menu_lecture.triggered.connect(self.main.showTable)
        menu_teach.triggered.connect(self.main.showTable)
        menu_temp.triggered.connect(self.main.showTable)
        menu_tempTeach.triggered.connect(self.main.showTable)

        menu_isNULL.triggered.connect(self.main.isNULL)

    def scan_show(self):
        QMessageBox.information(self, "알림", "기능이 준비되지 않았습니다!", QMessageBox.Yes, QMessageBox.Yes)
        return
        path = "D:\\scan"
        file_list = []

        # print(os.listdir(path))

        for f in os.listdir(path):
            file_name, ext = os.path.splitext(f)
            if ext == ".jpg":
                file_list.append(str(path) + "\\" + str(f))
        
        scanner.file_list = file_list
        scanner.show()

    def report_gov_show(self):
        source = self.sender()
        report_gov.doc_type = source.text()
        report_gov.show()

    def batch_show(self):
        batch.show()

    def UPDATE_show(self):
        if self.main.textInfo.toPlainText() == "":
            QMessageBox.information(self, "객체 오류", "객체를 먼저 선택해주세요.",
            QMessageBox.Yes, QMessageBox.Yes)

        else:
            update.show()


    def INSERT_show(self):
        if self.main.current_table == "":
            QMessageBox.information(self, "테이블 오류", "테이블을 먼저 선택해주세요.\n상단 메뉴에 테이블이 존재합니다.",
            QMessageBox.Yes, QMessageBox.Yes)

        else:
            insert.show()

    def triState(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            print("ESC is pressed!")

    # context menu. 우클릭 메뉴
    def contextMenuEvent(self, QContextMenuEvent):
        cm = QMenu(self)
        
        quit = cm.addAction("Quit")

        # action: cm의 실행정보를 저장. 전체적인 map의 위치를 넘겨서 우클릭 하는 위치에 따라 다른 이벤트를 적용하도록
        action = cm.exec_(self.mapToGlobal(QContextMenuEvent.pos()))

        if action == quit:
            self.close()


    def closeEvent(self, QCloseEvent):
        # x(창닫기) 버튼을 눌렀을 경우!
        # QMessageBox.question(인자, title, message, 버튼 추가(여러개 가능(|사용)), 버튼 기본값)
        ans = QMessageBox.question(self, "종료", "DBMS를 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if ans == QMessageBox.Yes:
            ####################### 여기다가 conn.close()추가하기 !!!!!!!!!!!!!!!!!!!!!
            try:
                self.main.dbPrograms.conn.close()
            except:
                print("DBGUI Exception: Database is already closed!")
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = DBMS()
    insert = INSERT()
    update = UPDATE()
    batch = batchUpdate()
    report_gov = report()
    auto = Automation()

    # scanner = scanFile()
    sys.exit(app.exec_())