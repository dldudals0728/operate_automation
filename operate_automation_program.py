# 공용 import 항목

# 자동화 파일 import 항목

# import 한 파일 안에 import 되어 있는것은 따로 import 안해도 됨 !
import pyautogui # tkinter 창의 정보를 얻기 위한 import
# GUI 파일 import 항목
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk # combobox, progressbar
import tkinter.messagebox as msgbox

import cafe_update_module

import operate_data

from operate_automation_menu import automation
#                                       example
# preform = automation()
# perform.auto_move_class(4, "야간")
# perform.auto_move_report()
# perform.automation_task_students(3, "주간", "요양보호사 자격증 발급,재발급 신청서")
# perform.automation_task_report(5, "주간", "개강보고") # 수료보고가 따로 없기 때문에 kind = 개강보고로 고정 !
# perform.automation_task_temporary(4, "주간", "수료보고")
# perform.mkfile("5기주간0201", "교육수료증명서.hwp") # 뒤에 복사할 파일을 입력할 때 꼭 !!!!! 확장자 명까지 작성하기 ㅎㅎ
# perform.mkattendance(3, "야간")


global radio_num_var
global radio_time_var
global frame_option
global cmbbox

function = automation()

def automation_start():
    ordinal_num = radio_num_var.get()
    time = radio_time_var.get()
    mode = cmbbox.get()
    print("ordinal_num :",ordinal_num, "ordinal_num type :", type(ordinal_num))
    print("time :", time, "time type", type(time))
    print("mode :", mode, "mode type :", type(mode))
    mode_baseinfo = ["출석시간 반영", "교육생 자료 복사"]
    mode_manage = ["교육수료증명서", "대체실습확인서", "요양보호사 자격증 발급,재발급 신청서"]
    mode_report = ["개강보고", "출석부", "실시보고_대체실습", "수료보고_대체실습", "출석부_대체실습"]
    # mode list : "교육수료증명서", "대체실습확인서", "요양보호사 자격증 발급 신청서", "출석시간 반영", "교육생 자료 복사", "개강보고(실시보고)", "종강보고(수료보고)", "출석부", "대체실습"

    if mode == mode_baseinfo[0]:
        function.update_attendance(ordinal_num, time)

    # elif mode == mode_baseinfo[1]:
        # function.mkfile(ordinal_num, time, )

    if mode in mode_manage:
        function.auto_move_class(ordinal_num, time)
        function.automation_task_students(ordinal_num, time, mode, modevar)

    if mode in mode_report:
        if mode == mode_report[0]:
            function.automation_task_report(ordinal_num, time, mode)
        elif mode == mode_report[1]:
            function.mkattendance(ordinal_num, time)
        elif mode == mode_report[2]:
            mode = mode_report[2][:4]
            function.automation_task_temporary(ordinal_num, mode)
        elif mode == mode_report[3]:
            mode = mode_report[3][:4]
            function.automation_task_temporary(ordinal_num, mode)
        elif mode == mode_report[4]:
            msgbox.showerror("업데이트 필요", "대체실습 출석부 작성 자동화 프로그램이 업데이트 되지 않았습니다.(업데이트 필요) ")



def del_widget(user_widget):

    if user_widget.winfo_exists():
        user_widget.destroy()

def add_listbox(listbox):
    group = f"{radio_num_var.get()}기{radio_time_var.get()}"
    for idx, cell in enumerate(function.ws_members["E"], start=1):
        if not group in str(cell.value):
            continue
        string = f"{function.ws_members.cell(row=idx, column=1).value}. {function.ws_members.cell(row=idx, column=18).value}"
        listbox.insert(END, string)
    listbox.config(state=DISABLED)

def selection():
    if cmbbox.get() == "선택":
        msgbox.showinfo("알림", "자동화 옵션을 선택해주세요.")
        return
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

    lst_selection = ["선택", "교육수료증명서", "대체실습확인서", "요양보호사 자격증 발급,재발급 신청서"]
    lst_selection.remove("선택")

    lst_baseinfo = ["출석시간 반영", "교육생 자료 복사"]
    lst_manage = ["교육수료증명서", "대체실습확인서", "요양보호사 자격증 발급,재발급 신청서"]
    lst_report = ["개강보고", "출석부", "실시보고_대체실습", "수료보고_대체실습", "출석부_대체실습"]

    group = f"{radio_num_var.get()}기{radio_time_var.get()}"
    print(group)
    members = 0

    listbox.config(state=NORMAL)
    listbox.delete(0, END)

    if cmbbox.get() == "출석시간 반영":
        info_message = "D:\\"+operate_data.ac_name+"\\교육생관리\\출석부_기관장용\n폴더 내부의 파일들을 참조하여 출석부를 최신화 합니다."
    elif cmbbox.get() == "교육생 자료 복사":
        info_message = "D:\\Master\\mkfile\n폴더 내부의 파일들을 참조하여 출석부를 최신화 합니다."
    elif cmbbox.get() in lst_manage or cmbbox.get() in lst_report:
        info_message = "작성된 명단의 내용을 참조하여 \"" + cmbbox.get() + "\" 작성을 시작합니다."
    
    listbox.insert(END, info_message)
    add_listbox(listbox)
    
        

    
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

    radio_xlsx.select()
    radio_xlsx["state"] = "disable"
    radio_hwp["state"] = "disable"

