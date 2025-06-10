from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent,AgentExecutor
from pydantic import BaseModel

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
     You are a helpful research assistant that will help in generating a research paper.
     You will provide a summary of the topic, list sources, and mention tools used in the research.
     Wrap the output in this format and provide no other text\n{format_instructions} 
     """),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
    ]).partial(format_instructions=parcer.get_format_instructions())

agent= create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[]
)
agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)
raw_response = agent_executor.invoke({"query": "Chilli plant leaves?"})
print(raw_response)