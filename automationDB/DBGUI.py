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
from datetime import datetime

import os
import shutil

from PIL import Image

class scanFile(QWidget):
    global db

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("파일 스캔")
        self.file_list = []
        self.file_index = 0
        
    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.targetTable = "user"
        cnt_row = 5
        cnt_col = 7
        self.resize(600, 400)

        self.labelImg = QLabel(self)
        self.labelImg.setFixedSize(500, 600)
        self.grid.addWidget(self.labelImg, 0, 0, cnt_row, 1)
        self.labelID_user = QLabel("ID", self)
        self.labelID_user.setFixedWidth(90)
        self.labelID_user.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelID_user, 0, 1)
        self.textID_user = QLineEdit()
        self.grid.addWidget(self.textID_user, 0, 2)
        self.labelName_user = QLabel("이름", self)
        self.labelName_user.setFixedWidth(90)
        self.labelName_user.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelName_user, 0, 3)
        self.textName_user = QLineEdit()
        self.grid.addWidget(self.textName_user, 0, 4)
        self.labelLicen_user = QLabel("자격증", self)
        self.labelLicen_user.setFixedWidth(90)
        self.labelLicen_user.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelLicen_user, 0, 5)
        self.textLicen_user = QLineEdit()
        self.grid.addWidget(self.textLicen_user, 0, 6)

        self.labelClsN_user = QLabel("기수", self)
        self.labelClsN_user.setFixedWidth(90)
        self.labelClsN_user.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelClsN_user, 1, 1)
        self.textClsN_user = QLineEdit()
        self.grid.addWidget(self.textClsN_user, 1, 2)
        self.labelClsT_user = QLabel("반", self)
        self.labelClsT_user.setFixedWidth(90)
        self.labelClsT_user.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelClsT_user, 1, 3)
        self.textClsT_user = QLineEdit()
        self.grid.addWidget(self.textClsT_user, 1, 4)
        self.labelTemp = QLabel("대체실습", self)
        self.labelTemp.setFixedWidth(90)
        self.labelTemp.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelTemp, 1, 5)
        self.textTemp = QLineEdit()
        self.grid.addWidget(self.textTemp, 1, 6)

        self.labelRRN = QLabel("주민등록번호", self)
        self.labelRRN.setFixedWidth(90)
        self.labelRRN.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelRRN, 2, 1)
        self.textRRN = QLineEdit()
        self.grid.addWidget(self.textRRN, 2, 2, 1, 2)
        self.labelPhone = QLabel("전화번호", self)
        self.labelPhone.setFixedWidth(90)
        self.labelPhone.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelPhone, 2, 4)
        self.textPhone = QLineEdit()
        self.grid.addWidget(self.textPhone, 2, 5, 1, 2)
        
        
        self.labelAdr = QLabel("주소", self)
        self.labelAdr.setFixedWidth(90)
        self.labelAdr.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelAdr, 3, 1)
        self.textAdr = QLineEdit()
        self.grid.addWidget(self.textAdr, 3, 2, 1, 5)
        self.labelOriginAdr = QLabel("본적주소", self)
        self.labelOriginAdr.setFixedWidth(90)
        self.labelOriginAdr.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.labelOriginAdr, 4, 1)
        self.textOriginAdr = QLineEdit()
        self.grid.addWidget(self.textOriginAdr, 4, 2, 1, 5)

        self.btnInsert = QPushButton("Insert", self)
        self.btnInsert.clicked.connect(self.scanner)
        self.btnCancel = QPushButton("Close", self)
        self.btnCancel.clicked.connect(self.close)

        self.grid.addWidget(self.btnInsert, cnt_row, cnt_col - 2)
        self.grid.addWidget(self.btnCancel, cnt_row, cnt_col - 1)

    def refreshUI(self):
        print("self.file_list")
        print(self.file_list)

        file_name = self.file_list[self.file_index]
        pixmap = QPixmap(file_name)
        pixmap = pixmap.scaledToWidth(500)

        self.labelImg.setPixmap(QPixmap(pixmap))
        self.textID_user.clear()
        self.textName_user.clear()
        self.textLicen_user.clear()
        self.textClsN_user.clear()
        self.textClsT_user.clear()
        self.textTemp.clear()
        self.textRRN.clear()
        self.textPhone.clear()
        self.textAdr.clear()
        self.textOriginAdr.clear()

        doc_type = "주민등록등본"
        name = "name"
        adr = "주소"
        origin_adr = "본적주소"

        self.textName_user.setText(name)
        self.textAdr.setText(adr)
        self.textOriginAdr.setText(origin_adr)

        print("self.textID_user.text()")
        print("\"" + self.textID_user.text() + "\"")
        print(type(self.textID_user.text()))
        print("self.textName_user.text()")
        print("\"" + self.textName_user.text() + "\"")
        print(type(self.textName_user.text()))
        print("self.textLicen_user.text()")
        print("\"" + self.textLicen_user.text() + "\"")
        print(type(self.textLicen_user.text()))
        print("self.textClsN_user.text()")
        print("\"" + self.textClsN_user.text() + "\"")
        print(type(self.textClsN_user.text()))
        print("self.textClsT_user.text()")
        print("\"" + self.textClsT_user.text() + "\"")
        print(type(self.textClsT_user.text()))
        print("self.textTemp.text()")
        print("\"" + self.textTemp.text() + "\"")
        print(type(self.textTemp.text()))
        print("self.textRRN.text()")
        print("\"" + self.textRRN.text() + "\"")
        print(type(self.textRRN.text()))
        print("self.textPhone.text()")
        print("\"" + self.textPhone.text() + "\"")
        print(type(self.textPhone.text()))
        print("self.textAdr.text()")
        print("\"" + self.textAdr.text() + "\"")
        print(type(self.textAdr.text()))
        print("self.textOriginAdr.text()")
        print("\"" + self.textOriginAdr.text() + "\"")
        print(type(self.textOriginAdr.text()))

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

        rs = db.main.dbPrograms.SELECT("classNumber, classTime", "lecture", orderBy="classNumber")
        if rs == "error":
            QMessageBox.information(self, "ERROR", "class batchUpdate returns error", QMessageBox.Yes, QMessageBox.Yes)
        else:
            for rows in rs:
                self.class_num_list.append(rows[0])
            
            self.class_num_list = set(self.class_num_list)
            self.class_num_list = list(self.class_num_list)
            self.class_num_list.sort()
            self.combobox_N.addItems(self.class_num_list)

