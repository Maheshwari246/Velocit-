
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
import tempfile
from yolov8_core import process_video
import base64

st.set_page_config(layout="wide")
st.title("🚘 VelocIT: License Plate Detection")

uploaded_file = st.file_uploader(
    "📤 Upload a traffic video",
    type=["mp4", "avi", "mov"]
)

if uploaded_file is not None:
    video_bytes = uploaded_file.read()
    encoded_video = base64.b64encode(video_bytes).decode("utf-8")

    st.markdown("### 🎞️ Uploaded Video")
    st.markdown(
        f"""
        <div style='max-width: 500px;'>
            <video controls style='width:100%; height:auto;'>
                <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
            </video>
        </div>
        """,
        unsafe_allow_html=True
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_bytes)
        temp_video_path = tmp.name

    if st.button("▶️ Run Detection"):
        with st.spinner("Processing... Please wait."):

            output_path = process_video(temp_video_path)

        st.success("✅ Detection Completed!")

        if output_path and os.path.exists(output_path):
            with open(output_path, "rb") as file:
                out_bytes = file.read()

            encoded_output = base64.b64encode(out_bytes).decode("utf-8")

            st.markdown("### 📽️ Output Video")
            st.markdown(
                f"""
                <div style='max-width: 500px;'>
                    <video controls style='width:100%; height:auto;'>
                        <source src="data:video/mp4;base64,{encoded_output}" type="video/mp4">
                    </video>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("❌ Couldn't load output video.")
