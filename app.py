import streamlit as st
from PIL import Image
import numpy as np
import webcolors

# ----------------------------------------
# 色名を取得する関数
# ----------------------------------------
def closest_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb, spec="css3")
    except ValueError:
        min_dist = float("inf")
        closest_name = "Unknown"
        for hex_val, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r2, g2, b2 = webcolors.hex_to_rgb(hex_val)
            dist = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, (r2, g2, b2)))
            if dist < min_dist:
                min_dist = dist
                closest_name = name
        return closest_name

# ----------------------------------------
# 代表色抽出
# ----------------------------------------
def get_dominant_colors(img, n_colors=3):
    img = img.resize((200, 200))
    arr = np.array(img).reshape((-1, 3))

    kmeans = KMeans(n_clusters=n_colors, random_state=0)
    kmeans.fit(arr)

    centers = np.array(kmeans.cluster_centers_, dtype=int)
    return centers.tolist()

# ----------------------------------------
# UI
# ----------------------------------------
st.markdown(
    "<h1 style='white-space: nowrap;'>📸 カメラ・アップロードでカラー判定</h1>",
    unsafe_allow_html=True
)
st.write("画像から代表色を抽出して **色名 / HEX / RGB** を表示します。")

input_type = st.radio(
    "入力方法を選んでください",
    ("カメラで撮影", "ファイルを選択")
)

img = None

# ----------------------------------------
# カメラ入力（安全設計）
# ----------------------------------------
if input_type == "カメラで撮影":
    st.subheader("📷 カメラ入力")
    use_camera = st.checkbox("カメラを起動する")
    if use_camera:
        img_file = st.camera_input("撮影")
        if img_file:
            img = Image.open(img_file)
    else:
        st.info("💡 チェックを入れるとカメラが起動します")

# ----------------------------------------
# ファイルアップロード
# ----------------------------------------
else:
    img_file = st.file_uploader(
        "画像をアップロード",
        type=["jpg", "jpeg", "png"]
    )
    if img_file:
        img = Image.open(img_file)

# ----------------------------------------
# 判定結果表示
# ----------------------------------------
if img is not None:
    st.image(img, caption="判定対象画像", use_column_width=True)

    colors = get_dominant_colors(img, n_colors=3)

    st.subheader("🎨 代表色")

    for rgb in colors:
        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
        name = closest_color_name(tuple(rgb))

        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(
                f"<div style='background:{hex_code}; width:50px; height:50px; border-radius:6px;'></div>",
                unsafe_allow_html=True
            )
        with col2:
            st.write(f"**{name}**  |  HEX: {hex_code}  |  RGB: {rgb}")
