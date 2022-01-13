import os
import random
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.drawing.image import Image
from database import DB

class Automation:
    def __init__(self):
        self.wbPath = "D:\\Master\\mkfile\\"
        self.basePath = "D:\\남양노아요양보호사교육원\\교육생관리\\"
        self.imsi_workbook_path = "D:\\Master\\PythonWorkspace\\imsi.xlsx"
        self.wb = None
        self.ws = None
        self.DB = DB()
        self.wb_imsi = None
        self.ws_imsi = None

    """
    교육수료증명서를 어떻게 일괄적으로 출력 할 것인가!
    1. 기수, 반 별로 생성 및 출력한다.  X
    2. 시험 회차에 따라 일괄 생성 및 출력한다.  O
    3. 개인적으로 생성 및 출력한다. (일일이!!! ) ==> 이건 좀 필요할 듯. 누군가 누락됐을 때 생성할 필요 있음!    O
    """
    def mkDoc(self, doc_type, exam):
        self.wbPath += "\\{}.xlsx".format(doc_type)
        if doc_type == "교육수료증명서":
            try:
                where = "exam={};".format(exam)
                user_rs = self.DB.SELECT("*", "user", where)

                user_query_list = ["id", "name", "RRN", "phoneNumber", "license", "address", "originAddress", "classNumber", "classTime", \
                    "totalCreditHour", "theoryCreditHour", "practicalCreditHour", "trainingCreditHour", "temporaryClassNumber", "exam"]
                item_dict = {}

                for rows in user_rs:
                    for index in range(len(rows)):
                        item_dict[user_query_list[index]] = rows[index]

                    save_path = self.basePath + "{}\\{}{}\\{}".format(item_dict["classNumber"], item_dict["classNumber"], item_dict["classTime"], item_dict["name"])

                    self.wb = load_workbook(self.wbPath)
                    self.ws = self.wb.active

                    where = "classNumber = '{}' and classTime = '{}'".format(item_dict["classNumber"], item_dict["classTime"])
                    classInfo_rs = self.DB.SELECT("*", "lecture", where, fetchone=True)

                    item_dict["startDate"] = classInfo_rs[2].strftime("%Y년 %m월 %d일")
                    item_dict["endDate"] = classInfo_rs[3].strftime("%Y년 %m월 %d일")

                    where = "classNumber='{}'".format(item_dict["temporaryClassNumber"])
                    tempInfo_rs = self.DB.SELECT("*", "temptraining", where, fetchone=True)

                    item_dict["startDate_temp"] = tempInfo_rs[1].strftime("%Y 년 %m 월 %d 일")
                    item_dict["endDate_temp"] = tempInfo_rs[2].strftime("%Y 년 %m 월 %d 일")
                    item_dict["awardDate"] = tempInfo_rs[3].strftime("%Y 년    %m 월     %d 일")

                    # 교육수료증명서 호수
                    string = "    2021  년  제  {} 호".format(item_dict["id"])
                    self.ws.cell(row=1, column=1).value = string

                    # 이름
                    string = " {}".format(" ".join(item_dict["name"]))
                    self.ws.cell(row=4, column=3).value = string

                    # 주소
                    string = " {}".format(item_dict["address"])
                    self.ws.cell(row=5, column=3).value = string

                    # 주민등록번호
                    string = " {}".format(str(item_dict["RRN"]))
                    self.ws.cell(row=6, column=3).value = string

                    # 전화번호
                    string = item_dict["phoneNumber"]
                    self.ws.cell(row=6, column=6).value = string

                    # 교육과정명
                    string = " 요양보호사 {}".format(item_dict["classNumber"])
                    self.ws.cell(row=7, column=3).value = string

                    # 이론실기 이수기간 / 각 기수별로 기간 선정, 2020 년  11 월  16 일 ∼  21 년  01 월 15 일 형식으로, 끝기간은 년도수 두자리만 표시
                    string = "{} ~ {}".format(item_dict["startDate"], item_dict["endDate"])
                    self.ws.cell(row=9, column=3).value = string

                    # 이론실기 이수시간
                    string = "        {}  시간".format(int(item_dict["theoryCreditHour"]) + int(item_dict["practicalCreditHour"]))
                    self.ws.cell(row=9, column=7).value = string

                    # 실습기간 / 대체실습 각 기수별 or 실습기간 따로 만들기,  21년 01월 18일 ∼ 21년 03월 13일 형식으로, 년도수 두자리만 표시
                    string = "{} ~ {}".format(item_dict["startDate_temp"], item_dict["endDate_temp"])
                    self.ws.cell(row=12, column=4).value = string

                    # 대체실습이 종료되면, 각 사람마다 실습시간(각 기관) 이 달라짐. 업데이트 필요
                    # 실습시간
                    string = "        {}  시간".format(item_dict["trainingCreditHour"])
                    self.ws.cell(row=12, column=7).value = string

                    # 총 실습시간
                    string = "         {}  시간".format(item_dict["trainingCreditHour"])
                    self.ws.cell(row=18, column=7).value = string

                    # 총 이수시간
                    string = "       {}  시간".format(item_dict["totalCreditHour"])
                    self.ws.cell(row=19, column=7).value = string

                    # 수여일 / 각 인원 대체실습 기준 종료일 바로 다음 월요일 날짜로 지정
                    string = "                                      {}".format(item_dict["awardDate"])
                    self.ws.cell(row=23, column=1).value = string

                    self.wb.save(save_path + "\\{}_{}xlsx".format(item_dict["name"], doc_type))
                    self.wb.close()

            except:
                self.DB.conn.close()

        elif doc_type == "대체실습확인서":
            try:
                where = "exam={};".format(exam)
                user_rs = self.DB.SELECT("id, name, RRN, phoneNumber, classNumber, trainingCreditHour, temporaryClassNumber", "user", where)

                user_query_list = ["id", "name", "RRN", "phoneNumber", "classNumber", "trainingCreditHour", "temporaryClassNumber"]
                item_dict = {}

                for rows in user_rs:
                    for index in range(len(rows)):
                        item_dict[user_query_list[index]] = rows[index]

                    save_path = self.basePath + "{}\\{}{}\\{}".format(item_dict["classNumber"], item_dict["classNumber"], item_dict["classTime"], item_dict["name"])

                    self.wb = load_workbook(self.wbPath)
                    self.ws = self.wb.active

                    teacher_rs = self.DB.SELECT("*", "teacher")
                    teacher_dict = {}
                    for rows in teacher_rs:
                        teacher_dict[rows[2]] = rows

                    where = "classNumber = '{}'".format(item_dict["temporaryClassNumber"])
                    temp_teacher_rs = self.DB.SELECT("teacherName", "temptrainingteacher", where=where)
                    temp_teacher_list = []
                    for rows in temp_teacher_rs:
                        temp_teacher_list.append(rows[0])

                    where = "classNumber='{}'".format(item_dict["temporaryClassNumber"])
                    tempInfo_rs = self.DB.SELECT("*", "temptraining", where, fetchone=True)

                    item_dict["startDate_temp"] = tempInfo_rs[1].strftime("%Y 년  %m 월  %d 일")
                    item_dict["endDate_temp"] = tempInfo_rs[2].strftime("%Y 년  %m 월  %d 일")
                    item_dict["awardDate"] = tempInfo_rs[3].strftime("%Y 년   %m 월    %d 일")

                    # 이름
                    string = item_dict["name"]
                    self.ws.cell(row=7, column=2).value = string

                    # 생년월일
                    BoD = item_dict["RRN"][:7]
                    string = ". ".join(BoD)
                    self.ws.cell(row=7, column=3).value = string

                    # 연락처
                    string = item_dict["phoneNumber"]
                    self.ws.cell(row=7, column=4).value = string

                    # 교육기관명
                    string = "남양노아요양보호사교육원"
                    self.ws.cell(row=7, column=5).value = string

                    # 교육과정명
                    string = " 요양보호사 {}".format(item_dict["classNumber"])
                    self.ws.cell(row=7, column=7).value = string

                    # 강사
                    for teacher in temp_teacher_list:
                        for i in range(7):
                            string = teacher_dict[teacher][i]
                            self.ws.cell(row=12, column=i + 1).value = string                        

                    # 대체실습 기간
                    string = "{}  ~    {}".format(item_dict["startDate_temp"], item_dict["endDate_temp"])
                    self.ws.cell(row=20, column=3).value = string

                    # 대체실습 시간
                    string = "  총     {}  시간".format(item_dict["trainingCreditHour"])
                    self.ws.cell(row=21, column=3).value = string

                    # 합격여부 
                    self.ws.cell(row=22, column=3).value = "합격"

                    # 자체시험 점수
                    name = self.ws_members.cell(row=idx, column=18).value
                    for cell in self.ws_score["C"]:
                        if cell.value == name:
                            temp_row = cell.row
                    temp_score = self.ws_score.cell(row=temp_row, column=7).value
                    if temp_score == None:
                        temp_score = random.randint(85, 100)
                    else:
                        pass
                    self.ws.cell(row=22, column=6).value = temp_score

                    # 비고 

                    # 서명

                    # 수여일
                    string = "                                      {}".format(item_dict["awardDate"])
                    self.ws.cell(row=27, column=1).value = string

                    self.wb.save(save_path + "\\{}_{}xlsx".format(item_dict["name"], doc_type))
                    self.wb.close()

            except:
                self.DB.conn.close()

        elif doc_type == "요양보호사 자격증 발급,재발급 신청서":
            try:
                item_dict = {}

                where = "exam={};".format(exam)
                exam_rs = self.DB.SELECT("*", "exam", where, fetchone=True)
                item_dict["examDate"] = exam_rs[3].strftime("%Y년 %m월 %d일")
                item_dict["passDate"] = exam_rs[4].strftime("%Y년 %m월 %d일")
                item_dict["submitDate"] = exam_rs[5].strftime("     %Y  년     %m  월    %d   일    ")

                user_rs = self.DB.SELECT("id, name, RRN, phoneNumber, address, classNumber, classTime, temporaryClassNumber", "user", where)

                user_query_list = ["id", "name", "RRN", "phoneNumber", "address", "classNumber", "classTime", "temporaryClassNumber"]

                for rows in user_rs:
                    for index in range(len(rows)):
                        item_dict[user_query_list[index]] = rows[index]

                    save_path = self.basePath + "{}\\{}{}\\{}".format(item_dict["classNumber"], item_dict["classNumber"], item_dict["classTime"], item_dict["name"])

                    self.wb = load_workbook(self.wbPath)
                    self.ws = self.wb.active

                    where = "classNumber = '{}' and classTime = '{}'".format(item_dict["classNumber"], item_dict["classTime"])
                    classInfo_rs = self.DB.SELECT("*", "lecture", where, fetchone=True)

                    item_dict["startDate"] = classInfo_rs[2].strftime("%Y.%m.%d")
                    item_dict["endDate"] = classInfo_rs[3].strftime("%Y.%m.%d")

                    where = "classNumber='{}'".format(item_dict["temporaryClassNumber"])
                    tempInfo_rs = self.DB.SELECT("*", "temptraining", where, fetchone=True)

                    item_dict["startDate_temp"] = tempInfo_rs[1].strftime("%Y.%m.%d")
                    item_dict["endDate_temp"] = tempInfo_rs[2].strftime("%Y.%m.%d")
                    item_dict["awardDate"] = tempInfo_rs[3].strftime("%Y 년    %m 월     %d 일")
                    
                    """
                    시험 회차, 시험 시행일, 합격일, 신청 일자, 합격 예정일(?) 등 컬럼 맞춰서 table 생성하기!
                    """

                    # 사진
                    # D:\남양노아요양보호사교육원\교육생관리\7기\7기주간0503\7. 이윤옥
                    ## 사진 이름을 어떻게 짛을 지가 관건!
                    try:
                        student_picture = save_path + "\\{}.jpg".format(item_dict["name"])
                        img = Image(student_picture)
                    except:
                        student_picture = save_path + "\\{}{}_{}.jpg".format(item_dict["classNumber"], item_dict["classTime"], item_dict["name"])
                        img = Image(student_picture)
                    img.height = 142
                    img.width = 111
                    img.anchor = "G6"
                    self.ws.add_image(img)

                    # 이름
                    string = "성명(한자)   {}".format(item_dict["name"])
                    self.ws.cell(row=6, column=2).value = string

                    # 주민등록번호
                    string = "주민등록번호  {}".format(item_dict["RRN"])
                    self.ws.cell(row=7, column=2).value = string

                    # 주소
                    string = "주소   {}".format(item_dict["address"])
                    self.ws.cell(row=8, column=2).value = string

                    # 전화번호
                    string = "전화번호  {}".format(item_dict["phoneNumber"])
                    self.ws.cell(row=9, column=2).value = string

                    # 요양보호사 교육기간. 부터
                    string = item_dict["startDate"][2:]
                    self.ws.cell(row=12, column=2).value = string

                    # 요양보호사 교육기간. 까지
                    string = item_dict["endDate"][2:]
                    self.ws.cell(row=12, column=3).value = string

                    # 교육과정명
                    string = "요양보호사 {}기 (이론,실기)".format(item_dict["classNumber"])
                    self.ws.cell(row=12, column=4).value = string

                    # 교육기관명
                    string = "남양노아요양보호사교육원"
                    self.ws.cell(row=12, column=7).value = string

                    # 요양보호사 교육기간(실습). 부터
                    string = item_dict["startDate_temp"][2:]
                    self.ws.cell(row=13, column=2).value = string

                    # 요양보호사 교육기간(실습). 까지
                    string = item_dict["endDate_temp"][2:]
                    self.ws.cell(row=13, column=3).value = string

                    # 교육과정명(실습)
                    string = "요양보호사 (대체실습{}기)".format(item_dict["temporaryClassNumber"])
                    self.ws.cell(row=13, column=4).value = string

                    # 교육기관명(실습)
                    string = "남양노아요양보호사교육원"
                    self.ws.cell(row=13, column=7).value = string

                    # 시험 시행일
                    string = "시험시행일   {}".format(item_dict["examDate"])
                    self.ws.cell(row=14, column=2).value = string

                    # 시험 합격일
                    string = "시험합격일   {}".format(item_dict["passDate"])
                    self.ws.cell(row=14, column=5).value = string

                    # 신청 일자
                    string = item_dict["submitDate"]
                    self.ws.cell(row=19, column=1).value = string

                    # 이름 / shift 는 keyDown(or Up) 에서 left 와 right 를 모두 입력해 주어야 정상작동 함 !!
                    string = "{} (서명 또는 인)".format(item_dict["name"])
                    self.ws.cell(row=20, column=4).value = string

                    self.wb.save(save_path + "\\{}_{}xlsx".format(item_dict["name"], doc_type))
                    self.wb.close()

            except:
                self.DB.conn.close()

    def report(self, doc_type, number, time=None):
        """
        개강보고
        대체실습 실시보고
        대체실습 수료보고
        """
        if time == "":
            time == None

        if doc_type == "개강보고":
            self.wb_imsi = Workbook()
            self.ws_imsi = self.wb_imsi.active
            rs = self.DB.SELECT("license, name, RRN, address, phoneNumber", "user", "classNumber='{}' and classTime='{}'".format(number, time), orderBy="FIELD(license, '일반', '사회복지사', '간호조무사', '간호사', '물리치료사'), id *1")
            for indexX, rows in enumerate(rs, start=1):
                license = rows[0]
                if license == "일반":
                    category = "신규\n(일반)"
                else:
                    category = "자격증\n"
                    if license == "간호사" or license == "물리치료사":
                        category += "({})".format(license[:2])
                    else:
                        category += "({}{})".format(license[0], license[2])

                name = rows[1]
                DOB = rows[2][:7]
                DOB = DOB[:2] + ". " + DOB[2:4] + ". " + DOB[4:]
                address = rows[3]
                phone = rows[4]

                data_list = [category, name, DOB, address, phone]

                self.ws_imsi.cell(row=indexX, column=1).value = indexX
                self.ws_imsi.cell(row=indexX, column=1).alignment = Alignment(horizontal="center", vertical="center")
                self.ws_imsi.cell(row=indexX, column=1).font = Font(size=10)
                for indexY, value in enumerate(data_list, start=2):
                    self.ws_imsi.cell(row=indexX, column=indexY).value = value
                    self.ws_imsi.cell(row=indexX, column=indexY).alignment = Alignment(horizontal="center", vertical="center")
                    self.ws_imsi.cell(row=indexX, column=indexY).font = Font(size=10)

        elif doc_type == "대체실습 실시보고":
            self.wb_imsi = Workbook()
            self.ws_imsi = self.wb_imsi.active
            rs = self.DB.SELECT("license, name, RRN, phoneNumber, classTime, classNumber", "user", "temporaryClassNumber='{}'".format(number), orderBy="classNumber *1, FIELD(classTime, '주간', '야간'), FIELD(license, '일반', '사회복지사', '간호조무사', '간호사', '물리치료사'), id *1")
            for indexX, rows in enumerate(rs, start=1):
                license = rows[0]
                if license == "일반":
                    category = "신규"
                    time = 80
                else:
                    category = "자격증"
                    time = 8

                name = rows[1]
                DOB = rows[2][:6]
                DOB = DOB[:2] + ". " + DOB[2:4] + ". " + DOB[4:]
                phone = rows[3]
                class_info = rows[4] + "반 " + rows[5]
                rs_lecture = self.DB.SELECT("endDate", "lecture", "classNumber='{}' and classTime='{}'".format(rows[5], rows[4]))
                class_end_date = rs_lecture[0][0].strftime("%Y.%m.%d")
                time = str(time) + "시간"

                data_list = [category, name, DOB, phone, class_info, class_end_date, time]

                self.ws_imsi.cell(row=indexX, column=1).value = indexX
                self.ws_imsi.cell(row=indexX, column=1).alignment = Alignment(horizontal="center", vertical="center")
                self.ws_imsi.cell(row=indexX, column=1).font = Font(size=10)
                for indexY, value in enumerate(data_list, start=2):
                    self.ws_imsi.cell(row=indexX, column=indexY).value = value
                    self.ws_imsi.cell(row=indexX, column=indexY).alignment = Alignment(horizontal="center", vertical="center")
                    self.ws_imsi.cell(row=indexX, column=indexY).font = Font(size=10)



        elif doc_type == "대체실습 수료보고":
            self.wb_imsi = Workbook()
            self.ws_imsi = self.wb_imsi.active
            rs = self.DB.SELECT("classTime, classNumber, totalCreditHour, theoryCreditHour, practicalCreditHour, trainingCreditHour, name, RRN, address, phoneNumber", "user", "temporaryClassNumber='{}'".format(number), orderBy="classNumber *1, FIELD(classTime, '주간', '야간'), FIELD(license, '일반', '사회복지사', '간호조무사', '간호사', '물리치료사'), id *1")
            rs_temp_lecture = self.DB.SELECT("awardDate", "temptraining", "classNumber='{}'".format(number))
            award_date = rs_temp_lecture[0][0].strftime("%Y.%m.%d")
            for indexX, rows in enumerate(rs, start=1):
                class_info = rows[0] + "반\n" + rows[1]

                total_time = rows[2]
                theory_time = rows[3]
                practice_time = rows[4]
                training_time = rows[5]
                name = rows[6]
                RRN = rows[7][:6] + "\n" + rows[7][6:]
                address = rows[8]
                phone = rows[9]

                data_list = [class_info, total_time, theory_time, practice_time, "", training_time, name, RRN, address, phone, award_date]

                self.ws_imsi.cell(row=indexX, column=1).value = indexX
                self.ws_imsi.cell(row=indexX, column=1).alignment = Alignment(horizontal="center", vertical="center")
                self.ws_imsi.cell(row=indexX, column=1).font = Font(size=10)
                for indexY, value in enumerate(data_list, start=2):
                    self.ws_imsi.cell(row=indexX, column=indexY).value = value
                    self.ws_imsi.cell(row=indexX, column=indexY).alignment = Alignment(horizontal="center", vertical="center")
                    self.ws_imsi.cell(row=indexX, column=indexY).font = Font(size=10)


        self.wb_imsi.save(self.imsi_workbook_path)
        self.wb_imsi.close()
        os.system(self.imsi_workbook_path)




        
    def examPassList(self, exam):
        pass


if __name__ == '__main__':
    auto = Automation()

    auto.report("개강보고", "12기", "주간")