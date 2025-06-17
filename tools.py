from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
"""To create custom tools, you can use the tool decorator from langchain.tools"""
from langchain.tools import Tool
from datetime import datetime
'''-------------------------------------------'''
def save_to_file_func(input_str: str) -> str:
    try:
        filename, content = input_str.split("::", 1)
        filename = filename.strip()
        content = content.strip()
        if not filename:
            return "Error: Filename is empty. Provide input like 'filename.txt::Your content here'."
    except ValueError:
        return "Error: Input must be in format '<filename>::<content>'."

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: Content saved to '{filename}'"
    except Exception as e:
        return f"Error: Could not save to file '{filename}': {e}"
'''-------------------------------------------'''
# Instantiate as a Tool
save_to_file_tool = Tool(
    name="save_to_file",
    func=save_to_file_func,
    description="Save content to a file. Input '<filename>::<content>'"
)
'''---------------------------------------'''
def save_to_txt(data: str, filename: str = "research_output.txt"):  
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"  
    with open(filename, "a", encoding="utf-8") as f:  
        f.write(formatted_text)  
    return f"Data successfully saved to {filename}"  
save_tool = Tool(  
name="seal",  
func=save_to_txt,  
description="Search the web for information")  
'''---------------------------------------'''




search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="DuckDuckGoSearch",
    func=search.run,
    description="Search the web for information",
    return_direct=True
)
api_wrapper = WikipediaAPIWrapper(wiki_client=any, top_k_results = 2, doc_content_chars_max=2000,lang="en")
wiki_tool= WikipediaQueryRun(api_wrapper=api_wrapper)
