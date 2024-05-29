from chat_utils import get_vectorstore, get_query_response

import os
import streamlit as st

st.set_page_config(layout="wide")
st.title("Chat with Video")

# get list of videos from text file files_uploaded.txt
available_videos = []
if os.path.exists('files_uploaded.txt'):
    with open('files_uploaded.txt', 'r') as f:
        available_videos = f.read().splitlines()

# Multiselect for video selection
selected_videos = st.multiselect('Select videos to ask questions about:', available_videos)

# Check if the selection changed
if "previous_selection" not in st.session_state:
    st.session_state.previous_selection = selected_videos

if st.session_state.previous_selection != selected_videos:
    st.session_state.messages = []
    st.session_state.previous_selection = selected_videos

if available_videos:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Get assistant response
            videos = selected_videos if selected_videos != [] else available_videos

            res = get_query_response(prompt, videos)
            answer = res.get("answer", "Error in response. Please try again.")
            references = res.get("references", [])
            
            # Format the answer with references as a tooltip
            if references:
                references_str = ", ".join(references)
                formatted_answer = f"{answer} \n\n<sup>References: {references_str}</sup>"
            else:
                formatted_answer = answer
            
            # Display the formatted answer
            st.markdown(formatted_answer, unsafe_allow_html=True)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": formatted_answer})
else:
    st.info("No videos uploaded yet. Please upload a video to start chatting.")