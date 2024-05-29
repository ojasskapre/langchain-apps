from openai import OpenAI
import ffmpeg
import os
import tempfile

def extract_audio(video_path, audio_path):
    """Extract audio from video and save it as a temporary file."""
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format='mp3', acodec='mp3')
            .run(overwrite_output=True, quiet=True)
        )
        print(f"Audio extracted to {audio_path}")
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e}")
        raise

def get_file_size(file_path):
    """Get the size of a file in bytes."""
    return os.path.getsize(file_path)

def split_audio(audio_path, chunk_dir, chunk_size=25*1024*1024):
    """Split audio file into chunks less than 25MB."""
    print("Splitting audio into chunks...")
    os.makedirs(chunk_dir, exist_ok=True)
    chunks = []
    try:
        input_audio = ffmpeg.input(audio_path)
        duration = float(ffmpeg.probe(audio_path)['format']['duration'])
        num_chunks = int(duration // (chunk_size / get_file_size(audio_path) * duration))
        print("Number of Chunks: ", num_chunks)
        for i in range(num_chunks + 1):
            chunk_path = os.path.join(chunk_dir, f"chunk_{i}.mp3")
            start_time = i * duration / (num_chunks + 1)
            ffmpeg.output(input_audio, chunk_path, ss=start_time, t=duration / (num_chunks + 1)).run(overwrite_output=True, quiet=True)
            chunks.append(chunk_path)
    except ffmpeg.Error as e:
        print(f"Error splitting audio: {e}")
        raise
    return chunks

def transcribe_audio_chunk(audio_path):
    """Transcribe audio to text using OpenAI Whisper API."""
    print("Transcribing audio chunk...")
    client = OpenAI()
    try:
        with open(audio_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
        return response.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        raise

def transcribe_audio(audio_path):
    """Transcribe audio to text using OpenAI Whisper API, handling size limits."""
    print("Transcribing audio...")
    chunk_dir = tempfile.mkdtemp()
    try:
        chunks = split_audio(audio_path, chunk_dir)
        transcription = ""
        for chunk in chunks:
            transcription += transcribe_audio_chunk(chunk) + " "
        return transcription
    finally:
        # Cleanup: Remove the temporary chunk directory and files
        for chunk in chunks:
            os.remove(chunk)
        os.rmdir(chunk_dir)