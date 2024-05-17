from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from bs4 import BeautifulSoup

import requests
import markdown
from weasyprint import HTML

RESULTS_PER_QUESTION = 3
ddg_search = DuckDuckGoSearchAPIWrapper()

def scrape_text(url):
  try:
    response = requests.get(url)
    
    if response.status_code == 200:
      # Parse the content of the page using BeautifulSoup
      soup = BeautifulSoup(response.text, 'html.parser')
        
      # Extract all text from the webpage
      text = soup.get_text(separator=' ', strip=True)

      return text
    else:
      return f"Failed to scrape the webpage. Status code: {response.status_code}"
  except Exception as e:
    print(f"An error occurred: {e}")
    return f"Failed to scrape the webpage. Error: {e}"

def flatten_list_of_list(list_of_list):
  content = []
  for sublist in list_of_list:
    content.append("\n\n".join(sublist))
  return "\n\n".join(content)

def web_search(query: str, num_results: int = RESULTS_PER_QUESTION):
  results = ddg_search.results(query, num_results)
  return [r["link"] for r in results]

def download_as_pdf(results):
  content = markdown.markdown(results)
  HTML(string=content).write_pdf("report.pdf")