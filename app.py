
import streamlit as st
import pandas as pd
import os
from PIL import Image, ExifTags

st.set_page_config(page_title="裝備租借展示", layout="wide")
st.title("🛡️ 裝備租借展示系統")

sheet_url = "https://docs.google.com/spreadsheets/d/1VbqOaRt3lWAEJjg-QdGABBT2XdC6B_2ZuIsqrASGmio/export?format=csv&gid=0"

@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

def open_oriented_image(path):
    try:
        image = Image.open(path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except:
        image = Image.open(path)
    return image

df = load_data()
df = df[df["名稱"].notna()]# ✅ 過濾掉空白名稱的資料列

keyword = st.text_input("🔍 搜尋裝備名稱或內容物關鍵字").strip()
if keyword:
    df = df[df["名稱"].str.contains(keyword, case=False, na=False) | df["內容物"].str.contains(keyword, case=False, na=False)]

categories = ["全部"] + sorted(df["分類"].dropna().unique().tolist())
selected = st.radio("📂 類別篩選：", categories, horizontal=True)
if selected != "全部":
    df = df[df["分類"] == selected]

cols = st.columns(3)
for i, (_, row) in enumerate(df.iterrows()):
    with cols[i % 3]:
        image_path = None
        for ext in [".jpg", ".JPG", ".png"]:
            path = f"image/{row['名稱']}{ext}"
            if os.path.exists(path):
                image_path = path
                break

        if image_path:
            img = open_oriented_image(image_path)
            st.image(img, use_container_width=True)
        else:
            st.warning(f"❗ 找不到圖片：{row['名稱']}.jpg/.JPG/.png")

        st.markdown(f"#### {row['名稱']}")
        st.markdown(f"📦 分類：{row['分類']}")
        st.markdown(f"💰 每日租金：${int(row['每日租金']) if pd.notna(row['每日租金']) else '—'}")
        st.markdown(f"💥 損壞賠償價：${int(row['原價']) if pd.notna(row['原價']) else '—'}")
        尺寸 = row['尺寸'] if '尺寸' in row and pd.notna(row['尺寸']) else "—"
        st.markdown(f"📏 尺寸：{尺寸}")
        st.markdown(f"🔹 內容物：{row['內容物']}")
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📝 我要預約租借")

with st.form("rental_form"):
    name = st.text_input("👤 你的名字")
    item = st.selectbox("📦 想租借的裝備", df["名稱"].unique())
    days = st.number_input("📆 租借天數", min_value=1, value=1)
    submit = st.form_submit_button("送出預約")

    if submit:
        st.success(f"感謝你，{name}！你已預約【{item}】，租借 {days} 天。後續會與你聯繫！")
