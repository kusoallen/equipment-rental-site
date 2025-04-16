
# 裝備租借展示網站（使用 Streamlit）

## 🚀 如何部署

1. 前往 https://streamlit.io/cloud 登入並建立新 App
2. 將此專案上傳到 GitHub（包含 app.py 與 requirements.txt）
3. 在 Streamlit Cloud 選擇你的 GitHub 專案部署
4. 開啟網頁後，即可自動讀取 Google Sheet 並顯示裝備卡片

## ✅ 功能

- 自動讀取 Google Sheet（需設為公開）
- 圖片以 Google Drive 提供（請將每張圖片設為「任何人可檢視」，並使用圖片 ID 替換 `REPLACE_ID_HERE`）
- 可切換分類「套裝」「單件配件」「全部」
- 顯示每日租金、原價、內容物與尺寸
