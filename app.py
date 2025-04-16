
import streamlit as st
import pandas as pd
#123
# Google Sheet CSV 連結（需設為公開）
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSbq8dzRa9Q58u-KZfdgtqpWyH8MnYzsnOBQvJ3T0NDd1rDqj3tpU0L4v3_bj_C_DmMMImY_Mr4XrHv/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

df = load_data()

st.set_page_config(page_title="裝備租借展示", layout="wide")
st.title("🎭 裝備租借展示頁")

# 分類按鈕
categories = ["全部"] + sorted(df["分類"].dropna().unique().tolist())
selected = st.radio("請選擇要查看的分類：", categories, horizontal=True)

# 篩選資料
if selected != "全部":
    filtered = df[df["分類"] == selected]
else:
    filtered = df

# 每行最多顯示 3 張卡片
cols = st.columns(3)

for i, (_, row) in enumerate(filtered.iterrows()):
    with cols[i % 3]:
        st.image(f"https://drive.google.com/uc?id=REPLACE_ID_HERE", width=250, caption=row["名稱"])
        st.markdown(f"### {row['名稱']}")
        st.markdown(f"📦 **分類**：{row['分類']}")
        st.markdown(f"💰 **每日租金**：${int(row['每日租金']) if pd.notna(row['每日租金']) else '—'}")
        st.markdown(f"💥 **損壞賠償價**：${int(row['原價']) if pd.notna(row['原價']) else '—'}")
        st.markdown(f"📏 **尺寸**：{row['尺寸'] if pd.notna(row['尺寸']) else '—'}")
        st.markdown(f"🔹 **內容物**：{row['內容物']}")
