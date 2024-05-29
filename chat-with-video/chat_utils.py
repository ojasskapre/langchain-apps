from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from prompts import generate_system_prompt, generate_user_prompt

import os

load_dotenv()


def split_transcription(transcription):
  """Split the transcription into multiple components."""
  splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
  return splitter.split_text(transcription)

def get_vectorstore():
  """Return a Pinecone vector store object."""
  embeddings = OpenAIEmbeddings()
  vectorstore = PineconeVectorStore(index_name=os.getenv("PINECONE_INDEX_NAME"), embedding=embeddings)
  return vectorstore

def add_text_to_pinecone(text, vectorstore, video_filename):
  print(f"Adding text to Pinecone vector store")
  vectorstore.add_texts(texts=[text], metadatas=[{'video_filename': video_filename}])


def format_docs(docs):
  """Format the documents for the RAG model."""
  if not docs:
    return "I'm sorry, but I don't have enough information from the provided videos to answer that question."

  # Extract unique video filenames from the metadata
  video_filenames = {doc.metadata['video_filename'] for doc in docs}

  # Join the page content of all documents
  formatted_text = "\n\n".join(doc.page_content for doc in docs)
  
  # Format the video filenames as references
  references = "\n\nReferences:\n" + "\n".join(video_filenames)
  
  return formatted_text + references


def get_rag_chain(selected_videos):
  """Create a RAG chain for answering questions based on video content."""
  llm = ChatOpenAI(model="gpt-3.5-turbo-1106")
  vectorstore = get_vectorstore()
  retriever = vectorstore.as_retriever(search_kwargs={"filter": {"video_filename": {"$in": selected_videos}}})

  SYSTEM_PROMPT = generate_system_prompt()
  USER_PROMPT = generate_user_prompt()

  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", SYSTEM_PROMPT),
      ("user", USER_PROMPT)
    ]
  )

  rag_chain = (
      {"context": retriever | format_docs, "question": RunnablePassthrough()}
      | prompt
      | llm
      | JsonOutputParser()
  )
  return rag_chain


def get_query_response(prompt, selected_videos):
  rag_chain = get_rag_chain(selected_videos)
  answer = rag_chain.invoke(prompt)
  return answer