class UPDATE(QWidget):
    # 새 창을 띄우기 위해 서로 global로 연결
    global db

    def __init__(self):
        super().__init__()
        self.initUI()
        self.targetTable = ""
        self.base_path = "D:\\남양노아요양보호사교육원\\교육생관리"

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
        before_path = self.base_path + "\\{}\\{}{}".format(before_number, before_number, before_time)
        after_path = self.base_path + "\\{}\\{}{}".format(after_number, after_number, after_time)
        dir_list = os.listdir(before_path)

        for directory in dir_list:
            if name == directory:
                before_path = before_path + "\\{}".format(directory)

        if not os.path.exists(after_path):
            os.makedirs(after_path)

        shutil.move(before_path, after_path)

    def dataUpdate(self):
        if self.targetTable == "user":
            if self.textID_user.text().strip() == "" or self.textName_user.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return
            
            user_list = []
            user_list.append(self.textID_user.text().strip())
            user_list.append(self.textName_user.text().strip())
            user_list.append(self.textRRN.text().strip())
            user_list.append(self.textPhone.text().strip())
            user_list.append(self.textLicen_user.text().strip())
            user_list.append(self.textAdr.text().strip())
            user_list.append(self.textOriginAdr.text().strip())
            user_list.append(self.textClsN_user.text().strip())
            user_list.append(self.textClsT_user.text().strip())
            # 총 이수, 이론, 실기, 실습 시간으로 NULL값 추가
            try:
                total_Hour = str(int(self.textTheT.text().strip()) + int(self.textPracT.text().strip()) + int(self.textTrainT.text().strip()))
            except:
                total_Hour = NULL
            user_list.append(total_Hour)
            user_list.append(self.textTheT.text().strip())
            user_list.append(self.textPracT.text().strip())
            user_list.append(self.textTrainT.text().strip())
            user_list.append(self.textTemp.text().strip())
            user_list.append(self.textExam.text().strip())

            query_list = ["id", "name", "RRN", "phoneNumber", "license", "address", "originAddress", "classNumber", "classTime", \
                "totalCreditHour", "theoryCreditHour", "practicalCreditHour", "trainingCreditHour", "temporaryClassNumber", "exam"]

            where = "id = '{}' and name = '{}' and RRN='{}'".format(self.key_dict["ID"], self.key_dict["name"], self.key_dict["RRN"])
            query = ""
            for i in range(len(user_list)):
                query += query_list[i] + "="

                # 값이 없거나 NULL값인 경우는 그냥('없이) query문에 들어가고, 아닌 경우는 '를 붙혀서 query문에 넣는다!
                if user_list[i] == "" or user_list[i] == NULL or user_list[i] == None:
                    user_list[i] = NULL
                    query += user_list[i]

                else:
                    query += "'" + user_list[i] + "'"

                if i != len(user_list) - 1:
                    query += ", "
            
            ask = "ID: {}\t이름: {}\t주민등록번호: {}\n전화번호: {}\t자격증: {}\n주소: {}\n본적주소: {}\n기수: {}\t반: {}\t 대체실습: {}\n총 이수시간: {}\t이론이수: {}\t실습이수: {}\t실기이수: {}\n시험회차: {}회"\
                .format(user_list[0], user_list[1], user_list[2], user_list[3], user_list[4], user_list[5], user_list[6], user_list[7], user_list[8], user_list[13], user_list[9], user_list[10], user_list[11], user_list[12], user_list[14])
            ask += "\n해당 정보로 업데이트합니다."
                
        elif self.targetTable == "lecture":
            if self.textClsN_lecture.text().strip() == "" or self.textClsT_lecture.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 반을 입력해야 합니다!")
                return

            lect_list = []
            lect_list.append(self.textClsN_lecture.text().strip())
            lect_list.append(self.textClsT_lecture.text().strip())
            lect_list.append(self.textStartD_lecture.text().strip())
            lect_list.append(self.textEndD_lecture.text().strip())

            query_list = ["classNumber", "classTime", "startDate", "endDate"]

            where = "classNumber = '{}' and classTime = '{}'".format(self.key_dict["기수"], self.key_dict["반"])

            query = ""
            for i in range(len(lect_list)):
                query += query_list[i] + "="

                if lect_list[i] == "" or lect_list[i] == NULL or lect_list[i] == None:
                    lect_list[i] = NULL
                    query += lect_list[i]

                else:
                    query += "'" + lect_list[i] + "'"

                if i != len(lect_list) - 1:
                    query += ", "

            ask = "기수: {}\t반: {}\n시작일: {}\n종료일: {}\n".format(lect_list[0], lect_list[1], lect_list[2], lect_list[3])
            ask += "\n해당 정보로 업데이트합니다."

        elif self.targetTable == "teacher":
            if self.textID_teacher.text().strip() == "" or self.textName_teacher.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return
            
            teach_list = []
            teach_list.append(self.textID_teacher.text().strip())
            teach_list.append(self.textCateg.text().strip())
            teach_list.append(self.textName_teacher.text().strip())
            teach_list.append(self.textDOB.text().strip())
            teach_list.append(self.textLicen_teacher.text().strip())
            teach_list.append(self.textMinC.text().strip())
            teach_list.append(self.textACK.text().strip())

            query_list = ["id", "category", "name", "dateOfBirth", "license", "minCareer", "ACKDate"]

            where = "id = '{}' and name = '{}'".format(self.key_dict["ID"], self.key_dict["name"])

            query = ""
            for i in range(len(teach_list)):
                query += query_list[i] + "="

                if teach_list[i] == "" or teach_list[i] == NULL or teach_list[i] == None:
                    teach_list[i] = NULL
                    query += teach_list[i]

                else:
                    query += "'" + teach_list[i] + "'"

                if i != len(teach_list) - 1:
                    query += ", "

            ask = "ID: {}\t이름: {}\t자격증: {}\n생년월일: {}\t구분: {}\n최소경력: {}\n도 승인일자: {}\n"\
                .format(teach_list[0], teach_list[1], teach_list[2], teach_list[3], teach_list[4], teach_list[5], teach_list[6])
            ask += "\n해당 정보로 업데이트합니다."

        elif self.targetTable == "temptraining":
            if self.textClsN_tempTrain.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수를 입력해야 합니다!")
                return

            temp_list = []
            temp_list.append(self.textClsN_tempTrain.text().strip())
            temp_list.append(self.textStartD_tempTrain.text().strip())
            temp_list.append(self.textEndD_tempTrain.text().strip())
            temp_list.append(self.textAwardD.text().strip())

            query_list = ["classNumber", "startDate", "endDate", "awardDate"]

            where = "classNumber = '{}'".format(self.key_dict["기수"])

            query = ""
            for i in range(len(temp_list)):
                query += query_list[i] + "="

                if temp_list[i] == "" or temp_list[i] == NULL or temp_list[i] == None:
                    temp_list[i] = NULL
                    query += temp_list[i]

                else:
                    query += "'" + temp_list[i] + "'"

                if i != len(temp_list) - 1:
                    query += ", "

            ask = "기수: {}\n시작일: {}\n종료일: {}\n수여일: {}\n".format(temp_list[0], temp_list[1], temp_list[2], temp_list[3])
            ask += "\n해당 정보로 업데이트합니다."

        elif self.targetTable == "temptrainingteacher":
            if self.textClsN_tempTrainT.text().strip() == "" or self.textTeach.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 담당강사를 입력해야 합니다!")
                return

            tempT_list = []
            tempT_list.append(self.textClsN_tempTrainT.text().strip())
            tempT_list.append(self.textTeach.text().strip())

            query_list = ["classNumber", "teacherName"]

            where = "classNumber = '{}' and teacherName = '{}'".format(self.key_dict["기수"], self.key_dict["강사"])

            query = ""
            for i in range(len(tempT_list)):
                query += query_list[i] + "="
                if tempT_list[i] == "" or tempT_list[i] == NULL or tempT_list[i] == None:
                    tempT_list[i] = NULL
                    query += tempT_list[i]

                else:
                    query += "'" + tempT_list[i] + "'"

                if i != len(tempT_list) - 1:
                    query += ", "

            ask = "기수: {}\n강사: {}\n".format(tempT_list[0], tempT_list[1])
            ask += "\n해당 정보로 업데이트합니다."


        ans = QMessageBox.question(self, "데이터 수정 확인", ask, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            db.main.dbPrograms.UPDATE(self.targetTable, query, where)
            QMessageBox.about(self, "완료", "데이터를 성공적으로 수정했습니다.")
            db.main.showTable(Refresh=True)
            db.main.textInfo.clear()

            if self.targetTable == "user":
                name = self.textName_user.text().strip()
                number = self.textClsN_user.text().strip()
                time = self.textClsT_user.text().strip()

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

    def showEvent(self, QShowEvent):
        self.key_dict = {}
        self.lineEditList = []
        cnt_row = 0
        cnt_col = 0
        # 1. 기존에 있던 label과 Line Edit 삭제
        for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().deleteLater()
                # self.grid.itemAt(i).widget().hide()

        # 2. 공통으로 들어갈 insert 버튼과 close 버튼 생성
        self.btnUpdate = QPushButton("Update", self)
        self.btnUpdate.clicked.connect(self.dataUpdate)
        self.btnCancel = QPushButton("Close", self)
        self.btnCancel.clicked.connect(self.close)
        
        # 3. 현재 테이블에 맞는 label 및 Line Edit 생성 및 추가
        if db.main.curTable == "user":
            self.targetTable = "user"
            self.setWindowTitle("데이터 수정 - 수강생")
            cnt_row = 7
            cnt_col = 6
            self.resize(600, 400)

            self.labelID_user = QLabel("ID", self)
            self.labelID_user.setFixedWidth(90)
            self.labelID_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelID_user, 0, 0)
            self.textID_user = QLineEdit()
            self.grid.addWidget(self.textID_user, 0, 1)
            self.lineEditList.append(self.textID_user)
            self.labelName_user = QLabel("이름", self)
            self.labelName_user.setFixedWidth(90)
            self.labelName_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelName_user, 0, 2)
            self.textName_user = QLineEdit()
            self.grid.addWidget(self.textName_user, 0, 3)
            self.lineEditList.append(self.textName_user)
            self.labelLicen_user = QLabel("자격증", self)
            self.labelLicen_user.setFixedWidth(90)
            self.labelLicen_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelLicen_user, 0, 4)
            self.textLicen_user = QLineEdit()
            self.grid.addWidget(self.textLicen_user, 0, 5)
            self.lineEditList.append(self.textLicen_user)

            self.labelClsN_user = QLabel("기수", self)
            self.labelClsN_user.setFixedWidth(90)
            self.labelClsN_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_user, 1, 0)
            self.textClsN_user = QLineEdit()
            self.grid.addWidget(self.textClsN_user, 1, 1)
            self.lineEditList.append(self.textClsN_user)
            self.labelClsT_user = QLabel("반", self)
            self.labelClsT_user.setFixedWidth(90)
            self.labelClsT_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsT_user, 1, 2)
            self.textClsT_user = QLineEdit()
            self.grid.addWidget(self.textClsT_user, 1, 3)
            self.lineEditList.append(self.textClsT_user)
            self.labelTemp = QLabel("대체실습", self)
            self.labelTemp.setFixedWidth(90)
            self.labelTemp.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelTemp, 1, 4)
            self.textTemp = QLineEdit()
            self.grid.addWidget(self.textTemp, 1, 5)
            self.lineEditList.append(self.textTemp)

            self.labelRRN = QLabel("주민등록번호", self)
            self.labelRRN.setFixedWidth(90)
            self.labelRRN.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelRRN, 2, 0)
            self.textRRN = QLineEdit()
            self.grid.addWidget(self.textRRN, 2, 1, 1, 2)
            self.lineEditList.append(self.textRRN)
            self.labelPhone = QLabel("전화번호", self)
            self.labelPhone.setFixedWidth(90)
            self.labelPhone.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelPhone, 2, 3)
            self.textPhone = QLineEdit()
            self.grid.addWidget(self.textPhone, 2, 4, 1, 2)
            self.lineEditList.append(self.textPhone)
            
            
            self.labelAdr = QLabel("주소", self)
            self.labelAdr.setFixedWidth(90)
            self.labelAdr.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelAdr, 3, 0)
            self.textAdr = QLineEdit()
            self.grid.addWidget(self.textAdr, 3, 1, 1, 5)
            self.lineEditList.append(self.textAdr)
            self.labelOriginAdr = QLabel("본적주소", self)
            self.labelOriginAdr.setFixedWidth(90)
            self.labelOriginAdr.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelOriginAdr, 4, 0)
            self.textOriginAdr = QLineEdit()
            self.grid.addWidget(self.textOriginAdr, 4, 1, 1, 5)
            self.lineEditList.append(self.textOriginAdr)

            self.labelTotalT = QLabel("총 이수시간은 이론 + 실기 + 실습 이수시간으로 입력됩니다.")
            self.grid.addWidget(self.labelTotalT, 5, 0, 1, 6)

            self.labelTheT = QLabel("이론이수")
            self.labelTheT.setFixedWidth(90)
            self.labelTheT.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelTheT, 6, 0)
            self.textTheT = QLineEdit()
            self.grid.addWidget(self.textTheT, 6, 1)
            self.lineEditList.append(self.textTheT)

            self.labelPracT = QLabel("실기이수")
            self.labelPracT.setFixedWidth(90)
            self.labelPracT.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelPracT, 6, 2)
            self.textPracT = QLineEdit()
            self.grid.addWidget(self.textPracT, 6, 3)
            self.lineEditList.append(self.textPracT)

            self.labelTrainT = QLabel("실습이수")
            self.labelTrainT.setFixedWidth(90)
            self.labelTrainT.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelTrainT, 6, 4)
            self.textTrainT = QLineEdit()
            self.grid.addWidget(self.textTrainT, 6, 5)
            self.lineEditList.append(self.textTrainT)

            self.labelExam = QLabel("시험회차")
            self.labelExam.setFixedWidth(90)
            self.labelExam.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelExam, 7, 0)
            self.textExam = QLineEdit()
            self.grid.addWidget(self.textExam, 7, 1)
            self.lineEditList.append(self.textExam)

            input_user = []
            for i in range(15):
                input_user.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_user[i] == None or input_user[i] == NULL or input_user[i] == "" or input_user[i] == "None" or input_user[i] == "NULL":
                    input_user[i] = ""

            self.textID_user.setText(str(input_user[0]))
            self.textName_user.setText(str(input_user[1]))
            self.textLicen_user.setText(str(input_user[4]))
            self.textClsN_user.setText(str(input_user[7]))
            self.textClsT_user.setText(str(input_user[8]))
            self.textTemp.setText(str(input_user[13]))
            self.textRRN.setText(str(input_user[2]))
            self.textPhone.setText(str(input_user[3]))
            self.textAdr.setText(str(input_user[5]))
            self.textOriginAdr.setText(str(input_user[6]))
            self.textTheT.setText(str(input_user[10]))
            self.textPracT.setText(str(input_user[11]))
            self.textTrainT.setText(str(input_user[12]))
            self.textExam.setText(str(input_user[14]))

            self.key_dict["ID"] = str(input_user[0])
            self.key_dict["name"] = str(input_user[1])
            self.key_dict["RRN"] = str(input_user[2])
            self.key_dict["기수"] = str(input_user[7])
            self.key_dict["반"] = str(input_user[8])
            self.key_dict["자격증"] = str(input_user[4])

        elif db.main.curTable == "lecture":
            self.targetTable = "lecture"
            self.setWindowTitle("데이터 수정 - 기수")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.labelClsN_lecture = QLabel("기수", self)
            self.labelClsN_lecture.setFixedWidth(90)
            self.labelClsN_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_lecture, 0, 0)
            self.textClsN_lecture = QLineEdit()
            self.textClsN_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textClsN_lecture, 0, 1)
            self.lineEditList.append(self.textClsN_lecture)
            self.labelClsT_lecture = QLabel("반", self)
            self.labelClsT_lecture.setFixedWidth(90)
            self.labelClsT_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsT_lecture, 0, 2)
            self.textClsT_lecture = QLineEdit()
            self.textClsT_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textClsT_lecture, 0, 3)
            self.lineEditList.append(self.textClsT_lecture)
            self.labelStartD_lecture = QLabel("시작일", self)
            self.labelStartD_lecture.setFixedWidth(90)
            self.labelStartD_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelStartD_lecture, 1, 0)
            self.textStartD_lecture = QLineEdit()
            self.textStartD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textStartD_lecture, 1, 1)
            self.lineEditList.append(self.textStartD_lecture)
            self.labelEndD_lecture = QLabel("종료일", self)
            self.labelEndD_lecture.setFixedWidth(90)
            self.labelEndD_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelEndD_lecture, 1, 2)
            self.textEndD_lecture = QLineEdit()
            self.textEndD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textEndD_lecture, 1, 3)
            self.lineEditList.append(self.textEndD_lecture)

            input_lecture = []
            for i in range(4):
                input_lecture.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_lecture[i] == None or input_lecture[i] == NULL or input_lecture[i] == "" or input_lecture[i] == "None" or input_lecture[i] == "NULL":
                    input_lecture[i] = ""

            self.textClsN_lecture.setText(str(input_lecture[0]))
            self.textClsT_lecture.setText(str(input_lecture[1]))
            self.textStartD_lecture.setText(str(input_lecture[2]))
            self.textEndD_lecture.setText(str(input_lecture[3]))

            self.key_dict["기수"] = str(input_lecture[0])
            self.key_dict["반"] = str(input_lecture[1])

        elif db.main.curTable == "teacher":
            self.targetTable = "teacher"
            self.setWindowTitle("데이터 수정 - 강사")
            cnt_row = 3
            cnt_col = 6
            self.resize(400, 200)
            self.labelID_teacher = QLabel("ID", self)
            self.labelID_teacher.setFixedWidth(90)
            self.labelID_teacher.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelID_teacher, 0, 0)
            self.textID_teacher = QLineEdit()
            self.grid.addWidget(self.textID_teacher, 0, 1)
            self.lineEditList.append(self.textID_teacher)
            self.labelName_teacher = QLabel("이름", self)
            self.labelName_teacher.setFixedWidth(90)
            self.labelName_teacher.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelName_teacher, 0, 2)
            self.textName_teacher = QLineEdit()
            self.grid.addWidget(self.textName_teacher, 0, 3)
            self.lineEditList.append(self.textName_teacher)
            self.labelLicen_teacher = QLabel("자격증", self)
            self.labelLicen_teacher.setFixedWidth(90)
            self.labelLicen_teacher.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelLicen_teacher, 0, 4)
            self.textLicen_teacher = QLineEdit()
            self.grid.addWidget(self.textLicen_teacher, 0, 5)
            self.lineEditList.append(self.textLicen_teacher)
            self.labelDOB = QLabel("생년월일", self)
            self.labelDOB.setFixedWidth(90)
            self.labelDOB.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelDOB, 1, 0)
            self.textDOB = QLineEdit()
            self.grid.addWidget(self.textDOB, 1, 1, 1, 2)
            self.lineEditList.append(self.textDOB)
            self.labelCateg = QLabel("전임/외래", self)
            self.labelCateg.setFixedWidth(90)
            self.labelCateg.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelCateg, 1, 3)
            self.textCateg = QLineEdit()
            self.grid.addWidget(self.textCateg, 1, 4, 1, 2)
            self.lineEditList.append(self.textCateg)
            self.labelMinC = QLabel("최소경력", self)
            self.labelMinC.setFixedWidth(90)
            self.labelMinC.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelMinC, 2, 0)
            self.textMinC = QLineEdit()
            self.grid.addWidget(self.textMinC, 2, 1, 1, 2)
            self.lineEditList.append(self.textMinC)
            self.labelACK = QLabel("도 승인일자")
            self.labelACK.setFixedWidth(90)
            self.labelACK.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelACK, 2, 3)
            self.textACK = QLineEdit()
            self.grid.addWidget(self.textACK, 2, 4, 1, 2)
            self.lineEditList.append(self.textACK)

            input_teacher = []
            for i in range(7):
                input_teacher.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_teacher[i] == None or input_teacher[i] == NULL or input_teacher[i] == "" or input_teacher[i] == "None" or input_teacher[i] == "NULL":
                    input_teacher[i] = ""

            self.textID_teacher.setText(str(input_teacher[0]))
            self.textName_teacher.setText(str(input_teacher[2]))
            self.textLicen_teacher.setText(str(input_teacher[4]))
            self.textDOB.setText(str(input_teacher[3]))
            self.textCateg.setText(str(input_teacher[1]))
            self.textMinC.setText(str(input_teacher[5]))
            self.textACK.setText(str(input_teacher[6]))

            self.key_dict["ID"] = str(input_teacher[0])
            self.key_dict["name"] = str(input_teacher[2])

        elif db.main.curTable == "temptraining":
            self.targetTable = "temptraining"
            self.setWindowTitle("데이터 수정 - 대체실습")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.labelClsN_tempTrain = QLabel("기수", self)
            self.labelClsN_tempTrain.setFixedWidth(90)
            self.labelClsN_tempTrain.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_tempTrain, 0, 0)
            self.textClsN_tempTrain = QLineEdit()
            self.textClsN_tempTrain.setFixedWidth(120)
            self.grid.addWidget(self.textClsN_tempTrain, 0, 1)
            self.lineEditList.append(self.textClsN_tempTrain)
            self.labelStartD_tempTrain = QLabel("시작일", self)
            self.labelStartD_tempTrain.setFixedWidth(90)
            self.labelStartD_tempTrain.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelStartD_tempTrain, 0, 2)
            self.textStartD_tempTrain = QLineEdit()
            self.textStartD_tempTrain.setFixedWidth(120)
            self.grid.addWidget(self.textStartD_tempTrain, 0, 3)
            self.lineEditList.append(self.textStartD_tempTrain)
            self.labelEndD_tempTrain = QLabel("종료일", self)
            self.labelEndD_tempTrain.setFixedWidth(90)
            self.labelEndD_tempTrain.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelEndD_tempTrain, 1, 0)
            self.textEndD_tempTrain = QLineEdit()
            self.textEndD_tempTrain.setFixedWidth(120)
            self.grid.addWidget(self.textEndD_tempTrain, 1, 1)
            self.lineEditList.append(self.textEndD_tempTrain)
            self.labelAwardD = QLabel("수여일", self)
            self.labelAwardD.setFixedWidth(90)
            self.labelAwardD.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelAwardD, 1, 2)
            self.textAwardD = QLineEdit()
            self.textAwardD.setFixedWidth(120)
            self.grid.addWidget(self.textAwardD, 1, 3)
            self.lineEditList.append(self.textAwardD)

            input_tempTrain = []
            for i in range(4):
                input_tempTrain.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_tempTrain[i] == None or input_tempTrain[i] == NULL or input_tempTrain[i] == "" or input_tempTrain[i] == "None" or input_tempTrain[i] == "NULL":
                    input_tempTrain[i] = ""

            self.textClsN_tempTrain.setText(str(input_tempTrain[0]))
            self.textStartD_tempTrain.setText(str(input_tempTrain[1]))
            self.textEndD_tempTrain.setText(str(input_tempTrain[2]))
            self.textAwardD.setText(str(input_tempTrain[3]))

            self.key_dict["기수"] = str(input_tempTrain[0])

        elif db.main.curTable == "temptrainingteacher":
            self.targetTable = "temptrainingteacher"
            self.setWindowTitle("데이터 수정 - 대체실습 강사")
            cnt_row = 2
            cnt_col = 2
            self.resize(300, 200)
            self.labelClsN_tempTrainT = QLabel("기수", self)
            self.labelClsN_tempTrainT.setFixedWidth(90)
            self.labelClsN_tempTrainT.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_tempTrainT, 0, 0)
            self.textClsN_tempTrainT = QLineEdit()
            self.textClsN_tempTrainT.setFixedWidth(90)
            self.grid.addWidget(self.textClsN_tempTrainT, 0, 1)
            self.lineEditList.append(self.textClsN_tempTrainT)
            self.labelTeach = QLabel("강사", self)
            self.labelTeach.setFixedWidth(90)
            self.labelTeach.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelTeach, 1, 0)
            self.textTeach = QLineEdit()
            self.textTeach.setFixedWidth(90)
            self.grid.addWidget(self.textTeach, 1, 1)
            self.lineEditList.append(self.textTeach)

            input_tempTrainT = []
            for i in range(2):
                input_tempTrainT.append(db.main.readDB.index(db.main.table.currentIndex().row(), i).data())

                if input_tempTrainT[i] == None or input_tempTrainT[i] == NULL or input_tempTrainT[i] == "" or input_tempTrainT[i] == "None" or input_tempTrainT[i] == "NULL":
                    input_tempTrainT[i] = ""

            self.textClsN_tempTrainT.setText(str(input_tempTrainT[0]))
            self.textTeach.setText(str(input_tempTrainT[1]))

            self.key_dict["기수"] = str(input_tempTrainT[0])
            self.key_dict["강사"] = str(input_tempTrainT[1])
        
        # 4. 재생성된 버튼 추가
        self.grid.addWidget(self.btnUpdate, cnt_row, cnt_col - 2)
        self.grid.addWidget(self.btnCancel, cnt_row, cnt_col - 1)
        for lineEdit in self.lineEditList:
            lineEdit.returnPressed.connect(self.dataUpdate)


