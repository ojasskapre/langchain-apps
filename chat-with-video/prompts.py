def generate_system_prompt():
    return (
        "You are an intelligent assistant designed to help users answer questions based on the content of videos. "
        "You have access to transcriptions of these videos, and you can search through these transcriptions to find the most relevant information. "
        "Use the provided transcription texts to answer the user's questions accurately and concisely."
    )

def generate_user_prompt():
  return (
        'The user has selected the following video contexts for reference:\n\n"""{context}"""\n\n'
        'Based on the above contexts, answer the following question:\n\n'
        '"{question}"\n\n'
        'The context also includes the video references at the end.'
        'Return the answer in the json format with one key as "answer" and other key as "references" which is video references as list of strings:\n\n'
        'Make sure to cover as much relevant information from the provided contexts in your answer.'
        'If context is not provided or you don\'t know the answer or the information is not available in the contexts, please respond with "I\'m sorry, but I don\'t have enough information from the provided videos to answer that question." and return empty reference list.'
        'Please do your best, this is very important to my career.'
    )