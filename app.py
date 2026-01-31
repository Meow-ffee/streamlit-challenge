import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import webcolors


# -----------------------------
# 色名を取得する関数
# -----------------------------
def closest_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb, spec="css3")
    except ValueError:
        min_distance = float("inf")
        closest_name = None

        for hex_value, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r2, g2, b2 = webcolors.hex_to_rgb(hex_value)
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, (r2, g2, b2)))

            if distance < min_distance:
                min_distance = distance
                closest_name = name

        return closest_name


# -----------------------------
# 代表色を取得する関数
# -----------------------------
def get_dominant_colors(img, n_colors=3):
    img = img.convert("RGB")
    img = img.resize((200, 200))  # 処理軽量化

    pixels = np.array(img).reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=0, n_init="auto")
    kmeans.fit(pixels)

    centers = kmeans.cluster_centers_.astype(int)
    return centers.tolist()


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="カラー判定", layout="centered")

st.title("📸 カメラ・アップロードでカラー判定")
st.write("撮影または画像アップロードから、代表的な色を判定します。")


# 入力方法選択
input_type = st.radio(
    "入力方法を選んでください",
    ("カメラで撮影", "ファイルを選択")
)

img = None

# カメラ入力（スマホ・PC対応）
if input_type == "カメラで撮影":
    img_file = st.camera_input("撮影")
    if img_file is not None:
        img = Image.open(img_file)

# ファイルアップロード
else:
    img_file = st.file_uploader(
        "画像をアップロード",
        type=["jpg", "jpeg", "png"]
    )
    if img_file is not None:
        img = Image.open(img_file)


# -----------------------------
# 判定結果表示
# -----------------------------
if img is not None:
    st.image(img, caption="判定対象画像", use_column_width=True)

    colors = get_dominant_colors(img, n_colors=3)

    st.subheader("🎨 代表色")

    for rgb in colors:
        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
        color_name = closest_color_name(tuple(rgb))

        col1, col2 = st.columns([1, 5])

        with col1:
            st.markdown(
                f"<div style='width:50px; height:50px; background:{hex_code}; border-radius:8px;'></div>",
                unsafe_allow_html=True
            )

        with col2:
            st.write(
                f"**{color_name}**  \n"
                f"HEX: `{hex_code}`  \n"
                f"RGB: {tuple(rgb)}"
            )
