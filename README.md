# OrangeAppleAssistant

這是一個用於管理和追蹤學生程式課程學習進度的工具，通過 OpenAI 的 GPT 模型，根據用戶輸入自動生成詳細的學習報告。

## 功能
- 讓用戶輸入課程細節和學生的學習表現。
- 自動生成專業且禮貌的學習報告。
- 支援多種程式課程，包括 Scratch、Python、JavaScript 和 AI等等。(可在db.py自行新增)
- 使用 OpenAI 的 API 進行文字生成。

## 需求條件
- Python 3.10 或更高版本
- 包含 OpenAI API 金鑰的 `config.json` 文件（需自行提供）

## 安裝步驟
1. 複製專案到本地：
   ```bash
   git clone https://github.com/your-repo/orangeapple.git
   cd orangeapple
   ```
2. 建立虛擬環境（可選但建議使用）：
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows 系統執行：venv\Scripts\activate
   ```
3. 安裝所需的套件：
   ```bash
   pip install -r requirements.txt
   ```
4. 在專案根目錄下建立 config.json 文件，結構如下：
   ```json
   {
    "openai_api_key": "your-openai-api-key"
   }
   ```
## 使用方法
1.  執行主程式：
    ```bash
    python main.py
    ```
2. 在圖形化介面中輸入學生資訊、課程信息和學習表現。
3. 可直接複製生成的學習報告，或保存用於後續使用。
## 專案結構
   ```bash
  OrangeApple/
  │
  ├── db.py                # 包含預定義的課程和章節內容
  ├── helpers.py           # 助手函數，包括 OpenAI API 的整合
  ├── main.py              # 主程式邏輯及圖形化介面
  ├── config.json          # 配置文件，存放 OpenAI API 金鑰（需自行建立）
  ├── requirements.txt     # Python 依賴列表
  └── README.md            # 專案說明文件
   ```
## JSON API 金鑰需求
此專案需要用戶在 config.json 文件中提供有效的 OpenAI API 金鑰才能正常運行。請確保金鑰可用且未過期。
