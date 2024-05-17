from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

from prompts import generate_webpage_summary_template, generate_search_queries_prompt, generate_research_report_prompt
from utils import scrape_text, flatten_list_of_list, web_search, download_as_pdf

import json

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

WRITER_SYSTEM_PROMPT = "You are an AI critical thinker research assistant. Your sole purpose is to write well written, criticallycritically acclaimed, objective and structured reports on given text."

RESEARCH_REPORT_PROMPT = generate_research_report_prompt()

prompt = ChatPromptTemplate.from_messages(
  [
    ("system", WRITER_SYSTEM_PROMPT),
    ("user", RESEARCH_REPORT_PROMPT)
  ]
)

chain = RunnablePassthrough.assign(
  context = full_research_chain | flatten_list_of_list) | prompt | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser()

results = chain.invoke(
  {
    "question": "How to implement FAIR CyberSecurity Risk framework for an Online Banking System?",
  }
)

download_as_pdf(results)