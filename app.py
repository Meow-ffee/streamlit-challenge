import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import webcolors

# --- 色名取得ヘルパー関数 ---
def closest_color_name(rgb):
    try:
        # 近い CSS3 色名を取得
        name = webcolors.rgb_to_name(rgb, spec="css3")
    except ValueError:
        # 近似色名を探す
        min_distances = {}
        for hex_val, name_val in webcolors.CSS3_HEX_TO_NAMES.items():
            r2, g2, b2 = webcolors.hex_to_rgb(hex_val)
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, (r2, g2, b2)))
            min_distances[distance] = name_val
        name = min_distances[min(min_distances.keys())]
    return name

# --- 色解析関数 ---
def get_dominant_colors(img, n_colors=3):
    img = img.resize((200, 200))  # 処理軽量化
    arr = np.array(img)
    arr = arr.reshape((-1, 3))

    kmeans = KMeans(n_clusters=n_colors, random_state=0)
    kmeans.fit(arr)
    centers = np.array(kmeans.cluster_centers_, dtype=int)
    return centers.tolist()

# --- Streamlit UI ---
st.title("📸 カメラ・アップロードでカラー判定（Streamlit版）")
st.write("画像から代表色を抽出して色名・HEX・RGB を表示します。")

# --- 画像入力（カメラ OR アップロード） ---
input_type = st.radio("入力方法を選んでください", ("カメラで撮影", "ファイルを選択"))

img = None
if input_type == "カメラで撮影":
    img_file = st.camera_input("カメラで撮影")
    if img_file:
        img = Image.open(img_file)
elif input_type == "ファイルを選択":
    img_file = st.file_uploader("画像をアップロード", type=["jpg", "png", "jpeg"])
    if img_file:
        img = Image.open(img_file)

# --- 判定と表示 ---
if img is not None:
    st.image(img, caption="判定対象画像", use_column_width=True)

    # 代表色取得
    colors = get_dominant_colors(img, n_colors=3)

    st.write("### 🎨 代表色")

    for rgb in colors:
        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
        name = closest_color_name(tuple(rgb))

        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<div style='background:{hex_code}; width:50px; height:50px;'></div>", unsafe_allow_html=True)
        with col2:
            st.write(f"HEX: {hex_code}  |  RGB: {rgb}  |  Color Name: **{name}**")
