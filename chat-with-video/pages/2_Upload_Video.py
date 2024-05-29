from process_video import process_uploaded_video
import streamlit as st

uploaded_video = st.file_uploader("Upload a video", type=["mp4"])
# If a video is uploaded, start processing
if uploaded_video:
    with st.spinner('Processing video...'):
        # Process the uploaded video (implement this function in chat_utils)
        process_uploaded_video(uploaded_video)