from pydantic import BaseModel, Field
from typing import Literal, List
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from typing_extensions import Annotated, TypedDict
from langchain_core.output_parsers import PydanticToolsParser
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
import dotenv
import os
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from src.agents.planner import llm, llm_formater
from src.tools import tools_researcher
from src.prompts.planner import prompt_structure
from src.prompts.reseacher import prompt_agent_researcher 


model_researcher = llm.bind_tools(tools_researcher)

class News(TypedDict):
    titulo_da_noticia: Annotated[str,'Títlo da notícia']
    link: Annotated[str,'Link da notícia']
    resumo: Annotated[str, 'Resumo e descrição da notícia']
    justificativa_relevancia: Annotated[str,'Motivo pelo qual a notícia é relevante para a empresa e para a dimensão analisada']
    data: Annotated[str,'Data da notícia']

class DimensaoNews(TypedDict):
    dimensao: Annotated[str,'Dimensão que está sendo feita a pesquisa']
    news: Annotated[List[News], 'Lista de notícias relevantes para a dimensão e para a empresa']

class ListDimensaoNews(TypedDict):
    list_dimensao_news: Annotated[List[DimensaoNews],"Lista de dimensão com notícias relevantes para a empresa"]

model_researcher_formater = llm_formater.with_structured_output(ListDimensaoNews)

class AgenteResearcher(MessagesState):
    final_response: Annotated[dict, 'resposta final estruturada']


memory_researcher = MemorySaver()

# Define the function that calls the model
def call_model_researcher(state: AgenteResearcher):
    chain = prompt_agent_researcher | model_researcher
    response = chain.invoke(input={"messages":state['messages']})
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function that determines whether to continue or not
def should_continue(state: AgenteResearcher):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we respond to the user
    if not last_message.tool_calls:
        return 'end'
    # Otherwise if there is, we continue
    else:
        return "continue"
    
def format_research(state:AgenteResearcher):
    messages = state['messages']
    chain = prompt_structure | model_researcher_formater
    response = chain.invoke({'messages':messages})
    return {'final_response':response}


# Define a new graph
workflow_reseacher = StateGraph(AgenteResearcher)

# Define the two nodes we will cycle between
workflow_reseacher.add_node("agent_researcher", call_model_researcher)
workflow_reseacher.add_node("tools", ToolNode(tools_researcher))
workflow_reseacher.add_node("format_research",format_research)
# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow_reseacher.set_entry_point("agent_researcher")

# We now add a conditional edge
workflow_reseacher.add_conditional_edges(
    "agent_researcher",
    should_continue,
    {
        "continue": "tools",
        'end': "format_research",
    },
)

workflow_reseacher.add_edge("tools", "agent_researcher")
workflow_reseacher.add_edge("format_research", END)

graph_reseacher = workflow_reseacher.compile(checkpointer=memory_researcher)