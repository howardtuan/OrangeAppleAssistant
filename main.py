import tkinter as tk
from tkinter import ttk
from tkinter import Checkbutton
import tkinter.messagebox
from ttkbootstrap import Style
from helpers import aichat, get_course_details
from ui_components import create_ui

def onOK():
    global entry, comboExample1, comboExample2, radiobutton_var, CheckVarAI, CheckVar1, entrystudy
    CodeName, WhatList = get_course_details(comboExample1.get(), comboExample2.get())
    WhatInside = WhatList[int(comboExample2.get()[1:]) - 1]
    study_performance = entrystudy.get()  # 獲取學習表現

    if radiobutton_var.get() == '1':
        schedule_str = "專案完整完成囉！請繼續保持～"
    else:
        schedule_str = "專案尚未完成哦！有空的話可以利用閒暇時間補完～加油！"
    
    if CheckVar1.get() == 1:  # 上週未完成專案完成
        msg = "這次在課程中已經將上次未完成的專案完成囉！\n"
    else:# 上週進度正常
        msg = ""
    if CheckVarAI.get() == 1:
        msg += f"{entry.get()}今天的進度是{CodeName}的第{comboExample2.get()[1:]}課－{WhatInside}\n-------------------------------------------------\n{entry.get()}的{schedule_str}"
        
        AI_MSG = aichat(msg, study_performance)

        window.clipboard_clear()
        window.clipboard_append(AI_MSG)
        window.update()
        tkinter.messagebox.showinfo(title="訊息已複製", message=f"已將內容複製到剪貼板：\n\n{AI_MSG}")
    else:
        msg += f"{entry.get()}今天的進度是{CodeName}的第{comboExample2.get()[1:]}課－{WhatInside}\n-------------------------------------------------\n{entry.get()}的{schedule_str}"
        window.clipboard_clear()
        window.clipboard_append(msg)
        window.update()
        tkinter.messagebox.showinfo(title="訊息已複製", message=f"已將內容複製到剪貼板：\n\n{msg}")


# 初始化 UI 和主視窗
style = Style(theme='darkly')
window = style.master
entry, entrystudy, comboExample1, comboExample2, radiobutton_var, CheckVarAI, CheckVar1 = create_ui(window, onOK)
window.mainloop()
