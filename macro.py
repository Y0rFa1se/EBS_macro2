import time
import webbrowser

from tkinter import *
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk

import pyautogui

def Gui():
    gui = Tk()
    gui.title("EBS macro")
    gui.iconbitmap("imgs/icon.ico")
    gui.geometry("700x600")
    gui.resizable(False, False)

    label1 = Label(gui, text = "EBS macro\n")
    label1.pack()

    txt = Text(gui, width=70, height=20)
    txt.pack()
    txt.insert(END, """이 부분을 지우고
    
'강의링크'
'강의시간'
'강의링크'
'강의시간'
    
순서로 적어주세요
    
예시)
    
https://www.naver.com
1:00:00
https://www.youtube.com
1:00""")

    Label(gui, text="\n").pack()

    def add():
        with open("files/lectures.txt", "w") as lec:
            lec.write(txt.get("1.0", END))
        log.insert(END, "강의 추가됨\n")
        print(txt.get("1.0", END))
        print("강의 추가됨")
        msgbox.showinfo("강의 추가됨", "강의 추가됨")

    def openbrows():
        webbrowser.open(url = "https://oc.ebssw.kr/")
        print("브라우저 엶")
        log.insert(END, "브라우저 엶\n")

    def run():
        pvar.set(0)
        links = []
        lrt = []

        with open("files/lectures.txt", "r") as lec:
            while True:
                lecs = lec.readline().replace("\n", "")
                if (lecs == ""):
                    break
                lrntime = lec.readline().replace("\n", "")
                links.append(lecs)
                if (lrntime.count(":") == 2):
                    l1, l2, l3 = map(int, lrntime.split(":"))
                    lrntime = (l1 * 3600) + (l2 * 60) + l3 + 10
                elif (lrntime.count(":") == 1):
                    l1, l2 = map(int, lrntime.split(":"))
                    lrntime = (l1 * 60) + l2 + 10
                lrt.append(lrntime)

        tolrt = 0
        leftt = 0
        for j in lrt:
            tolrt += j
        progbar.config(maximum = tolrt)
        pvar.set(leftt)
        toclock = str(tolrt // 3600) + ":" + str((tolrt % 3600) // 60) + ":" + str(tolrt % 60)

        for k in range(len(links)):
            webbrowser.open(links[k])
            time.sleep(3)

            for i in range(10, 7, -1):
                scan = False
                log.insert(END, "현재 정확도" + str(i * 0.1) + "\n")
                print("현재 정확도" + str(i * 0.1))
                ploc = pyautogui.locateOnScreen("imgs/click.PNG", confidence=(i * 0.1))

                if (ploc != None):
                    log.insert(END, "스캔완료\n")
                    print("스캔완료")
                    scan = True
                    break

            txt.delete("1.0", END)
            txt.insert(END, "시간 총합 : " + toclock + "\n")
            txt.insert(END, "강의 수 : " + str(len(links)) + "\n")
            txt.insert(END, "남은 강의 수 : " + str(len(links) - (k + 1)) + "\n")
            time.sleep(3)

            if (scan == True):
                pyautogui.click(pyautogui.center(ploc))

            print(lrt[k])
            time.sleep(lrt[k])
            leftt += lrt[k]
            pvar.set(leftt)

    def listlecs():
        log.insert(END, "리스트 엶\n")
        print("리스트 엶")
        links = []
        lrt = []

        with open("files/lectures.txt", "r") as lec:
            while True:
                lecs = lec.readline().replace("\n", "")
                if (lecs == ""):
                    break
                lrntime = lec.readline().replace("\n", "")
                links.append(lecs)
                lrt.append(lrntime)

        txt.delete("1.0", END)
        for i in range(len(links)):
            txt.insert(END, links[i] + "\n")
            txt.insert(END, lrt[i] + "\n")

    def check():
        log.insert(END, "click.png 스캔시작\n")
        print("click.png 스캔시작")
        scan = False
        for i in range(10, 7, -1):
            log.insert(END, "현재 정확도" + str(i * 0.1) + "\n")
            print("현재 정확도" + str(i * 0.1))
            ploc = pyautogui.locateOnScreen("imgs/click.PNG", confidence = (i * 0.1))
            if (ploc != None):
                log.insert(END, "스캔완료\n")
                print("스캔완료")
                msgbox.showinfo("스캔완료", "오브젝트 발견, 정확도 : " + str(i * 0.1))
                scan = True
                break
        if (scan == False):
            log.insert(END, "오브젝트 발견하지 못함\n")
            print("오브젝트 발견하지 못함")
            msgbox.showwarning("스캔완료", "오브젝트 발견하지 못함")

    def help():
        txt.delete("1.0", END)
        txt.insert(END, """add : 텍스트박스에 적은 링크와 시간을 files/lectures.txt에 저장함
open : 온라인클래스 창을 엶
run : 저장된 강의 링크와 시간을 이용해 강의 자동재생
list : files/lectures.txt에 저장된 강의 목록을 표효시함
check : 이미지 인식 확인 ("확인" 버튼의 인식에 대한 정보를 표시한다)
help : 이거

첫실행시 imgs폴더에 click.png를 등록한다 (영상참고)


실행 방법

텍스트박스에 강의 링크와 시간을 적기 -> add -> open -> 로그인 -> run
※실행중에는 절대 창을 건드리지 마세요※""")
        log.insert(END, "도움말 엶\n")
        print("도움창 엶")

    pvar = IntVar()
    progbar = ttk.Progressbar(gui, maximum = 100, length = 600, variable = pvar)
    progbar.pack()

    Label(gui, text = "\n").pack()

    btns = LabelFrame(gui, text = "실행")
    btns.pack()

    Button(btns, text = "add", command = add, padx = 20, pady = 10).grid(row = 1, column = 0)
    Label(btns, text = "   ").grid(row = 1, column = 1)
    Button(btns, text = "open", command = openbrows, padx = 20, pady = 10).grid(row = 1, column = 2)
    Label(btns, text="   ").grid(row=1, column=3)
    Button(btns, text="run", command = run, padx=20, pady=10).grid(row=1, column=4)
    Button(btns, text="check", command = check, padx=20, pady=10).grid(row=2, column=0)
    Label(btns, text="   ").grid(row=2, column=1)
    Button(btns, text="list", command=listlecs, padx=20, pady=10).grid(row=2, column=2)
    Label(btns, text="   ").grid(row=2, column=3)
    Button(btns, text="help", command=help, padx=20, pady=10).grid(row=2, column=4)

    Label(gui, text="\nlog").pack()

    log = Text(gui, width = 50, height = 3)
    log.pack()
    
    print("프로그램 실행됨")
    log.insert(END, "프로그램 실행됨\n")

    gui.mainloop()

Gui()