def manage():
    global frame_option
    global cmbbox

    lst = ["선택", "교육수료증명서", "대체실습확인서", "요양보호사 자격증 발급,재발급 신청서"]
    cmbbox["values"] = lst
    cmbbox.current(0)

    radio_xlsx.select()
    radio_xlsx["state"] = "normal"
    radio_hwp["state"] = "normal"

def report():
    global frame_option
    global cmbbox
    global chkvar_temp

    lst = ["선택", "개강보고", "출석부", "실시보고_대체실습", "수료보고_대체실습", "출석부_대체실습"]
    cmbbox["values"] = lst
    cmbbox.current(0)

    radio_hwp.select()
    radio_xlsx["state"] = "disable"
    radio_hwp["state"] = "disable"
        
def test():
    print(modevar.get())

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
    label3.grid(row=3, column=0, sticky=W)

    label4 = Label(frame, text="ver. 0.2.1   combobox 동적 값 할당   21.02.16\n\n")
    label4.grid(row=4, column=0, sticky=W)

    label5 = Label(frame, text="ver. 0.3.1   진행 업무 확인, progressbar 추가   21.02.25\n\n")
    label5.grid(row=5, column=0, sticky=W)

    update_window.mainloop()

def start():
    print("radio num var : " + str(radio_num_var.get()))
    print("radio time var : " + str(radio_time_var.get()))

    print(cmbbox.get())

    for i in range(101):
        pvar.set(i)
        progressbar.update()
        pyautogui.sleep(0.01)

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
frame_1 = Frame(main_frame, bd=1, relief="solid")
frame_1.pack(fill="x")

frame_option = LabelFrame(frame_1, text="업무 자동화")
frame_option.pack(fill="both")

# Option 선택 combobox frame
frame_cmbbox = Frame(frame_option)
frame_cmbbox.pack()
label = Label(frame_cmbbox, text="Option")
label.pack(side="left", padx=5, pady=5)

lst = ["선택"]
cmbbox = ttk.Combobox(frame_cmbbox, state="readonly", values=lst, width=30)
cmbbox.current(0)
cmbbox.pack(side="left", padx=5, pady=5)

# excel version frame
frame_mode = Frame(frame_cmbbox)
frame_mode.pack(side="right")

label_mode = Label(frame_mode, text="mode selection")
label_mode.pack(side="top")

frame_mode_select = Frame(frame_mode)
frame_mode_select.pack(side="bottom")

modevar = BooleanVar()
radio_xlsx = Radiobutton(frame_mode_select, text="Excel", value=True, variable=modevar)
radio_xlsx.select()
radio_hwp = Radiobutton(frame_mode_select, text="한글", value=False, variable=modevar)
radio_xlsx.pack(side="left", padx=5, pady=5)
radio_hwp.pack(side="right", padx=5, pady=5)
basic()

# 2번 프레임
frame_2 = Frame(main_frame)
frame_2.pack(fill="both")

# 진행상황 프레임
frame_progress = Frame(frame_2)
frame_progress.pack(fill="both")
frame_list = Frame(frame_progress)
frame_list.pack(fill="both")
scrollbar = Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")
listbox = Listbox(frame_list, yscrollcommand=scrollbar.set, disabledforeground="black")
listbox.pack(fill="both")
pvar = DoubleVar()
progressbar = ttk.Progressbar(frame_progress, maximum=100, variable=pvar)
progressbar.pack(side="bottom", fill="both")

# 서브 프레임
sub_frame = Frame(root, relief="solid", bd=1)
sub_frame.pack(side="right", padx=5, pady=5, fill="both", expand=True)

# side = bottom
# ver 0.1.1 : 프레임 순서 설정  / 0.1.2 : basic 함수에 프레임 추가로 가독성 상승
label_verinfo = Label(sub_frame, text="버전정보 0.3.1")
label_verinfo.pack(side="bottom")

btn_update = Button(sub_frame, text="업데이트 내역", command=check_update, width=12)
btn_update.pack()

btn_select = Button(sub_frame, text="시작", command=start, width=12)
btn_select.pack(padx=5, pady=5)

btn_cafe = Button(sub_frame, text="카페 자동화", command=cafe_update, width=12)
btn_cafe.pack(padx=5, pady=5)

btn_quit = Button(sub_frame, text="종료", command=root.quit, width=12)
btn_quit.pack(padx=5, pady=5)



scrollbar.config(command=listbox.yview)
root.mainloop()

a = pyautogui.getWindowsWithTitle("교육원 운영 자동화 프로그램")[0]

print(a)