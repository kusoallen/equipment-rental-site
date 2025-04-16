
import streamlit as st
import pandas as pd
import urllib.parse

# Streamlit 設定
st.set_page_config(page_title="裝備租借展示", layout="wide")
st.title("🛡️ 裝備租借展示系統")

# Google Sheet CSV 匯出連結
sheet_url = "https://docs.google.com/spreadsheets/d/1VbqOaRt3lWAEJjg-QdGABBT2XdC6B_2ZuIsqrASGmio/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

# 🖼 圖片名稱與 Drive ID 對應表（你需手動補上對應）
image_ids = {
    "黃巾軍套裝": "1uT3K7au8Tz8k-dkG6A5-NIcn4o9AqMZK",
    "希臘戰士套裝": "1w5sVBWUl9WrfCZs_k28nW7-j3lqS4XaZ",
    "維京棉甲戰士套裝": "1y1BPJoaAHOMqY5EMDBFV-qLS03NIlRxH",
    "維京披風棕": "1c5RRaRMIFgZgIG0O1gCuZru4ZIlMGaU2"
    # ... 請補齊剩下圖片名稱與ID
}

# 載入資料
df = load_data()

# 🔍 搜尋欄
keyword = st.text_input("🔍 搜尋裝備名稱或內容物關鍵字").strip()

if keyword:
    df = df[df["名稱"].str.contains(keyword, case=False, na=False) | df["內容物"].str.contains(keyword, case=False, na=False)]

# 🔘 分類選單
categories = ["全部"] + sorted(df["分類"].dropna().unique().tolist())
selected = st.radio("📂 類別篩選：", categories, horizontal=True)

# 篩選資料
if selected != "全部":
    df = df[df["分類"] == selected]

# 🧱 顯示裝備卡片
cols = st.columns(3)
for i, (_, row) in enumerate(df.iterrows()):
    with cols[i % 3]:
        image_url = f"https://drive.google.com/uc?id={image_ids.get(row['名稱'], '')}"
        st.image(image_url, use_column_width=True, caption=row["名稱"])
        st.markdown(f"#### {row['名稱']}")
        st.markdown(f"📦 分類：{row['分類']}")
        st.markdown(f"💰 每日租金：${int(row['每日租金']) if pd.notna(row['每日租金']) else '—'}")
        st.markdown(f"💥 損壞賠償價：${int(row['原價']) if pd.notna(row['原價']) else '—'}")
        st.markdown(f"📏 尺寸：{row['尺寸'] if pd.notna(row['尺寸']) else '—'}")
        st.markdown(f"🔹 內容物：{row['內容物']}")

# 📝 表單區塊（模擬）
st.markdown("---")
st.subheader("📝 我要預約租借")

with st.form("rental_form"):
    name = st.text_input("👤 你的名字")
    item = st.selectbox("📦 想租借的裝備", df["名稱"].unique())
    days = st.number_input("📆 租借天數", min_value=1, value=1)
    submit = st.form_submit_button("送出預約")

    if submit:
        st.success(f"感謝你，{name}！你已預約【{item}】，租借 {days} 天。後續會與你聯繫！")

