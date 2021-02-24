# 공용 import 항목

# 자동화 파일 import 항목

# import 한 파일 안에 import 되어 있는것은 따로 import 안해도 됨 !
import pyautogui # tkinter 창의 정보를 얻기 위한 import
# GUI 파일 import 항목
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk # combobox, progressbar
import tkinter.messagebox as msgbox

from operate_automation_menu import automation

import cafe_update_module
#                                       example
# preform = automation()
# perform.auto_move_class(4, "야간")
# perform.auto_move_report()
# perform.automation_task_students(3, "주간", "자격증 발급,재발급 신청서")
# perform.automation_task_report(5, "주간", "개강보고") # 수료보고가 따로 없기 때문에 kind = 개강보고로 고정 !
# perform.automation_task_temporary(4, "주간", "수료보고")
# perform.mkfile("5기주간0201", "교육수료증명서.hwp") # 뒤에 복사할 파일을 입력할 때 꼭 !!!!! 확장자 명까지 작성하기 ㅎㅎ
# perform.mkattendance(3, "야간")


global frame_run
global radio_num_var
global radio_time_var
global frame_option
global cmbbox

def automation_start():
    get_start = automation()
    ordinal_num = radio_num_var.get()
    time = radio_time_var.get()
    mode = cmbbox.get()
    print("ordinal_num :",ordinal_num, "ordinal_num type :", type(ordinal_num))
    print("time :", time, "time type", type(time))
    print("mode :", mode, "mode type :", type(mode))
    mode_baseinfo = ["출석시간 반영", "교육생 자료 복사"]
    mode_manage = ["교육수료증명서", "대체실습확인서", "자격증 발급,재발급 신청서"]
    mode_report = ["개강보고", "출석부", "실시보고_대체실습", "수료보고_대체실습", "출석부_대체실습"]
    # mode list : "교육수료증명서", "대체실습확인서", "요양보호사 자격증 발급 신청서", "출석시간 반영", "교육생 자료 복사", "개강보고(실시보고)", "종강보고(수료보고)", "출석부", "대체실습"

    if mode == mode_baseinfo[0]:
        get_start.update_attendance(ordinal_num, time)

    # elif mode == mode_baseinfo[1]:
        # get_start.mkfile(ordinal_num, time, )

    if mode in mode_manage:
        get_start.auto_move_class(ordinal_num, time)
        get_start.automation_task_students(ordinal_num, time, mode)

    if mode in mode_report:
        if mode == mode_report[0]:
            get_start.automation_task_report(ordinal_num, time, mode)
        elif mode == mode_report[1]:
            get_start.mkattendance(ordinal_num, time)
        elif mode == mode_report[2]:
            mode = mode_report[2][:4]
            get_start.automation_task_temporary(ordinal_num, mode)
        elif mode == mode_report[3]:
            mode = mode_report[3][:4]
            get_start.automation_task_temporary(ordinal_num, mode)
        elif mode == mode_report[4]:
            msgbox.showerror("업데이트 필요", "대체실습 출석부 작성 자동화 프로그램이 업데이트 되지 않았습니다.(업데이트 필요) ")



def del_widget(user_widget):

    if user_widget.winfo_exists():
        user_widget.destroy()

#####################################################################################################
# def mk_progressbar(user_widget, total_point):
#     p_var = DoubleVar()
#     frame_p = Frame(user_widget)
#     frame_p.pack(fill="x")
#     progressbar = ttk.Progressbar(frame_p, maximum=100, variable=p_var)
#     progressbar.pack(fill="x")
#     def update():
#         point = i / total_point * 100
#         p_var.set(point)
#         progressbar.update()
        

#####################################################################################################

