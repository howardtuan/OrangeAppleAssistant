import json
import sys
from pathlib import Path

import openai


def load_api_key_from_json(file_path="config.json"):
    """
    從 JSON 配置檔讀取 OpenAI API Key
    """
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    config_path = Path(file_path)

    if not config_path.is_absolute():
        config_path = base_dir / config_path

    if not config_path.exists():
        fallback = Path.cwd() / file_path
        if fallback.exists():
            config_path = fallback

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)
        return config.get("openai_api_key")


def aichat(msg, config_path="config.json"):
    api_key = load_api_key_from_json(config_path)
    if not api_key:
        raise ValueError("未找到 OpenAI API Key，請確認 config.json。")

    openai.api_key = api_key

    system_prompt = (
        "你是老師，請把輸入內容整理成聯絡簿文章。"
        "語氣自然、口語一點，不要官腔，不要敬語或客套語。"
        "保持成段落、不要條列或標題。"
        "若開頭包含「已完成上週內容，驗收問題為：【...】。」這句，請原封不動保留在最前面。"
        "內容需包含：學生、課程、課堂內容、學習表現、驗收問題、進度狀態。"
        "若有資訊不足，請用自然語句帶過，不要出現「未填寫」字樣。"
    )

    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": msg},
        ],
    )

    return completion.choices[0].message["content"]


# db.py
import db


def get_course_details(combo_value, lesson_value):
    """
    根據課程與課次回傳課程名稱與內容清單

    Args:
        combo_value (str): 課程代碼 (例如 "Scratch0")
        lesson_value (str): 課次 (例如 "L1", "L2")

    Returns:
        tuple: (課程名稱, 課程內容清單)
    """
    course_mapping = {
        "Scratch0": ("Scratch 入門", db.Scratch0),
        "Scratch1": ("Scratch 進階", db.Scratch1),
        "Python": ("Python 基礎", db.Python),
        "Python2": ("Python 進階", db.Python2),
        "JavaScript": ("JavaScript 基礎", db.JavaScript),
        "JavaScript_New": ("JavaScript 進階", db.JavaScript_New),
        "HTML": ("HTML5 基礎", db.HTML),
        "DB": ("資料庫與 SQL", db.DB),
        "Algorithm": ("演算法與邏輯", db.Algorithm),
        "AI": ("AI 基礎", db.AI),
    }

    course_name, course_content = course_mapping.get(combo_value, ("未知課程", []))
    return course_name, course_content
