from dotenv import load_dotenv
from chat_utils import split_transcription, get_vectorstore, add_text_to_pinecone
from video_utils import extract_audio, transcribe_audio, get_file_size

import os
import tempfile
import uuid

load_dotenv()


def process_uploaded_video(uploaded_video):
    # Create a temporary file for the video
    temp_dir = tempfile.gettempdir()
    video_path = os.path.join(temp_dir, uploaded_video.name)
    
    with open(video_path, "wb") as temp_video_file:
        temp_video_file.write(uploaded_video.getbuffer())

    # Process the video file
    process(video_path)

    # Cleanup: Remove the temporary video file
    os.remove(video_path)


def process(video_path):
    # Create a temporary file for the audio
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio_file:
        audio_path = temp_audio_file.name
    
    try:
        transcription = ""
        # if transcription.txt exists (used only in development), then read it else transcribe the video
        if os.path.exists('transcription.txt'):
            with open('transcription.txt', 'r') as f:
                transcription = f.read()
            print(f"Transcription loaded from file")
        else:
            # Extract audio from video
            extract_audio(video_path, audio_path)

            # Get and print the size of the temporary audio file
            file_size = get_file_size(audio_path)
            print(f"Temporary audio file size: {file_size / (1024 * 1024):.2f} MB")
            
            # Transcribe audio to text
            transcription = transcribe_audio(audio_path)
            print(f"Transcription completed")

            # save the transcription to a file
            # with open('transcription.txt', 'w') as f:
            #     f.write(transcription)

        # Split the transcription into multiple components
        components = split_transcription(transcription)
        print(f"Transcription split into {len(components)} components")

        # Initialize a Pinecone vector store
        vectorstore = get_vectorstore()

        # Add each component to the Pinecone vector store
        filename = os.path.basename(video_path)
        for component in components:
            add_text_to_pinecone(component, vectorstore, video_filename=filename)
        
        # save filename to a file
        with open('files_uploaded.txt', 'a') as f:
            f.write("\n"+filename)

    finally:
        # Cleanup: Remove the temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    # give two options, ask for video path or exit
    print("Video processing script!")
    print("1. Enter video path")
    print("2. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        video_path = input("Enter the video path: ")
        process(video_path)
    elif choice == '2':
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")