def selection():
    global frame_run
    global lstbox_members

    if cmbbox.get() == "선택":
        msgbox.showinfo("알림", "자동화 옵션을 선택해주세요.")
    else:
        ready = msgbox.askyesno("선택", f"{radio_num_var.get()}기 {radio_time_var.get()}반 {cmbbox.get()} 자동화 작업을 선택하셨습니다.")
        print(ready)
        if ready == True:
            print(cmbbox.get())
            print(radio_num_var.get())
            print(radio_time_var.get())
        elif ready == False:
            msgbox.showinfo("알림", "자동화 옵션을 다시 선택해주세요.")
            return

    lst_selection = ["선택", "교육수료증명서", "대체실습확인서", "자격증 발급,재발급 신청서"]
    lst_selection.remove("선택")
    # frame_run = Frame(frame_2) # 이걸 안하면 계속 빨간줄 생김 ,, / 근데 이걸 하면 선택을 두번 연속 눌렀을 때 프레임이 안사라짐 ,,
    del_widget(frame_run)

    # if cmbbox.get() in lst_selection:
    frame_run = Frame(frame_2)
    frame_run.pack(fill="x")

    frame_members = Frame(frame_run)
    frame_members.pack(fill="x")

        # scrbar = Scrollbar(frame_members)
        # scrbar.pack(side="right", fill="y")

        # lstbox_members = Listbox(frame_members, selectmode="extended", height=10, yscrollcommand=scrbar.set)
        # lstbox_members.pack(side="left", fill="both", expand=True)

        # for i in range(1, 31):
        #     lstbox_members.insert(END, str(i) + "번")

        # scrbar.config(command=lstbox_members.yview)

    frame_btn_run = Frame(frame_run)
    frame_btn_run.pack(fill="x")

    btn_run_satrt = Button(frame_btn_run, text="실행", width=12, command=automation_start)
    btn_run_satrt.pack(side="right", padx=5, pady=5)



def basic():
    global radio_num_var
    global radio_time_var

    frame_basic_num = Frame(frame_option)
    frame_basic_num.pack(fill="x")
    label_num = Label(frame_basic_num, text="기수 선택")
    label_num.pack(side="left", padx=(30, 0), pady=5)

    frame_radio_num = Frame(frame_basic_num)
    frame_radio_num.pack()
    radio_num_var = IntVar() # StringVar 로 하려 했으나, noa_auto_menu 함수 인자가 int 형으로 되어 있어 IntVar 로 받음
    btn_number_1 = Radiobutton(frame_radio_num, text="1기", value=1, variable=radio_num_var)
    btn_number_1.select()
    btn_number_2 = Radiobutton(frame_radio_num, text="2기", value=2, variable=radio_num_var)
    btn_number_3 = Radiobutton(frame_radio_num, text="3기", value=3, variable=radio_num_var)
    btn_number_4 = Radiobutton(frame_radio_num, text="4기", value=4, variable=radio_num_var)
    btn_number_5 = Radiobutton(frame_radio_num, text="5기", value=5, variable=radio_num_var)

    frame_basic_time = Frame(frame_option)
    frame_basic_time.pack(fill="x")
    label_time = Label(frame_basic_time, text="시간 선택")
    label_time.pack(side="left", padx=(30, 0), pady=5)

    frame_radio_time = Frame(frame_basic_time)
    frame_radio_time.pack()
    radio_time_var = StringVar()
    btn_daytime = Radiobutton(frame_radio_time, text="주간", value="주간", variable=radio_time_var)
    btn_daytime.select()
    btn_nighttime = Radiobutton(frame_radio_time, text="야간", value="야간", variable=radio_time_var)

    btn_number_5.pack(side="right", padx=5, pady=5)
    btn_number_4.pack(side="right", padx=5, pady=5)
    btn_number_3.pack(side="right", padx=5, pady=5)
    btn_number_2.pack(side="right", padx=5, pady=5)
    btn_number_1.pack(side="right", padx=5, pady=5)

    btn_nighttime.pack(side="right", padx=5, pady=5)
    btn_daytime.pack(side="right", padx=5, pady=5)

    frame_basic_btn = Frame(frame_option)
    frame_basic_btn.pack(fill="x")
    btn_select = Button(frame_basic_btn, text="선택", command=selection, width=12)
    btn_select.pack(side="right", padx=15, pady=5)

def baseinfo():
    global frame_option
    global cmbbox

    lst = ["선택", "출석시간 반영", "교육생 자료 복사"]
    cmbbox["values"] = lst
    cmbbox.current(0)

def manage():
    global frame_option
    global cmbbox

    lst = ["선택", "교육수료증명서", "대체실습확인서", "자격증 발급,재발급 신청서"]
    cmbbox["values"] = lst
    cmbbox.current(0)

