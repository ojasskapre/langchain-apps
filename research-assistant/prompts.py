def generate_webpage_summary_template():
  return """{text}

  -------------------

  Using the above text, answer in short the following question:

  > {question}

  -------------------
  if the question cannot be answered using the text, simply summarize the text. Include all factual information, numbers, stats, etc.
"""

def generate_search_queries_prompt():
  return 'Write 3 google search queries to search online that form an objective opinion from the following task: "{question}"' \
          'Also include in the queries specified task details such as locations, names, etc.\n' \
          'You must respond with a list of search queries strictly in the following format: ["query 1", "query 2", "query 3"].'

def generate_research_report_prompt():
  return 'Information: """{context}"""\n\n' \
          'Using the above information, answer the following' \
          ' query or task: "{question}" in a detailed report --' \
           " The report should focus on the answer to the query, should be well structured, informative," \
          " in depth and comprehensive, with facts and numbers if available and a minimum of 1200 words.\n" \
          "You should strive to write the report as long as you can using all relevant and necessary information provided.\n" \
          "You must write the report with markdown syntax.\n " \
          "Use an unbiased and journalistic tone. \n" \
          "You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.\n" \
          "You MUST write all used source urls at the end of the report as references, and make sure to not add duplicated sources, but only one reference for each.\n" \
          "Every url should be hyperlinked: [url website](url)"\
          """
            Additionally, you MUST include hyperlinks to the relevant URLs wherever they are referenced in the report : 
        
            eg:    
                # Report Header
                
                This is a sample text. ([url website](url))
            """\
          "Cite search results using inline notations. Only cite the most \
          relevant results that answer the query accurately. Place these citations at the end \
          of the sentence or paragraph that reference them.\n"\
          "Please do your best, this is very important to my career."        