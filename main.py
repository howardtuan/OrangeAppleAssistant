import tkinter.messagebox as messagebox

from ttkbootstrap import Style

from helpers import aichat, get_course_details
from ui_components import create_ui


def build_contact_book(
    name,
    course_name,
    lesson_number,
    lesson_topic,
    schedule_text,
    performance,
    questions,
):
    performance_text = performance if performance else "未提供"
    questions_text = questions if questions else "未提供"

    return (
        f"{name}今天在{course_name}完成第 {lesson_number} 課〈{lesson_topic}〉。"
        f"本堂課內容是{lesson_topic}。"
        f"{name}上課表現：{performance_text}。"
        f"進度狀態：{schedule_text}。"
        "\n\n"
        f"本堂課驗收問題：【{questions_text}】。"
    )


def on_generate():
    name = name_entry.get().strip() or "學生"
    course_code = course_combo.get()
    lesson_code = lesson_combo.get()
    display_course = display_course_combo.get()
    display_lesson = display_lesson_entry.get().strip()

    course_name, lesson_list = get_course_details(course_code, lesson_code)
    lesson_index = 0
    if lesson_code and lesson_code[1:].isdigit():
        lesson_index = int(lesson_code[1:]) - 1

    if 0 <= lesson_index < len(lesson_list):
        lesson_topic = lesson_list[lesson_index]
    else:
        lesson_topic = "（未找到課程內容）"

    schedule_text = "進度正常" if schedule_var.get() == "fixed" else "進度落後"

    if display_course and display_course != "(原始課名)":
        output_course_name = display_course
    else:
        output_course_name = course_name

    display_number = None
    if display_lesson.isdigit():
        number = int(display_lesson)
        if 1 <= number <= 45:
            display_number = number

    if display_number is None:
        if lesson_code and lesson_code[1:].isdigit():
            display_number = int(lesson_code[1:])
        else:
            display_number = 1

    performance = performance_text.get("1.0", "end").strip()
    questions = questions_text.get("1.0", "end").strip()
    previous_questions = previous_questions_text.get("1.0", "end").strip()

    contact_body = build_contact_book(
        name,
        output_course_name,
        display_number,
        lesson_topic,
        schedule_text,
        performance,
        questions,
    )
    has_previous = previous_var.get() == 1
    previous_text = " ".join(previous_questions.split()) if previous_questions else "未提供"
    opening = ""
    if has_previous:
        opening = f"已完成上週內容，驗收問題為：【{previous_text}】。\n\n"
    contact_book = opening + contact_body

    if ai_var.get() == 1:
        output = aichat(contact_book)
        marker = "已完成上週內容，驗收問題為：【"
        cleaned = output.lstrip()
        if marker in cleaned:
            idx = cleaned.find(marker)
            cleaned = cleaned[idx + len(marker):]
            end_idx = cleaned.find("】")
            if end_idx != -1:
                cleaned = cleaned[end_idx + 1 :].lstrip("。\n ")
        if has_previous:
            output = opening + cleaned
        else:
            output = cleaned
    else:
        output = contact_book

    # 確保一定有本堂課驗收問題
    if "本堂課驗收問題" not in output:
        questions_fallback = questions if questions else "未提供"
        output = output.rstrip() + f"\n\n本堂課驗收問題：【{questions_fallback}】。"

    window.clipboard_clear()
    window.clipboard_append(output)
    window.update()

    messagebox.showinfo(title="已產生聯絡簿", message=f"內容已複製到剪貼簿：\n\n{output}")


style = Style(theme="flatly")
window = style.master
(
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
) = create_ui(window, on_generate)

window.mainloop()