def report():
    global frame_option
    global cmbbox
    global chkvar_temp

    lst = ["선택", "개강보고", "출석부", "실시보고_대체실습", "수료보고_대체실습", "출석부_대체실습"]
    cmbbox["values"] = lst
    cmbbox.current(0)
        
def test():
    pass

def check_update():
    update_window = Tk()
    update_window.geometry("480x480")
    update_window.title("업데이트 내역")
    
    frame = LabelFrame(update_window, text="업데이트 내역")
    frame.pack(fill="both")

    label = Label(frame, text=" ")
    label.grid(row=0, column=0)

    label1 = Label(frame, text="ver. 0.1.0   프로젝트 시작   21.01.25\n\n")
    label1.grid(row=1, column=0, sticky=W)

    label2 = Label(frame, text="ver. 0.1.1   MainFrame 순서 고정   21.02.16\n\n")
    label2.grid(row=2, column=0, sticky=W)

    label3 = Label(frame, text="ver. 0.1.2   옵션선택 위치 조정   21.02.16\n\n")
    label3.grid(row=3, column=0)

    label4 = Label(frame, text="ver. 0.2.1   combobox 동적 값 할당   21.02.16\n\n")
    label4.grid(row=4, column=0)

    update_window.mainloop()

def start():
    print("radio num var : " + str(radio_num_var.get()))
    print("radio time var : " + str(radio_time_var.get()))

    print(cmbbox.get())

def cafe_update():
    cafe_update_module.cafe_update()

root = Tk()
root.title("교육원 운영 자동화 프로그램")
# root.geometry("510x480")
root.resizable(False, False)

# 메인 프레임
main_frame = Frame(root, relief="solid", bd=1)
main_frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)

# 버튼 집합 생성
frame_btn = LabelFrame(main_frame, text="자동화 메뉴")
frame_btn.pack(ipady=5)

btn_baseinfo = Button(frame_btn, text="BaseInfo", command=baseinfo, width=12)
btn_manage = Button(frame_btn, text="교육생관리", command=manage, width=12)
btn_report = Button(frame_btn, text="경기도청 보고", command=report, width=12)
btn_test = Button(frame_btn, text="국시원 자동화", command=test, width=12)

btn_baseinfo.pack(side="left", padx=10, pady=5)
btn_manage.pack(side="left", padx=10, pady=5)
btn_report.pack(side="left", padx=10, pady=5)
btn_test.pack(side="left", padx=10, pady=5)

# 1번 프레임
frame_1 = Frame(main_frame)
frame_1.pack(fill="x")
label_1 = Label(frame_1, text=" ")
label_1.pack(side="bottom")

frame_option = LabelFrame(frame_1, text="업무 자동화")
frame_option.pack(fill="both")

frame_cmbbox = Frame(frame_option)
frame_cmbbox.pack()
label = Label(frame_cmbbox, text="Option")
label.pack(side="left", padx=5, pady=5)

lst = ["선택"]
cmbbox = ttk.Combobox(frame_cmbbox, state="readonly", values=lst)
cmbbox.current(0)
cmbbox.pack(side="left", padx=5, pady=5)

basic()

# 2번 프레임
frame_2 = Frame(main_frame)
frame_2.pack(fill="both")

# 프로그램 실행 프레임
frame_run = Frame(frame_2)
frame_run.pack(fill="x")

# 서브 프레임
sub_frame = Frame(root, relief="solid", bd=1)
sub_frame.pack(side="right", padx=5, pady=5, fill="both", expand=True)

# side = bottom
# ver 0.1.1 : 프레임 순서 설정  / 0.1.2 : basic 함수에 프레임 추가로 가독성 상승
label_verinfo = Label(sub_frame, text="버전정보 0.2.1")
label_verinfo.pack(side="bottom")

btn_update = Button(sub_frame, text="업데이트 내역", command=check_update, width=12)
btn_update.pack()

btn_select = Button(sub_frame, text="시작", command=start, width=12)
btn_select.pack(padx=5, pady=5)

btn_cafe = Button(sub_frame, text="카페 자동화", command=cafe_update, width=12)
btn_cafe.pack(padx=5, pady=5)

btn_quit = Button(sub_frame, text="종료", command=root.quit, width=12)
btn_quit.pack(padx=5, pady=5)




root.mainloop()

a = pyautogui.getWindowsWithTitle("교육원 운영 자동화 프로그램")[0]

print(a)