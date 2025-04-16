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
import streamlit as st
from src.agents.planner import llm, llm_formater
from src.tools import tool_reader
from src.prompts.planner import prompt_structure
from src.prompts.reader import prompt_agent_reader

class NewsAnalized(TypedDict):
    titulo_da_noticia: Annotated[str,'Títlo da notícia']
    link: Annotated[str,'Link da notícia']
    justificativa_relevancia: Annotated[str,'Motivo pelo qual a notícia é relevante para a empresa e para a dimensão analisada']
    data: Annotated[str,'Data da notícia']
    resumo: Annotated[str,'Resumo detalhado da notícia']
    insights_estrategicos: Annotated[str,'Insights estratégicos sobre a empresa, com base na notícia']
    sentimento: Annotated[Literal['positivo','neutro','negativo'],'Análise de sentimento da notícia']
    peso_fonte: Annotated[Literal['grande_midia_nacional',
                                  'midia_especializada_ou_setorial',
                                  'sites_regionais_e_blogs_institucionais',
                                  'fontes_oficiais_da_empresa'], "Peso da fonte de notícia. Atribuímos um peso com base na influência e confiabilidade do veículo"]
    intensidade_impacto: Annotated[Literal['muito_alto','alto','moderado','baixo'],'Intensidade do Impacto (Gravidade / Positividade) Refere-se ao grau de relevância ou impacto reputacional da notícia']
    justificativa_avaliacao: Annotated[str,'justificativa da avaliação dada a notícia']
    comentarios: Annotated[str,'comentários adicionais']

class Avaliacao(TypedDict):
    noticias_avaliadas: Annotated[List[NewsAnalized], "Lista de notícias analizadas"]
    dimensao: Annotated[str,'Dimensão de análise da notícia']

class AgenteReader(MessagesState):
    final_response: Annotated[Avaliacao, 'resposta final estruturada']

@st.cache_resource()
def memory(id):
    memory_analizer = MemorySaver()
    return memory_analizer

model_reader = llm.bind_tools(tool_reader)
model_reader_structured = llm_formater.with_structured_output(Avaliacao)

memory_reader = MemorySaver()

# Define the function that calls the model
def call_model_reader(state: AgenteReader):
    chain = prompt_agent_reader | model_reader
    response = chain.invoke(input={"messages":state['messages']})
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function that determines whether to continue or not
def should_continue(state: AgenteReader):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we respond to the user
    if not last_message.tool_calls:
        return 'end'
    # Otherwise if there is, we continue
    else:
        return "continue"

def format_reader(state:AgenteReader):
    messages = state['messages']
    chain = prompt_structure | model_reader_structured
    response = chain.invoke({'messages':messages})
    return {"final_response": response}

# Define a new graph
subgraph_reader = StateGraph(AgenteReader)

# Define the two nodes we will cycle between
subgraph_reader.add_node("agent_reader", call_model_reader)
subgraph_reader.add_node("tools", ToolNode(tool_reader))
subgraph_reader.add_node("format_reader", format_reader)
# Set the entrypoint as `agent`
# This means that this node is the first one called
subgraph_reader.set_entry_point("agent_reader")

# We now add a conditional edge
subgraph_reader.add_conditional_edges(
    "agent_reader",
    should_continue,
    {
        "continue": "tools",
        'end': 'format_reader',
    },
)

subgraph_reader.add_edge("tools", "agent_reader")
subgraph_reader.add_edge('format_reader', END)
graph_reader = subgraph_reader.compile(checkpointer=memory_reader)