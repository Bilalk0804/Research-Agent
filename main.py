from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent,AgentExecutor
from langchain.chat_models import ChatHuggingFace
from langchain.llms import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel
from tools import search_tool,wiki_tool, save_tool
load_dotenv()
llm = init_chat_model("mistralai/mixtral-8x7b-instruct-v0.1", model_provider="Nvidia", api_key=os.getenv("NVIDIA_API_KEY"))

# prompt="Tell me how is an agent diffrent from a tool in the context of LLMs"
# response = llm.invoke(prompt)
# for chunk in llm.stream(prompt):
#    print(chunk.content, end='')


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
parcer = PydanticOutputParser(pydantic_object=ResearchResponse)
prompt = ChatPromptTemplate.from_messages(
    [
    ("system", 
     """
     You are an expert research assistant powered by AI. Your job is to gather concise, high-quality insights on a given topic using custom tools (e.g., search, Wikipedia, academic databases). For each topic, follow this structure:

    1. Provide a **concise summary** (150–300 words) explaining the topic clearly.
    2. List **credible sources** used, with links if available.
    3. Mention the **tools or methods** you used to find the information (e.g., Wikipedia wrapper, Google Search tool, academic search).
    4. Present all content in the following format (no extra commentary):

    {format_instructions}

    Avoid vague responses. If you cannot find information, state clearly which part failed and suggest next steps for research.
 
     """),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
    ]).partial(format_instructions=parcer.get_format_instructions())
tools=[search_tool,wiki_tool,save_tool]
agent= create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
query=input("How can I help you research? ")
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
raw_response = agent_executor.invoke({"query":query})
#print(raw_response)
#rint(raw_response['output'])
structured_response = parcer.parse(raw_response['output'])
print(structured_response)