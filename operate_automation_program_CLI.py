# 공용 import 항목
import sys
# 자동화 파일 import 항목

# import 한 파일 안에 import 되어 있는것은 따로 import 안해도 됨 !
import cafe_update_module
import operate_data

from operate_automation_menu import automation

function = automation()

class AutoCLI(automation):
    def __init__(self):
        print("자동화 프로그램을 시작합니다.")

        function = automation()

        self.gisu = None
        self.time = None
        self.printMenu()

    def exitProgram(self):
        print("프로그램을 종료합니다.")
        sys.exit()

    def inputGisuTime(self):
        self.gisu = input("기수를 입력해 주세요:")
        if (not self.gisu.isdigit()) or int(self.gisu) < 1:
            print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
            self.inputGisuTime()

        self.time = input("\'주간\' / \'야간\'을 입력해 주세요:")

        if self.time != "주간" and self.time != "야간":
            print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
            self.inputGisuTime()

    def printMenu4(self):
        print("\n\n")
        print("******* 국시원 자동화 *******")
        print("1. 합격자 명단 작성")
        print("2. 사진 복사")
        print("3. 국시원 회원가입")
        print("4. 출력_교육수료증명서")
        print("5. 출력_대체실습 확인서")
        print("6. 출력_요양보호사 자격증 발급, 재발급 신청서")
        print("q. 프로그램 종료")
        print("****************************")
        answer_menu = input("메뉴를 선택해주세요: ")
        if answer_menu == "1":
            print("\n합격자 명단 작성")
            exam = input("시험 회차: ")

            if not exam.isdigit():
                print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
                self.printMenu4()
            
            res = input(exam + "회합격자명단.xlsx 파일에 미리 작성된 인원이 있습니까? [y/n]")
            if res == "y" or res == "Y":
                exist = input("먼저 기입된 인원 수를 입력하세요: ")
            elif res == "n" or res == "N":
                exist = 0
            else:
                print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
                self.printMenu4()

            print(exam + "회 합격자명단 파일을 최신화합니다.")
            print("*******************************************************************")
            print("**************** 주의 ! 이 프로그램을 사용한 후에 *****************")
            print("**** 합격자명단 파일의 내용을 합격자명단_호환모드 로 복사한 후 ****")
            print("**************** 호환모드의 파일을 제출해야 합니다. ***************")
            print("*******************************************************************")
            function.list_pass(exam_round=int(exam), exist=int(exist))
            print(exam + "회 합격자명단 파일 최신화를 완료했습니다.")

        elif answer_menu == "2":
            print("\n사진 복사")
            exam = input("시험 회차: ")

            if not exam.isdigit():
                print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
                self.printMenu4()
            
            print(exam + "회 사진 복사를 시작합니다.")
            function.copy_picture(exam)
            print(exam + "회 사진 복사를 완료했습니다.")

        elif answer_menu == "3":
            print("\n국시원 회원가입")
            print("\n\n******************************************")
            print("**** 이 기능은 업데이트되지 않았습니다. ****")
            print("******************************************\n\n")
            self.printMenu4()

        elif answer_menu == "4" or answer_menu == "5" or answer_menu == "6":
            print("\n서류 출력")
            print("*****************************************************************************************")
            print("************************* 이 기능은 주의가 필요합니다 !WARNING! *************************")
            print("***************** 이 프로그램이 시작되면 파일들이 순차적으로 시작됩니다.*****************")
            print("************* 1. 프린터가 이면지가 아닌 A4용지로 되어있는지 확인해 주세요. **************")
            print("******************** 2. 출력할 A4용지의 양이 충분한지 확인해 주세요. ********************")
            print("** 3. 각 파일들이 모두 입력되었는지, 수정할 것은 없는지 잘 확인한 후에 실행해 주세요 ! **")
            print("*****************************************************************************************")

            res = input("작업을 진행하시겠습니까? 진행하기 전 주의사항을 한번 더 확인해주세요. [y/n]")
            if res == "y" or res == "Y":
                pass
            elif res == "n" or res == "N":
                print("\n메뉴를 다시 선택해주세요")
                self.printMenu4()
            else:
                print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
                self.printMenu4()
            
            self.inputGisuTime()

            print("******* 출력할 서류 선택 *******")
            print("1. 교육수료증명서")
            print("2. 대체실습 확인서")
            print("3. 요양보호사 자격증 발급, 재발급 신청서")
            print("q. 프로그램 종료")
            print("*******************************")
            task = input("출력할 서류를 선택해주세요: ")

            if task == "1":
                task = "교육수료증명서"
            
            elif task == "2":
                task = "대체실습확인서"
            
            elif task == "3":
                task = "요양보호사 자격증 발급,재발급 신청서"

            elif task == "q" or task == "Q":
                self.exitProgram()

            else:
                print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
                self.printMenu4()

            print(self.gisu + "기 " + self.time + "반 " + task + " 출력을 시작합니다.")
            function.printFile(self.gisu, self.time, task)
            print(self.gisu + "기 " + self.time + "반 " + task + " 출력을 완료하였습니다.")

        elif answer_menu == "q" or answer_menu == "Q":
            self.exitProgram()

        else:
            print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
            self.printMenu4()

        self.printMenu()

    def printMenu3(self):
        print("\n\n")
        print("******* 개강보고 *******")
        print("1. 개강보고")
        print("2. 출석부")
        print("3. 실시보고_대체실습")
        print("4. 수료보고_대체실습")
        print("5. 출석부_대체실습")
        print("q. 프로그램 종료")
        print("***********************")
        print("\n\n******************************************")
        print("**** 이 기능은 업데이트되지 않았습니다. ****")
        print("******************************************\n\n")
        self.printMenu()


    def printMenu2(self):
        print("\n\n")
        print("******* 교육생 관리 *******")
        print("1. 교육수료증명서")
        print("2. 대체실습 확인서")
        print("3. 요양보호사 자격증 발급, 재발급 신청서")
        print("q. 프로그램 종료")
        print("**************************")

        answer_menu = input("메뉴를 선택해주세요: ")
        if answer_menu == "1":
            answer_menu = "교육수료증명서"
        
        elif answer_menu == "2":
            answer_menu = "대체실습확인서"
        
        elif answer_menu == "3":
            answer_menu = "요양보호사 자격증 발급,재발급 신청서"

        elif answer_menu == "q" or answer_menu == "Q":
            self.exitProgram()

        else:
            print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
            self.printMenu2()

        print(self.gisu + "기 " + self.time + "반 " + answer_menu + "를 작성합니다.")
        function.automation_task_students(self.gisu, self.time, answer_menu, 1)
        print(self.gisu + "기 " + self.time + "반 " + answer_menu + " 작성을 완료하였습니다.")

        self.printMenu()



    def printMenu1(self):
        print("\n\n")
        print("******* Base Info *******")
        print("1. 출석시간 반영")
        print("2. 교육생 자료 복사")
        print("q. 프로그램 종료")
        print("*************************")
        answer_menu = input("메뉴를 선택해주세요: ")

        if answer_menu == "1":
            print("\n")
            print("출석시간 반영")
            
            self.inputGisuTime()

            print(self.gisu + "기 " + self.time + "반 출석부를 최신화 합니다.")
            function.update_attendance(self.gisu, self.time)
            print(self.gisu + "기 " + self.time + "반 출석부를 최신화를 완료했습니다.")

        elif answer_menu == "2":
            print("\n")
            print("<===== 교육생 자료 복사 =====>")
            print("******* 파일 선택 *******")
            print("1. 교육수료증명서")
            print("2. 대체실습 확인서")
            print("3. 요양보호사 자격증 발급, 재발급 신청서")
            print("************************")
            file_name = input("복사할 자료를 선택해 주세요.")
            
            if file_name == "1":
                file_name = "교육수료증명서.xlsx"
            elif file_name == "2":
                file_name = "대체실습확인서.xlsx"
            elif file_name == "3":
                file_name = "요양보호사 자격증 발급,재발급 신청서.xlsx"
            else:
                print("잘못 입력하셨습니다. 다시 입력해 주세요.")
                self.printMenu1()

            self.inputGisuTime()

            print(self.gisu + "기 " + self.time + "반 폴더에 " + file_name + "를 복사합니다.")
            function.mkfile(self.gisu, self.time, file_name)
            print(self.gisu + "기 " + self.time + "반 폴더로 " + file_name + "복사를 완료했습니다.")

        elif answer_menu == "q" or answer_menu == "Q":
            self.exitProgram()

        else:
            print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
            self.printMenu1()

        self.printMenu()

    def printMenu(self):
        print("\n\n")
        print("******* 메뉴 *******")
        print("1. Base Info")
        print("2. 교육생 관리")
        print("3. 경기도청 보고")
        print("4. 국시원 자동화")
        print("q. 프로그램 종료")
        print("********************")
        answer_menu = input("메뉴를 선택해주세요: ")
        if answer_menu == "1":
            self.printMenu1()

        elif answer_menu == "2":
            self.printMenu2()

        elif answer_menu == "3":
            self.printMenu3()
        
        elif answer_menu == "4":
            self.printMenu4()

        elif answer_menu == "q" or answer_menu == "Q":
            self.exitProgram()

        else:
            print("\n잘못 입력하셨습니다. 다시 입력해 주세요.")
            self.printMenu()

if __name__ == "__main__":
    a = AutoCLI()