class INSERT(QWidget):
    # 새 창을 띄우기 위해 서로 global로 연결
    global db

    def __init__(self):
        super().__init__()
        self.initUI()
        self.targetTable = ""
        self.base_path = "D:\\남양노아요양보호사교육원\\교육생관리"

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
        if self.targetTable == "user":
            if self.textID_user.text().strip() == "" or self.textName_user.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return

            user_list = []
            user_list.append(self.textID_user.text().strip())
            user_list.append(self.textName_user.text().strip())
            user_list.append(self.textRRN.text().strip())
            user_list.append(self.textPhone.text().strip())
            user_list.append(self.textLicen_user.text().strip())
            user_list.append(self.textAdr.text().strip())
            user_list.append(self.textOriginAdr.text().strip())
            user_list.append(self.textClsN_user.text().strip())
            user_list.append(self.textClsT_user.text().strip())
            # 총 이수, 이론, 실기, 실습 시간으로 NULL값 추가
            user_list.append(NULL)
            user_list.append(NULL)
            user_list.append(NULL)
            user_list.append(NULL)
            user_list.append(self.textTemp.text().strip())
            # 시험 회차 정보는 데이터 수정에서 입력
            user_list.append(NULL)

            query = ""
            for i in range(len(user_list)):
                # 값이 없거나 NULL값인 경우는 그냥('없이) query문에 들어가고, 아닌 경우는 '를 붙혀서 query문에 넣는다!
                if user_list[i] == "" or user_list[i] == NULL or user_list[i] == None:
                    user_list[i] = NULL
                    query += user_list[i]

                else:
                    query += "'" + user_list[i] + "'"

                if i != len(user_list) - 1:
                    query += ", "
            
            ask = "ID: {}\t이름: {}\t주민등록번호: {}\n전화번호: {}\t자격증: {}\n주소: {}\n본적주소: {}\n기수: {}\t반: {}\t 대체실습: {}\n총 이수시간: {}\t이론이수: {}\t실습이수: {}\t 실기이수: {}\n"\
                .format(user_list[0], user_list[1], user_list[2], user_list[3], user_list[4], user_list[5], user_list[6], user_list[7], user_list[8], user_list[13], user_list[9], user_list[10], user_list[11], user_list[12])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."
                
        elif self.targetTable == "lecture":
            if self.textClsN_lecture.text().strip() == "" or self.textClsT_lecture.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 반을 입력해야 합니다!")
                return

            lect_list = []
            lect_list.append(self.textClsN_lecture.text().strip())
            lect_list.append(self.textClsT_lecture.text().strip())
            lect_list.append(self.textStartD_lecture.text().strip())
            lect_list.append(self.textEndD_lecture.text().strip())

            query = ""
            for i in range(len(lect_list)):
                if lect_list[i] == "" or lect_list[i] == NULL or lect_list[i] == None:
                    lect_list[i] = NULL
                    query += lect_list[i]

                else:
                    query += "'" + lect_list[i] + "'"

                if i != len(lect_list) - 1:
                    query += ", "

            ask = "기수: {}\t반: {}\n시작일: {}\n종료일: {}\n".format(lect_list[0], lect_list[1], lect_list[2], lect_list[3])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."

        elif self.targetTable == "teacher":
            if self.textID_teacher.text().strip() == "" or self.textName_teacher.text().strip() == "":
                QMessageBox.warning(self, "오류", "ID, 이름값을 입력해야 합니다!")
                return
            
            teach_list = []
            teach_list.append(self.textID_teacher.text().strip())
            teach_list.append(self.textCateg.text().strip())
            teach_list.append(self.textName_teacher.text().strip())
            teach_list.append(self.textDOB.text().strip())
            teach_list.append(self.textLicen_teacher.text().strip())
            teach_list.append(self.textMinC.text().strip())
            teach_list.append(self.textACK.text().strip())

            query = ""
            for i in range(len(teach_list)):
                if teach_list[i] == "" or teach_list[i] == NULL or teach_list[i] == None:
                    teach_list[i] = NULL
                    query += teach_list[i]

                else:
                    query += "'" + teach_list[i] + "'"

                if i != len(teach_list) - 1:
                    query += ", "

            ask = "ID: {}\t이름: {}\t자격증: {}\n생년월일: {}\t구분: {}\n최소경력: {}\n도 승인일자: {}\n"\
                .format(teach_list[0], teach_list[1], teach_list[2], teach_list[3], teach_list[4], teach_list[5], teach_list[6])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."

        elif self.targetTable == "temptraining":
            if self.textClsN_tempTrain.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수를 입력해야 합니다!")
                return

            temp_list = []
            temp_list.append(self.textClsN_tempTrain.text().strip())
            temp_list.append(self.textStartD_tempTrain.text().strip())
            temp_list.append(self.textEndD_tempTrain.text().strip())
            temp_list.append(self.textAwardD.text().strip())

            query = ""
            for i in range(len(temp_list)):
                if temp_list[i] == "" or temp_list[i] == NULL or temp_list[i] == None:
                    temp_list[i] = NULL
                    query += temp_list[i]

                else:
                    query += "'" + temp_list[i] + "'"

                if i != len(temp_list) - 1:
                    query += ", "

            ask = "기수: {}\n시작일: {}\n종료일: {}\n수여일: {}\n".format(temp_list[0], temp_list[1], temp_list[2], temp_list[3])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."

        elif self.targetTable == "temptrainingteacher":
            if self.textClsN_tempTrainT.text().strip() == "" or self.textTeach.text().strip() == "":
                QMessageBox.warning(self, "오류", "기수, 담당강사를 입력해야 합니다!")
                return

            tempT_list = []
            tempT_list.append(self.textClsN_tempTrainT.text().strip())
            tempT_list.append(self.textTeach.text().strip())

            query = ""
            for i in range(len(tempT_list)):
                if tempT_list[i] == "" or tempT_list[i] == NULL or tempT_list[i] == None:
                    tempT_list[i] = NULL
                    query += tempT_list[i]

                else:
                    query += "'" + tempT_list[i] + "'"

                if i != len(tempT_list) - 1:
                    query += ", "

            ask = "기수: {}\n강사: {}\n".format(tempT_list[0], tempT_list[1])
            ask += "\n해당 정보를 데이터베이스에 추가합니다."


        ans = QMessageBox.question(self, "데이터 삽입 확인", ask, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            db.main.dbPrograms.INSERT(self.targetTable, query)
            QMessageBox.about(self, "완료", "데이터를 성공적으로 추가했습니다.")
            if self.targetTable == "user":
                name = self.textName_user.text().strip()
                number = self.textClsN_user.text().strip()
                time = self.textClsT_user.text().strip()

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

    def showEvent(self, QShowEvent):
        self.lineEditList = []

        cnt_row = 0
        cnt_col = 0
        # 1. 기존에 있던 label과 Line Edit 삭제
        for i in reversed(range(self.grid.count())):
                self.grid.itemAt(i).widget().deleteLater()
                # self.grid.itemAt(i).widget().hide()

        # 2. 공통으로 들어갈 insert 버튼과 close 버튼 생성
        self.btnInsert = QPushButton("Insert", self)
        self.btnInsert.clicked.connect(self.dataInsert)
        self.btnCancel = QPushButton("Close", self)
        self.btnCancel.clicked.connect(self.close)
        
        # 3. 현재 테이블에 맞는 label 및 Line Edit 생성 및 추가
        if db.main.curTable == "user":
            self.targetTable = "user"
            self.setWindowTitle("데이터 삽입 - 수강생")
            cnt_row = 5
            cnt_col = 6
            self.resize(600, 400)

            self.labelID_user = QLabel("ID", self)
            self.labelID_user.setFixedWidth(90)
            self.labelID_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelID_user, 0, 0)
            self.textID_user = QLineEdit()
            self.grid.addWidget(self.textID_user, 0, 1)
            self.lineEditList.append(self.textID_user)
            self.labelName_user = QLabel("이름", self)
            self.labelName_user.setFixedWidth(90)
            self.labelName_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelName_user, 0, 2)
            self.textName_user = QLineEdit()
            self.grid.addWidget(self.textName_user, 0, 3)
            self.lineEditList.append(self.textName_user)
            self.labelLicen_user = QLabel("자격증", self)
            self.labelLicen_user.setFixedWidth(90)
            self.labelLicen_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelLicen_user, 0, 4)
            self.textLicen_user = QLineEdit()
            self.grid.addWidget(self.textLicen_user, 0, 5)
            self.lineEditList.append(self.textLicen_user)

            self.labelClsN_user = QLabel("기수", self)
            self.labelClsN_user.setFixedWidth(90)
            self.labelClsN_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_user, 1, 0)
            self.textClsN_user = QLineEdit()
            self.grid.addWidget(self.textClsN_user, 1, 1)
            self.lineEditList.append(self.textClsN_user)
            self.labelClsT_user = QLabel("반", self)
            self.labelClsT_user.setFixedWidth(90)
            self.labelClsT_user.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsT_user, 1, 2)
            self.textClsT_user = QLineEdit()
            self.grid.addWidget(self.textClsT_user, 1, 3)
            self.lineEditList.append(self.textClsT_user)
            self.labelTemp = QLabel("대체실습", self)
            self.labelTemp.setFixedWidth(90)
            self.labelTemp.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelTemp, 1, 4)
            self.textTemp = QLineEdit()
            self.grid.addWidget(self.textTemp, 1, 5)
            self.lineEditList.append(self.textTemp)

            self.labelRRN = QLabel("주민등록번호", self)
            self.labelRRN.setFixedWidth(90)
            self.labelRRN.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelRRN, 2, 0)
            self.textRRN = QLineEdit()
            self.grid.addWidget(self.textRRN, 2, 1, 1, 2)
            self.lineEditList.append(self.textRRN)
            self.labelPhone = QLabel("전화번호", self)
            self.labelPhone.setFixedWidth(90)
            self.labelPhone.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelPhone, 2, 3)
            self.textPhone = QLineEdit()
            self.grid.addWidget(self.textPhone, 2, 4, 1, 2)
            self.lineEditList.append(self.textPhone)
            
            
            self.labelAdr = QLabel("주소", self)
            self.labelAdr.setFixedWidth(90)
            self.labelAdr.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelAdr, 3, 0)
            self.textAdr = QLineEdit()
            self.grid.addWidget(self.textAdr, 3, 1, 1, 5)
            self.lineEditList.append(self.textAdr)
            self.labelOriginAdr = QLabel("본적주소", self)
            self.labelOriginAdr.setFixedWidth(90)
            self.labelOriginAdr.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelOriginAdr, 4, 0)
            self.textOriginAdr = QLineEdit()
            self.grid.addWidget(self.textOriginAdr, 4, 1, 1, 5)
            self.lineEditList.append(self.textOriginAdr)

            self.textID_user.setFocus()

        elif db.main.curTable == "lecture":
            self.targetTable = "lecture"
            self.setWindowTitle("데이터 삽입 - 기수")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.labelClsN_lecture = QLabel("기수", self)
            self.labelClsN_lecture.setFixedWidth(90)
            self.labelClsN_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_lecture, 0, 0)
            self.textClsN_lecture = QLineEdit()
            self.textClsN_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textClsN_lecture, 0, 1)
            self.lineEditList.append(self.textClsN_lecture)
            self.labelClsT_lecture = QLabel("반", self)
            self.labelClsT_lecture.setFixedWidth(90)
            self.labelClsT_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsT_lecture, 0, 2)
            self.textClsT_lecture = QLineEdit()
            self.textClsT_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textClsT_lecture, 0, 3)
            self.lineEditList.append(self.textClsT_lecture)
            self.labelStartD_lecture = QLabel("시작일", self)
            self.labelStartD_lecture.setFixedWidth(90)
            self.labelStartD_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelStartD_lecture, 1, 0)
            self.textStartD_lecture = QLineEdit()
            self.textStartD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textStartD_lecture, 1, 1)
            self.lineEditList.append(self.textStartD_lecture)
            self.labelEndD_lecture = QLabel("종료일", self)
            self.labelEndD_lecture.setFixedWidth(90)
            self.labelEndD_lecture.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelEndD_lecture, 1, 2)
            self.textEndD_lecture = QLineEdit()
            self.textEndD_lecture.setFixedWidth(120)
            self.grid.addWidget(self.textEndD_lecture, 1, 3)
            self.lineEditList.append(self.textEndD_lecture)

        elif db.main.curTable == "teacher":
            self.targetTable = "teacher"
            self.setWindowTitle("데이터 삽입 - 강사")
            cnt_row = 3
            cnt_col = 6
            self.resize(400, 200)
            self.labelID_teacher = QLabel("ID", self)
            self.labelID_teacher.setFixedWidth(90)
            self.labelID_teacher.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelID_teacher, 0, 0)
            self.textID_teacher = QLineEdit()
            self.grid.addWidget(self.textID_teacher, 0, 1)
            self.lineEditList.append(self.textID_teacher)
            self.labelName_teacher = QLabel("이름", self)
            self.labelName_teacher.setFixedWidth(90)
            self.labelName_teacher.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelName_teacher, 0, 2)
            self.textName_teacher = QLineEdit()
            self.grid.addWidget(self.textName_teacher, 0, 3)
            self.lineEditList.append(self.textName_teacher)
            self.labelLicen_teacher = QLabel("자격증", self)
            self.labelLicen_teacher.setFixedWidth(90)
            self.labelLicen_teacher.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelLicen_teacher, 0, 4)
            self.textLicen_teacher = QLineEdit()
            self.grid.addWidget(self.textLicen_teacher, 0, 5)
            self.lineEditList.append(self.textLicen_teacher)
            self.labelDOB = QLabel("생년월일", self)
            self.labelDOB.setFixedWidth(90)
            self.labelDOB.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelDOB, 1, 0)
            self.textDOB = QLineEdit()
            self.grid.addWidget(self.textDOB, 1, 1, 1, 2)
            self.lineEditList.append(self.textDOB)
            self.labelCateg = QLabel("전임/외래", self)
            self.labelCateg.setFixedWidth(90)
            self.labelCateg.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelCateg, 1, 3)
            self.textCateg = QLineEdit()
            self.grid.addWidget(self.textCateg, 1, 4, 1, 2)
            self.lineEditList.append(self.textCateg)
            self.labelMinC = QLabel("최소경력", self)
            self.labelMinC.setFixedWidth(90)
            self.labelMinC.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelMinC, 2, 0)
            self.textMinC = QLineEdit()
            self.grid.addWidget(self.textMinC, 2, 1, 1, 2)
            self.lineEditList.append(self.textMinC)
            self.labelACK = QLabel("도 승인일자")
            self.labelACK.setFixedWidth(90)
            self.labelACK.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelACK, 2, 3)
            self.textACK = QLineEdit()
            self.grid.addWidget(self.textACK, 2, 4, 1, 2)
            self.lineEditList.append(self.textACK)

        elif db.main.curTable == "temptraining":
            self.targetTable = "temptraining"
            self.setWindowTitle("데이터 삽입 - 대체실습")
            cnt_row = 2
            cnt_col = 4
            self.resize(300, 200)
            self.labelClsN_tempTrain = QLabel("기수", self)
            self.labelClsN_tempTrain.setFixedWidth(90)
            self.labelClsN_tempTrain.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_tempTrain, 0, 0)
            self.textClsN_tempTrain = QLineEdit()
            self.textClsN_tempTrain.setFixedWidth(120)
            self.grid.addWidget(self.textClsN_tempTrain, 0, 1)
            self.lineEditList.append(self.textClsN_tempTrain)
            self.labelStartD_tempTrain = QLabel("시작일", self)
            self.labelStartD_tempTrain.setFixedWidth(90)
            self.labelStartD_tempTrain.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelStartD_tempTrain, 0, 2)
            self.textStartD_tempTrain = QLineEdit()
            self.textStartD_tempTrain.setFixedWidth(120)
            self.grid.addWidget(self.textStartD_tempTrain, 0, 3)
            self.lineEditList.append(self.textStartD_tempTrain)
            self.labelEndD_tempTrain = QLabel("종료일", self)
            self.labelEndD_tempTrain.setFixedWidth(90)
            self.labelEndD_tempTrain.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelEndD_tempTrain, 1, 0)
            self.textEndD_tempTrain = QLineEdit()
            self.textEndD_tempTrain.setFixedWidth(120)
            self.grid.addWidget(self.textEndD_tempTrain, 1, 1)
            self.lineEditList.append(self.textEndD_tempTrain)
            self.labelAwardD = QLabel("수여일", self)
            self.labelAwardD.setFixedWidth(90)
            self.labelAwardD.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelAwardD, 1, 2)
            self.textAwardD = QLineEdit()
            self.textAwardD.setFixedWidth(120)
            self.grid.addWidget(self.textAwardD, 1, 3)
            self.lineEditList.append(self.textAwardD)
            
        elif db.main.curTable == "temptrainingteacher":
            self.targetTable = "temptrainingteacher"
            self.setWindowTitle("데이터 삽입 - 대체실습 강사")
            cnt_row = 2
            cnt_col = 2
            self.resize(300, 200)
            self.labelClsN_tempTrainT = QLabel("기수", self)
            self.labelClsN_tempTrainT.setFixedWidth(90)
            self.labelClsN_tempTrainT.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelClsN_tempTrainT, 0, 0)
            self.textClsN_tempTrainT = QLineEdit()
            self.textClsN_tempTrainT.setFixedWidth(90)
            self.grid.addWidget(self.textClsN_tempTrainT, 0, 1)
            self.lineEditList.append(self.textClsN_tempTrainT)
            self.labelTeach = QLabel("강사", self)
            self.labelTeach.setFixedWidth(90)
            self.labelTeach.setAlignment(Qt.AlignRight)
            self.grid.addWidget(self.labelTeach, 1, 0)
            self.textTeach = QLineEdit()
            self.textTeach.setFixedWidth(90)
            self.grid.addWidget(self.textTeach, 1, 1)
            self.lineEditList.append(self.textTeach)

        # 4. 버튼을 추가하기 위한 row와 column check
        # 이거 왜 자꾸 증가하냐;
        # totalRow = self.grid.rowCount()
        # totalCol = self.grid.columnCount()
        
        # 5. 재생성된 버튼 추가
        self.grid.addWidget(self.btnInsert, cnt_row, cnt_col - 2)
        self.grid.addWidget(self.btnCancel, cnt_row, cnt_col - 1)
        for lineEdit in self.lineEditList:
            lineEdit.returnPressed.connect(self.dataInsert)

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

        self.curTable = ""

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

    def selected(self):
        if self.curTable == "user":
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

        elif self.curTable == "lecture":
            self.textInfo.clear()

            clsN = "기수: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            clsT = "반: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            startD = "시작일: " + str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            endD = "종료일: " + str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            send_string = clsN + "\n\n" + clsT + "\n\n" + startD + "\n\n" + endD
            
        elif self.curTable == "teacher":
            self.textInfo.clear()
            
            ID = "ID: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            categ = "분류: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            name = "이름: " + str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            DOB = "생년월일: " + str(self.readDB.index(self.table.currentIndex().row(), 3).data())
            licen = "자격증: " + str(self.readDB.index(self.table.currentIndex().row(), 4).data())
            career = "경력: " + str(self.readDB.index(self.table.currentIndex().row(), 5).data())
            ACKDate = "도 승인일자: " + str(self.readDB.index(self.table.currentIndex().row(), 6).data())

            send_string = ID + "\n\n" + categ + "\n\n" + DOB + "\n\n" + licen + "\n\n" + career + "\n\n" + ACKDate

        elif self.curTable == "temptraining":
            self.textInfo.clear()

            clsN = "기수: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            startD = "시작일: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            endD = "종료일: " + str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            awardD = "수여일: " + str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            send_string = clsN + "\n\n" + startD + "\n\n" + endD + "\n\n" + awardD
            
        elif self.curTable == "temptrainingteacher":
            self.textInfo.clear()

            clsN = "기수: " + str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            teacher = "반: " + str(self.readDB.index(self.table.currentIndex().row(), 1).data())

            send_string = clsN + "\n\n" + teacher

        self.textInfo.setText(send_string)


    def selectTable(self):
        if self.curTable == "user":
            self.readDB.setColumnCount(15)
            self.readDB.setHorizontalHeaderLabels(self.select_list_user)

        elif self.curTable == "lecture":
            self.readDB.setColumnCount(4)
            self.readDB.setHorizontalHeaderLabels(self.select_list_lecture)

        elif self.curTable == "teacher":
            self.readDB.setColumnCount(7)
            self.readDB.setHorizontalHeaderLabels(self.select_list_teacher)

        elif self.curTable == "temptraining":
            self.readDB.setColumnCount(4)
            self.readDB.setHorizontalHeaderLabels(self.select_list_temptraining)

        elif self.curTable == "temptrainingteacher":
            self.readDB.setColumnCount(2)
            self.readDB.setHorizontalHeaderLabels(self.select_list_temptrainingteacher)

    def showTable(self, Refresh=False):
        source = self.sender()
        self.changeCategory(Refresh=Refresh)
        self.readDB.clear()
        self.R_searchBox.clear()

        if Refresh == False:
            if source.text() == "수강생 관리":
                self.curTable = "user"
                order = "id"

                self.readDB.setColumnCount(15)
                self.readDB.setHorizontalHeaderLabels(self.select_list_user)

            elif source.text() == "기수 관리":
                self.curTable = "lecture"
                order = "classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_lecture)

            elif source.text() == "강사 관리":
                self.curTable = "teacher"
                order = "id"

                self.readDB.setColumnCount(7)
                self.readDB.setHorizontalHeaderLabels(self.select_list_teacher)


            elif source.text() == "대체실습":
                self.curTable = "temptraining"
                order = "classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptraining)

            elif source.text() == "대체실습 담당강사":
                self.curTable = "temptrainingteacher"
                order = "classNumber"

                self.readDB.setColumnCount(2)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptrainingteacher)

        elif Refresh == True:
            if self.curTable == "user":
                order = "id"

                self.readDB.setColumnCount(15)
                self.readDB.setHorizontalHeaderLabels(self.select_list_user)

            elif self.curTable == "lecture":
                order = "classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_lecture)

            elif self.curTable == "teacher":
                order = "id"

                self.readDB.setColumnCount(7)
                self.readDB.setHorizontalHeaderLabels(self.select_list_teacher)

            elif self.curTable == "temptraining":
                order = "classNumber"

                self.readDB.setColumnCount(4)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptraining)

            elif self.curTable == "temptrainingteacher":
                order = "classNumber"

                self.readDB.setColumnCount(2)
                self.readDB.setHorizontalHeaderLabels(self.select_list_temptrainingteacher)

        rs = self.dbPrograms.SELECT("*", self.curTable, orderBy=order)

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
            if self.curTable == "user":
                self.R_category.addItem("ID")
                self.R_category.addItem("이름")
                self.R_category.addItem("자격증")
                self.R_category.addItem("기수/반")
                self.R_category.addItem("대체실습")
                self.R_category.addItem("시험회차")
                self.R_category.addItem("SQL")

            elif self.curTable == "lecture":
                self.R_category.addItem("기수/반")
                self.R_category.addItem("SQL")

            elif self.curTable == "teacher":
                self.R_category.addItem("ID")
                self.R_category.addItem("이름")
                self.R_category.addItem("자격증")
                self.R_category.addItem("SQL")

            elif self.curTable == "temptraining":
                self.R_category.addItem("기수")
                # 시작일은 검색어 "이후"의 날짜들 모두, 종료일은 검색어 "이전"의 날짜들 모두
                # (시작일을 2022-01-01로 검색할 경우 1월 1일 이후에 시작하는 기수 검색)
                # (종료일을 2022-01-01로 검색할 경우 1월 1일 이전에 종료된 기수 검색)
                self.R_category.addItem("시작일")
                self.R_category.addItem("종료일")
                self.R_category.addItem("수여일")
                self.R_category.addItem("SQL")

            elif self.curTable == "temptrainingteacher":
                self.R_category.addItem("기수")
                self.R_category.addItem("강사")
                self.R_category.addItem("SQL")

    def search(self):
        keyWord = self.R_searchBox.text()
        if keyWord == "":
            QMessageBox.information(self, "검색어 오류", "검색어가 존재하지 않습니다!", QMessageBox.Yes, QMessageBox.Yes)
            return

        curTable = self.curTable
        curCategory = self.R_category.currentText()

        if curCategory == "ID":
            curCategory = "id"

        elif curCategory == "이름":
            curCategory = "name"

        elif curCategory == "자격증":
            curCategory = "license"

        elif curCategory == "기수/반":
            words = keyWord.split(" ")
            if len(words) == 1:
                if keyWord[-1] == "간":
                    curCategory = "classTime"

                else:
                    curCategory = "classNumber"
            
            elif len(words) == 2:
                if words[0][-1] == "간":
                    curCategory = "classTime = '{}' and classNumber".format(words[0])
                    keyWord = words[1]

                else:
                    curCategory = "classNumber = '{}' and classTime".format(words[0])
                    keyWord = words[1]

        elif curCategory == "대체실습":
            curCategory = "temporaryClassNumber"

        elif curCategory == "시험회차":
            curCategory = "exam"
            
        elif curCategory == "시작일":
            curCategory = "startDate"
            
        elif curCategory == "종료일":
            curCategory = "endDate"
            
        elif curCategory == "수여일":
            curCategory = "awardDate"
            
        elif curCategory == "강사":
            curCategory = "teacherName"

        elif curCategory == "SQL":
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
            if curCategory == "name" or curCategory == "teacherName":
                rs = self.dbPrograms.SELECT("*", curTable, where=f"{curCategory} LIKE '%{keyWord}%'")
            else:
                rs = self.dbPrograms.SELECT("*", curTable, where=f"{curCategory} = '{keyWord}'")
                
            if rs == "error":
                QMessageBox.information(self, "SQL query Error", "SQL query returns error!", QMessageBox.Yes, QMessageBox.Yes)
            else:
                search_result = "{}, \"{}\" 검색 결과\n{}개의 검색 결과가 존재합니다.".format(self.R_category.currentText(), self.R_searchBox.text(), len(rs))
                self.textInfo.setText(search_result)
                cols = self.readDB.columnCount()
                for i in range(len(rs)):
                    self.readDB.insertRows(self.readDB.rowCount(), 1)
                    for j in range(cols):
                        self.readDB.setData(self.readDB.index(i, j), str(rs[i][j]))
        except:
            QMessageBox.information(self, "검색 오류", "잘못된 검색입니다.", QMessageBox.Yes, QMessageBox.Yes)
            return

    def DELETE(self):
        targetTable = ""
        check = ""
        if self.curTable == "user":
            targetTable = "user"
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

        elif self.curTable == "lecture":
            targetTable = "lecture"
            clsN = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            clsT = str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            startD = str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            endD = str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            query = "classNumber = '{}' and classTime = '{}'".format(clsN, clsT)

            check = "기수: {}\t반: {}\n시작일: {}\n종료일: {}\n".format(clsN, clsT, startD, endD)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."
            
        elif self.curTable == "teacher":
            targetTable = "teacher"
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

        elif self.curTable == "temptraining":
            targetTable = "temptraining"
            clsN = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            startD = str(self.readDB.index(self.table.currentIndex().row(), 1).data())
            endD = str(self.readDB.index(self.table.currentIndex().row(), 2).data())
            awardD = str(self.readDB.index(self.table.currentIndex().row(), 3).data())

            check = "기수: {}\n시작일: {}\n종료일: {}\n수여일: {}\n".format(clsN, startD, endD, awardD)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."

            query = "classNumber = '{}'".format(clsN)
            
        elif self.curTable == "temptrainingteacher":
            targetTable = "temptrainingteacher"
            clsN = str(self.readDB.index(self.table.currentIndex().row(), 0).data())
            teacher = str(self.readDB.index(self.table.currentIndex().row(), 1).data())

            query = "classNumber = '{}' and teacherName = '{}'".format(clsN, teacher)

            check = "기수: {}\n강사: {}\n".format(clsN, teacher)
            check += "\n해당 정보를 데이터베이스에서 삭제합니다."


        ans = QMessageBox.question(self, "데이터 삭제 확인", check, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            db.main.dbPrograms.DELETE(targetTable, query)
            QMessageBox.about(self, "완료", "데이터를 성공적으로 삭제했습니다.")
            self.showTable(Refresh=True)
            self.textInfo.clear()
        else:
            pass

    def isNULL(self):
        self.readDB.clear()
        self.selectTable()

        if self.curTable == "":
            QMessageBox.information(self, "객체 오류", "테이블을 먼저 선택해주세요.", QMessageBox.Yes, QMessageBox.Yes)
            return

        elif self.curTable == "user":
            query = "id IS null or name IS null or RRN IS null or phoneNumber IS null or license IS null or address IS null or originAddress IS null or classNumber IS null or classTime IS null or totalCreditHour IS null or theoryCreditHour IS null or practicalCreditHour IS null or trainingCreditHour IS null or temporaryClassNumber IS null or exam IS null"
            order = "id"
            
        elif self.curTable == "lecture":
            query = "classNumber IS null or classTime IS null or startDate IS null or endDate IS null"
            order = "classNumber"

        elif self.curTable == "teacher":
            query = "id IS null or category IS null or name IS null or dateOfBirth IS null or license IS null or minCareer IS null or ACKDate IS null"
            order = "id"

        elif self.curTable == "temptraining":
            query = "classNumber IS null or startDate IS null or endDate IS null or awardDate IS null"
            order = "classNumber"

        elif self.curTable == "temptrainingteacher":
            query = "classNumber IS null or teacherName IS null"
            order = "classNumber"

        rs = self.dbPrograms.SELECT("*", self.curTable, where=query, orderBy=order)
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

        today = today = datetime.today().strftime("%Y%m%d")
        today = today[2:]
        file_name = ""
        self.backUpWbook = Workbook()
        ws = self.backUpWbook.active
        col = []

        if self.curTable == "":
            QMessageBox.information(self, "오류", "테이블을 먼저 선택해주세요.", QMessageBox.Yes, QMessageBox.Yes)
            return

        if self.curTable == "user":
            col = self.select_list_user
            file_name = "수강생DB"

        elif self.curTable == "lecture":
            col = self.select_list_lecture
            file_name = "기수,반DB"

        elif self.curTable == "teacher":
            col = self.select_list_teacher
            file_name = "강사DB"

        elif self.curTable == "temptraining":
            col = self.select_list_temptraining
            file_name = "대체실습DB"

        elif self.curTable == "temptrainingteacher":
            col = self.select_list_temptrainingteacher
            file_name = "대체실습 강사DB"

        for i, val in enumerate(col, start=1):
            ws.cell(row=1, column=i).value = val

        if self.curTable == "user":
            for i in range(self.readDB.rowCount()):
                for j in range(15):
                    ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())

        elif self.curTable == "lecture":
            for i in range(self.readDB.rowCount()):
                for j in range(4):
                    ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())
            
        elif self.curTable == "teacher":
            for i in range(self.readDB.rowCount()):
                for j in range(7):
                    ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())

        elif self.curTable == "temptraining":
            for i in range(self.readDB.rowCount()):
                for j in range(4):
                    ws.cell(row=i + 2, column=j + 1).value = str(self.readDB.index(i, j).data())
            
        elif self.curTable == "temptrainingteacher":
            for i in range(self.readDB.rowCount()):
                for j in range(2):
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
    global scanner

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NYNOA DBMS")
        # self.setWindowIcon(QIcon("D:\\user\\Desktop\\자동화파일\\0_남양로고_211220\\남양로고.png"))
        self.resize(1200, 800)
        # self.setFixedSize(1200, 800)

        # status Bar
        # self.statusBar()
        self.statusBar().showMessage("상태바")
        self.main = mainLayout()

        self.setCentralWidget(self.main)

        self.menuOpt()

        # btn = QPushButton("수강생 관리", self)
        # btn.resize(btn.sizeHint())
        # btn.move(50, 50)
        # btn.clicked.connect(QCoreApplication.instance().quit)
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

    def batch_show(self):
        batch.show()

    def UPDATE_show(self):
        if self.main.textInfo.toPlainText() == "":
            QMessageBox.information(self, "객체 오류", "객체를 먼저 선택해주세요.",
            QMessageBox.Yes, QMessageBox.Yes)

        else:
            update.show()


    def INSERT_show(self):
        if self.main.curTable == "":
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
    scanner = scanFile()
    sys.exit(app.exec_())