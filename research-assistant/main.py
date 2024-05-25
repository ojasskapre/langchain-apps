from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

from prompts import generate_webpage_summary_template, generate_search_queries_prompt, generate_research_report_prompt
from utils import scrape_text, flatten_list_of_list, web_search, download_as_pdf

import json
import streamlit as st

load_dotenv()


SUMMARY_TEMPLATE = generate_webpage_summary_template()
SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)

scrape_and_summarize_chain = RunnablePassthrough.assign(summary=RunnablePassthrough.assign(
  text=lambda x: scrape_text(x["url"])[:10000]
) | SUMMARY_PROMPT | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser()) | (lambda x: f"URL: {x['url']}\n\nSummary: {x['summary']}")

web_search_chain = RunnablePassthrough.assign(
  urls=lambda x: web_search(x["question"])
) | (lambda x: [{"question": x["question"], "url": url} for url in x["urls"]]) | scrape_and_summarize_chain.map()


SEARCH_PROMPT = ChatPromptTemplate.from_messages(
  [
    (
      "user", generate_search_queries_prompt()
    )
  ]
)

search_question_chain = SEARCH_PROMPT | ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0) | StrOutputParser() | json.loads

full_research_chain = search_question_chain | (lambda x: [{"question": q} for q in x]) | web_search_chain.map()

WRITER_SYSTEM_PROMPT = "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."

RESEARCH_REPORT_PROMPT = generate_research_report_prompt()

prompt = ChatPromptTemplate.from_messages(
  [
    ("system", WRITER_SYSTEM_PROMPT),
    ("user", RESEARCH_REPORT_PROMPT)
  ]
)

chain = RunnablePassthrough.assign(
  context = full_research_chain | flatten_list_of_list) | prompt | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser()

# results = chain.invoke(
#   {
#     "question": "How to implement FAIR CyberSecurity Risk framework for an Online Banking System?",
#   }
# )

# download_as_pdf(results)

# Initialize session state variables
if "generating" not in st.session_state:
    st.session_state.generating = False
if "results" not in st.session_state:
    st.session_state.results = None

# Streamlit UI
st.title("Research Assistant")
st.write("Enter a topic to generate a research report:")

topic = st.text_input("Topic")

# Disable the button if the report is generating
button_clicked = st.button("Generate Report", disabled=st.session_state.generating)

if button_clicked:
    st.session_state.generating = True

if st.session_state.generating:
    with st.spinner("Generating report..."):
        results = chain.invoke({"question": topic})
        st.session_state.results = results
        st.session_state.generating = False
        st.success("Report generated successfully!")

# Display the results if available
if st.session_state.results:
    st.write(st.session_state.results)
    pdf_data = download_as_pdf(st.session_state.results)
    if pdf_data:
        st.download_button(
            label="Download Report as PDF",
            data=pdf_data,
            file_name="research_report.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Failed to generate PDF.")