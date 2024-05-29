import streamlit as st

st.set_page_config(layout="wide")
st.title("Welcome to the Video Chat Application")

st.markdown("""
### Overview

This application allows you to interact with video content in two main ways:

1. **Chat With Video**: Select videos and ask questions to get insights based on the video content.
2. **Upload Video**: Upload your own videos to process and transcribe them, making them available for chat.

### Navigation

Use the sidebar to navigate between different pages:

- **Home**: You're currently here. This page provides an overview of the application.
- **Chat With Video**: Go to this page to select videos and ask questions about their content.
- **Upload Video**: Go to this page to upload new videos and process them.

### How to Use

1. Navigate to **Upload Video** to upload your video content.
2. Once the video is processed, navigate to **Chat With Video** to ask questions based on the video's content.

### Additional Resources

- [GitHub Repository](https://github.com/ojasskapre/langchain-apps/tree/main/chat-with-video) - Check out the source code on GitHub.
""")

st.image("process-video.png", caption="Video Processing Overview")
st.image("video-qa.png", caption="QA Process Overview")

st.markdown("""I hope you enjoy using this application!""")