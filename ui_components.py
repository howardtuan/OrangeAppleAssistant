import tkinter as tk
from tkinter import messagebox, ttk

from question_bank import draw_lesson_questions, format_numbered_questions


def create_ui(window, on_generate):
    window.title("學生聯絡簿產生器")
    window.geometry("1180x780")
    window.minsize(1120, 740)

    root = ttk.Frame(window, padding=20)
    root.grid(sticky="nsew")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    header = ttk.Frame(root)
    header.grid(row=0, column=0, sticky="ew")
    header.columnconfigure(0, weight=1)

    title = ttk.Label(header, text="學生聯絡簿產生器", font=("Microsoft JhengHei", 20, "bold"))
    subtitle = ttk.Label(
        header,
        text="快速整理課堂紀錄，包含驗收問題與學習表現",
        font=("Microsoft JhengHei", 11),
    )
    title.grid(row=0, column=0, sticky="w")
    subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

    content = ttk.Frame(root)
    content.grid(row=1, column=0, sticky="nsew", pady=(16, 0))
    root.rowconfigure(1, weight=1)
    content.columnconfigure(0, weight=1)
    content.columnconfigure(1, weight=1)
    content.rowconfigure(0, weight=1)

    left = ttk.LabelFrame(content, text="基本資料", padding=16)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    right = ttk.LabelFrame(content, text="課堂紀錄", padding=16)
    right.grid(row=0, column=1, sticky="nsew")
    left.columnconfigure(1, weight=1)
    right.columnconfigure(0, weight=1)
    right.rowconfigure(3, weight=1)
    right.rowconfigure(5, weight=1)

    ttk.Label(left, text="學生姓名", font=("Microsoft JhengHei", 11)).grid(
        row=0, column=0, sticky="w", pady=(0, 8)
    )
    name_entry = ttk.Entry(left, width=24)
    name_entry.grid(row=0, column=1, sticky="ew", pady=(0, 8))

    ttk.Label(left, text="課程", font=("Microsoft JhengHei", 11)).grid(
        row=1, column=0, sticky="w", pady=(0, 8)
    )
    course_combo = ttk.Combobox(
        left,
        values=["Scratch0", "Scratch1", "Python", "Python2", "JavaScript", "JavaScript_New", "HTML", "DB", "Algorithm", "AI"],
        state="readonly",
    )
    course_combo.current(1)
    course_combo.grid(row=1, column=1, sticky="ew", pady=(0, 8))

    ttk.Label(left, text="課次", font=("Microsoft JhengHei", 11)).grid(
        row=2, column=0, sticky="w", pady=(0, 8)
    )
    lesson_combo = ttk.Combobox(
        left,
        values=[f"L{i}" for i in range(1, 16)],
        state="readonly",
    )
    lesson_combo.current(1)
    lesson_combo.grid(row=2, column=1, sticky="ew", pady=(0, 8))

    ttk.Label(left, text="聯絡簿課程名稱", font=("Microsoft JhengHei", 11)).grid(
        row=3, column=0, sticky="w", pady=(0, 8)
    )
    display_course_combo = ttk.Combobox(
        left,
        values=["(原始課名)", "線上菁英初階", "線上菁英中階", "線上菁英高階"],
        state="readonly",
    )
    display_course_combo.current(0)
    display_course_combo.grid(row=3, column=1, sticky="ew", pady=(0, 8))

    ttk.Label(left, text="聯絡簿堂數（1~45）", font=("Microsoft JhengHei", 11)).grid(
        row=4, column=0, sticky="w", pady=(0, 8)
    )
    display_lesson_entry = ttk.Entry(left, width=8)
    display_lesson_entry.grid(row=4, column=1, sticky="w", pady=(0, 8))
    display_lesson_entry.insert(0, str(int(lesson_combo.get()[1:])) if lesson_combo.get() else "")

    def sync_display_lesson(_event=None):
        value = lesson_combo.get()
        if value and value[1:].isdigit():
            display_lesson_entry.delete(0, "end")
            display_lesson_entry.insert(0, value[1:])

    lesson_combo.bind("<<ComboboxSelected>>", sync_display_lesson)

    def get_previous_lesson_code():
        value = lesson_combo.get()
        if value and value[1:].isdigit():
            previous_number = max(1, int(value[1:]) - 1)
            return f"L{previous_number}"
        return value

    def draw_formatted_questions(course_code, lesson_code):
        try:
            questions = draw_lesson_questions(course_code, lesson_code)
        except (FileNotFoundError, ValueError) as exc:
            messagebox.showwarning(title="無法抽題", message=str(exc))
            return None

        return format_numbered_questions(questions)

    def replace_text(text_widget, value):
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", value)

    def fill_questions(text_widget, course_code, lesson_code):
        value = draw_formatted_questions(course_code, lesson_code)
        if value:
            replace_text(text_widget, value)

    def get_text_value(text_widget):
        return text_widget.get("1.0", "end").strip()

    ttk.Label(left, text="進度狀態", font=("Microsoft JhengHei", 11)).grid(
        row=5, column=0, sticky="w", pady=(0, 8)
    )
    schedule_var = tk.StringVar(value="fixed")
    schedule_frame = ttk.Frame(left)
    schedule_frame.grid(row=5, column=1, sticky="w", pady=(0, 8))
    ttk.Radiobutton(schedule_frame, text="進度正常", value="fixed", variable=schedule_var).grid(
        row=0, column=0, padx=(0, 12)
    )
    ttk.Radiobutton(schedule_frame, text="進度落後", value="makeup", variable=schedule_var).grid(
        row=0, column=1
    )

    previous_var = tk.IntVar(value=0)
    ttk.Checkbutton(left, text="上週未完成", variable=previous_var).grid(
        row=6, column=0, columnspan=2, sticky="w", pady=(4, 0)
    )

    ai_var = tk.IntVar(value=1)
    ttk.Checkbutton(left, text="AI 潤飾", variable=ai_var).grid(
        row=7, column=0, columnspan=2, sticky="w", pady=(4, 0)
    )

    suggestion = ttk.LabelFrame(left, text="驗收問題建議", padding=12)
    suggestion.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(16, 0))
    suggestion.columnconfigure(1, weight=1)

    ttk.Label(suggestion, text="抽題課程", font=("Microsoft JhengHei", 10)).grid(
        row=0, column=0, sticky="w", pady=(0, 8)
    )
    draw_course_combo = ttk.Combobox(
        suggestion,
        values=list(course_combo["values"]),
        state="readonly",
        width=18,
    )
    draw_course_combo.set(course_combo.get())
    draw_course_combo.grid(row=0, column=1, sticky="ew", pady=(0, 8))

    ttk.Label(suggestion, text="抽題課次", font=("Microsoft JhengHei", 10)).grid(
        row=1, column=0, sticky="w", pady=(0, 8)
    )
    draw_lesson_combo = ttk.Combobox(
        suggestion,
        values=list(lesson_combo["values"]),
        state="readonly",
        width=10,
    )
    draw_lesson_combo.set(lesson_combo.get())
    draw_lesson_combo.grid(row=1, column=1, sticky="ew", pady=(0, 8))

    standalone_questions_text = tk.Text(suggestion, height=4, wrap="word")
    standalone_questions_text.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 8))

    standalone_actions = ttk.Frame(suggestion)
    standalone_actions.grid(row=3, column=0, columnspan=2, sticky="ew")
    for index in range(4):
        standalone_actions.columnconfigure(index, weight=1)

    def draw_standalone_questions():
        value = draw_formatted_questions(draw_course_combo.get(), draw_lesson_combo.get())
        if value:
            replace_text(standalone_questions_text, value)

    def paste_standalone_questions(target_text):
        value = get_text_value(standalone_questions_text)
        if not value:
            messagebox.showwarning(title="尚未抽題", message="請先選擇課程與課次後按「獨立抽三題」。")
            return
        replace_text(target_text, value)

    def copy_standalone_questions():
        value = get_text_value(standalone_questions_text)
        if not value:
            messagebox.showwarning(title="尚未抽題", message="請先選擇課程與課次後按「獨立抽三題」。")
            return
        window.clipboard_clear()
        window.clipboard_append(value)
        window.update()
        messagebox.showinfo(title="已複製", message="抽出的題目已複製到剪貼簿。")

    ttk.Button(standalone_actions, text="獨立抽三題", command=draw_standalone_questions).grid(
        row=0, column=0, sticky="ew", padx=(0, 6)
    )
    ttk.Button(
        standalone_actions,
        text="貼到本堂",
        command=lambda: paste_standalone_questions(questions_text),
    ).grid(row=0, column=1, sticky="ew", padx=(0, 6))
    ttk.Button(
        standalone_actions,
        text="貼到上週",
        command=lambda: paste_standalone_questions(previous_questions_text),
    ).grid(row=0, column=2, sticky="ew", padx=(0, 6))
    ttk.Button(standalone_actions, text="複製", command=copy_standalone_questions).grid(
        row=0, column=3, sticky="ew"
    )

    ttk.Label(right, text="學習表現（可簡短描述）", font=("Microsoft JhengHei", 11)).grid(
        row=0, column=0, sticky="w"
    )
    performance_text = tk.Text(right, height=4, wrap="word")
    performance_text.grid(row=1, column=0, sticky="ew", pady=(6, 16))

    questions_header = ttk.Frame(right)
    questions_header.grid(row=2, column=0, sticky="ew")
    questions_header.columnconfigure(0, weight=1)
    ttk.Label(questions_header, text="本堂課驗收問題（可條列）", font=("Microsoft JhengHei", 11)).grid(
        row=0, column=0, sticky="w"
    )
    ttk.Button(
        questions_header,
        text="抽三題帶入",
        command=lambda: fill_questions(questions_text, course_combo.get(), lesson_combo.get()),
    ).grid(row=0, column=1, sticky="e")
    questions_text = tk.Text(right, height=6, wrap="word")
    questions_text.grid(row=3, column=0, sticky="ew", pady=(6, 12))

    previous_questions_header = ttk.Frame(right)
    previous_questions_header.grid(row=4, column=0, sticky="ew")
    previous_questions_header.columnconfigure(0, weight=1)
    ttk.Label(
        previous_questions_header,
        text="上週進度驗收問題（可條列）",
        font=("Microsoft JhengHei", 11),
    ).grid(row=0, column=0, sticky="w")
    ttk.Button(
        previous_questions_header,
        text="抽上一課帶入",
        command=lambda: fill_questions(previous_questions_text, course_combo.get(), get_previous_lesson_code()),
    ).grid(row=0, column=1, sticky="e")
    previous_questions_text = tk.Text(right, height=5, wrap="word")
    previous_questions_text.grid(row=5, column=0, sticky="nsew", pady=(6, 0))

    action = ttk.Frame(root)
    action.grid(row=2, column=0, sticky="ew", pady=(16, 0))
    action.columnconfigure(0, weight=1)
    generate_btn = ttk.Button(action, text="產生聯絡簿", command=on_generate, style="success.TButton")
    generate_btn.grid(row=0, column=0, sticky="e")

    return (
        name_entry,
        performance_text,
        questions_text,
        previous_questions_text,
        course_combo,
        lesson_combo,
        display_course_combo,
        display_lesson_entry,
        schedule_var,
        previous_var,
        ai_var,
    )
