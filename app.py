import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
import tempfile
from yolov8_core import process_video

st.set_page_config(page_title="VelocIT", layout="wide")

st.title("🚗 VelocIT: Vehicle Detection System")

uploaded_file = st.file_uploader("📤 Upload Video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(uploaded_file.read())
    temp_file.close()

    with st.spinner("Processing video..."):
        output_path = process_video(temp_file.name)

    st.success("Done!")

    st.video(output_path)

    with open(output_path, "rb") as f:
        st.download_button("Download Video", f, file_name="output.mp4")
