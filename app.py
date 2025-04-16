
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 設定 Streamlit 頁面資訊
st.set_page_config(page_title="裝備租借展示", layout="wide")
st.title("🛡️ 裝備租借展示系統")

# Google Sheet CSV 匯出連結（記得設為公開）
sheet_url = "https://docs.google.com/spreadsheets/d/1VbqOaRt3lWAEJjg-QdGABBT2XdC6B_2ZuIsqrASGmio/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

@st.cache_data
def get_drive_image_ids(folder_url):
    """解析 Google Drive 資料夾，取得檔案名稱與 ID 的對應表"""
    file_ids = {}
    html = requests.get(folder_url).text
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all("script"):
        if "window.viewerData" in script.text:
            data_start = script.string.find('{')
            data_text = script.string[data_start:]
            try:
                import json
                viewer_data = json.loads(data_text.split("};")[0] + "}")
                for item in viewer_data["docs"]:
                    title = item.get("title")
                    file_id = item.get("id")
                    if title and file_id:
                        name = title.rsplit(".", 1)[0]  # 去掉副檔名
                        file_ids[name] = file_id
            except Exception as e:
                print("JSON parsing error:", e)
            break
    return file_ids

# 載入資料與圖片 ID 對應
df = load_data()
image_ids = get_drive_image_ids("https://drive.google.com/drive/folders/12z1OG5vykinDStN_H8wGD5izxYBw40mW")

# 搜尋欄
keyword = st.text_input("🔍 搜尋裝備名稱或內容物關鍵字").strip()
if keyword:
    df = df[df["名稱"].str.contains(keyword, case=False, na=False) | df["內容物"].str.contains(keyword, case=False, na=False)]

# 類別篩選
categories = ["全部"] + sorted(df["分類"].dropna().unique().tolist())
selected = st.radio("📂 類別篩選：", categories, horizontal=True)
if selected != "全部":
    df = df[df["分類"] == selected]

# 顯示裝備卡片
cols = st.columns(3)
for i, (_, row) in enumerate(df.iterrows()):
    with cols[i % 3]:
        image_id = image_ids.get(row["名稱"], "")
        image_url = f"https://drive.google.com/uc?id={image_id}" if image_id else ""
        
if image_url:
    st.image(image_url, use_container_width=True, caption=row["名稱"])
else:
    st.warning(f"❗ 無圖片：{row['名稱']}")

st.markdown(f"#### {row['名稱']}")
st.markdown(f"📦 分類：{row['分類']}")
st.markdown(f"💰 每日租金：${int(row['每日租金']) if pd.notna(row['每日租金']) else '—'}")
st.markdown(f"💥 損壞賠償價：${int(row['原價']) if pd.notna(row['原價']) else '—'}")
尺寸 = row["尺寸"] if "尺寸" in row and pd.notna(row["尺寸"]) else "—"
st.markdown(f"📏 尺寸：{尺寸}")
st.markdown(f"🔹 內容物：{row['內容物']}")

        st.markdown(f"#### {row['名稱']}")
        st.markdown(f"📦 分類：{row['分類']}")
        st.markdown(f"💰 每日租金：${int(row['每日租金']) if pd.notna(row['每日租金']) else '—'}")
        st.markdown(f"💥 損壞賠償價：${int(row['原價']) if pd.notna(row['原價']) else '—'}")
        尺寸 = row["尺寸"] if "尺寸" in row and pd.notna(row["尺寸"]) else "—"
        st.markdown(f"📏 尺寸：{尺寸}")
        st.markdown(f"🔹 內容物：{row['內容物']}")

# 表單模組
st.markdown("---")
st.subheader("📝 我要預約租借")

with st.form("rental_form"):
    name = st.text_input("👤 你的名字")
    item = st.selectbox("📦 想租借的裝備", df["名稱"].unique())
    days = st.number_input("📆 租借天數", min_value=1, value=1)
    submit = st.form_submit_button("送出預約")

    if submit:
        st.success(f"感謝你，{name}！你已預約【{item}】，租借 {days} 天。後續會與你聯繫！")
