import tkinter as tk
from tkinter import ttk

def create_ui(window, onOK_callback):
    # 建立 UI 元件
    label = ttk.Label(window, text='姓名')
    label.grid(row=2, column=2)

    entry = tk.Entry(window, width=20)
    entry.grid(row=2, column=3)

    label_study = ttk.Label(window, text='學習表現（AI判斷用）')
    label_study.grid(row=3, column=4)

    entrystudy = tk.Entry(window, width=20)
    entrystudy.grid(row=3, column=5)

    comboExample1 = ttk.Combobox(window, values=["Scratch0", "Scratch1", "Python","Python2","JavaScript","JavaScript_New","HTML","DB","Algorithm","AI"])
    comboExample1.current(1)
    comboExample1.grid(row=3, column=2)

    comboExample2 = ttk.Combobox(window, values=[f"L{i}" for i in range(1, 16)])
    comboExample2.current(1)
    comboExample2.grid(row=3, column=3)

    CheckVar1 = tk.IntVar()
    C1 = tk.Checkbutton(window, text="上週未完成專案", variable=CheckVar1, onvalue=1, offvalue=0)
    C1.grid(row=4, column=2)

    CheckVarAI = tk.IntVar()
    C2 = tk.Checkbutton(window, text="使用AI", variable=CheckVarAI, onvalue=1, offvalue=0)
    C2.grid(row=5, column=2)

    radiobutton_var = tk.StringVar()
    myradiobutton1 = tk.Radiobutton(window, text='完成', value=1, variable=radiobutton_var)
    myradiobutton1.select()
    myradiobutton1.grid(row=4, column=3)

    myradiobutton2 = tk.Radiobutton(window, text='未完成', value=2, variable=radiobutton_var)
    myradiobutton2.grid(row=5, column=3)

    button = ttk.Button(window, text="OK", command=onOK_callback, style='success.TButton')
    button.grid(row=7, column=3)

    return entry, entrystudy, comboExample1, comboExample2, radiobutton_var, CheckVarAI, CheckVar1
