import openai
import json

def load_api_key_from_json(file_path="config.json"):
    """
    從 JSON 配置文件中加載 API 金鑰
    """
    with open(file_path, "r") as file:
        config = json.load(file)
        return config.get("openai_api_key")
    
def aichat(msg,study,config_path="config.json"):
    # 加載 API 金鑰
    api_key = load_api_key_from_json(config_path)
    if not api_key:
        raise ValueError("API 金鑰未設定或無效")

    openai.api_key = api_key

    """
    AI Chat Function for processing student progress and performance.
    Args:
        api_key (str): OpenAI API key.
        msg (str): Student's progress and record.
        study (str): Student's learning performance.
    Returns:
        str: AI response with modified content.
    """
    start = """你是一個國小至高中的某間程式設計補習班助理，要負責填寫學生上課學習狀況，待會會給你今天學生的「學習紀錄」以及「學習表現」，請使用有禮貌的方式改寫成一個新的文案！注意，學習紀錄的內容不可偏離原意！也不要把文字弄得太文謅謅，這只是一般的聯絡簿。文字處理時請寫成1~2段落，不需要用分隔線。也不需要加上「親愛的家長您好」這種東西，說學生學習態度時也可以自然一點！"""
    
    ori_msg="""
    小明今天的進度是Scratch菁英班的第2課－「絕佳配對」，卡牌配對的小遊戲，除了認識全等與相似以外，也有用程式邏輯去判斷是否全等跟是否相似。這堂課也運用到很多清單的邏輯，程式碼也變非常多，所以寫程式的時候一定要非常細心哦～
    -------------------------------------------------
    小明的專案完整完成囉！請繼續保持～"""
    # 使用OpenAI GPT-4o Mini 模型進行對話
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": start},
            {"role": "user", "content": "學習紀錄："+ori_msg+"上課表現："+"認真 準時完成"},
            {"role": "assistant", "content": "小明同學在今天的課程中完成了Scratch菁英班的第2課「絕佳配對」。這堂課的內容涉及到卡牌配對的小遊戲，除了學習全等與相似的概念外，他還運用程式邏輯去判斷卡牌是否全等和相似。這一課程中，他也學習了如何運用清單的邏輯並寫出複雜的程式碼。今天的專案都有準時完成哦！而且上課時也非常認真，要繼續保持哦！加油～"},    
            {"role": "user", "content": "學習紀錄："+msg+"上課表現："+study},
        ]
    )

    # 獲取機器人的回答
    ai_response = completion.choices[0].message['content']

    
    # 返回AI回答
    return ai_response

# 引用 db.py
import db

def get_course_details(combo_value, lesson_value):
    """
    根據選擇的課程和章節，取得課程詳細資訊。
    
    Args:
        combo_value (str): 使用者選擇的課程 (如 "Scratch0")。
        lesson_value (str): 使用者選擇的章節 (如 "L1", "L2")。

    Returns:
        tuple: 包含課程名稱 (str) 和課程內容 (list)。
    """
    # 定義課程對應的名稱
    course_mapping = {
        "Scratch0": ("Scratch實戰班", db.Scratch0),
        "Scratch1": ("Scratch菁英班", db.Scratch1),
        "Python": ("Python程式開發班", db.Python),
        "Python2": ("Python程式進階班", db.Python2),
        "JavaScript": ("JavaScript程式開發班", db.JavaScript),
        "JavaScript_New": ("JavaScript進階班", db.JavaScript_New),
        "HTML": ("HTML5網頁程式開發班", db.HTML),
        "DB": ("資料庫應用班", db.DB),
        "Algorithm": ("演算法研究與應用班", db.Algorithm),
        "AI": ("AI人工智慧班", db.AI)
    }

    # 從映射中取得課程名稱與內容
    course_name, course_content = course_mapping.get(combo_value, ("未知課程", []))

    # 回傳課程名稱和內容
    return course_name, course_content

