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
import uuid
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage,  SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
import streamlit as st

from src.agents.planner import llm
from src.agents.planner import graph_planner
from src.agents.reseacher import graph_reseacher
from src.agents.reader import graph_reader
from src.prompts.analyzer import prompt_agent_analizer

def calcular_nota_reputacao_normalizada(dimensao_dict):
    sentimento_map = {'positivo': 1, 'neutro': 0, 'negativo': -1}
    intensidade_map = {
        'muito_alto': 2.0,
        'alto': 1.5,
        'moderado': 1.0,
        'baixo': 0.5
    }
    peso_fonte_map = {
        'grande_midia_nacional': 1.0,
        'midia_especializada_ou_setorial': 0.9,
        'fontes_oficiais_da_empresa': 0.7,
        'sites_regionais_e_blogs_institucionais': 0.5
    }

    noticias = dimensao_dict.get('noticias_avaliadas', [])
    
    if not noticias:
        return 2.5  # Ausência de notícias = reputação neutra

    scores = []
    houve_negativa = False
    houve_positiva = False

    for noticia in noticias:
        sentimento = sentimento_map.get(noticia['sentimento'], 0)
        intensidade = intensidade_map.get(noticia['intensidade_impacto'], 1.0)
        peso_fonte = peso_fonte_map.get(noticia['peso_fonte'], 0.7)

        score = sentimento * intensidade * peso_fonte
        scores.append(score)

        if sentimento == -1:
            houve_negativa = True
        if sentimento == 1:
            houve_positiva = True

    media_score = sum(scores) / len(scores)

    # Se só houver notícias neutras
    if not houve_negativa and not houve_positiva:
        media_score += 0.25  # leve ajuste positivo

    # Normalização para intervalo [0, 5]
    min_valor, max_valor = -2.0, 2.0
    nota_normalizada = ((media_score - min_valor) / (max_valor - min_valor)) * 5
    nota_normalizada = max(0.0, min(5.0, nota_normalizada))  # garante que fique no intervalo

    return round(nota_normalizada, 2)

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

class AgenteAnalizer(MessagesState):
    analise_list: Annotated[Avaliacao, 'resposta final estruturada']
    empresa: Annotated[str,'Nome da empresa a ser avaliada']
    research_plan: dict
    planner_agent: list
    relevant_news: dict
    researcher_agent: list
    reader_analisys: list
    reader_agent: list
    score_dimensao: dict


@tool
def analise_empresa(empresa:str):
    """Chame essa ferramenta para inciar a análise. Passe o nome da empresa a ser pesquisada"""
    pass

@st.cache_resource()
def memory(id):
    memory_analizer = MemorySaver()
    return memory_analizer

class Analyzer:
    def __init__(self,id):
        self.config = {"configurable": {"thread_id": str(id)}}
        self.id = id
        self.chat_model_with_router = llm.bind_tools([analise_empresa])
        self.memory = memory(self.id)
        # Define a new graph
        self.workflow_analizer = StateGraph(AgenteAnalizer)

        # Define the two nodes we will cycle between
        self.workflow_analizer.add_node("chat_model", self.chat_model_analizer)
        self.workflow_analizer.add_node("planner", self.planner_agent)
        self.workflow_analizer.add_node("researcher", self.researcher_agent)
        self.workflow_analizer.add_node("reader", self.reader_agent)
        self.workflow_analizer.add_node("score", self.score)

        self.workflow_analizer.set_entry_point("chat_model")

        self.workflow_analizer.add_edge("planner", "researcher")
        self.workflow_analizer.add_edge("researcher", "reader")
        self.workflow_analizer.add_edge("reader", "score")
        self.workflow_analizer.add_edge("score", "chat_model")
        self.graph_analizer = self.workflow_analizer.compile(checkpointer=self.memory)


    def planner_agent(self,state:AgenteAnalizer):
        last_message = state['messages'][-1]
        tool_call = last_message.tool_calls
        
        empresa = str(tool_call[0]["args"]['empresa'])
        tool_call_id = tool_call[-1]["id"]

        # NOTE: it's important to insert a tool message here because LLM providers are expecting
        # all AI messages to be followed by a corresponding tool result message
        response = graph_planner.invoke({'messages':HumanMessage(f"faça a análise da empresa {empresa}")})

        tool_msg = {
            "role": "tool",
            "content": str(response['roteiro_pesquisa']),
            "tool_call_id": tool_call_id,
        }
        return Command(goto='researcher', 
                    update={'messages':[tool_msg],
                            'empresa':empresa, 
                            'research_plan':response['roteiro_pesquisa'],
                            'planner_agent':response['messages']})

    def researcher_agent(self,state:AgenteAnalizer):
        research_plan = state["research_plan"]
        response = graph_reseacher.invoke({'messages':HumanMessage(str(research_plan))})
        return {'messages':HumanMessage(f"Resultado da Análise do Agente Researcher: {str(response['final_response'])}"),
                'relevant_news':response['final_response'],
                'researcher_agent':response['messages']}

    def reader_agent(self,state:AgenteAnalizer):
        dimensao_list_news = state['relevant_news']['list_dimensao_news']
        subgraph_messages = []
        reader_analisys = []
        for dimensao in dimensao_list_news:
            response_subgraph = graph_reader.invoke({'messages': HumanMessage(str(dimensao))})
            reader_analisys.append(response_subgraph['final_response'])
            subgraph_messages.append(response_subgraph['messages'])
        
        return {'messages':HumanMessage(f"Resultado da Análise do agente Reader: {str(reader_analisys)}"),'reader_analisys':reader_analisys, 'reader_agent':subgraph_messages} 

    def score(self,state:AgenteAnalizer):
        analise_dimensoes = state['reader_analisys']
        resultado = {}
        for dim in analise_dimensoes:
            resultado[dim['dimensao']] = calcular_nota_reputacao_normalizada(dim) 
            
        return {'messages':HumanMessage(f"Com base nas notícias, o score por dimensão foi o seguinte: {str(resultado)}"),'score_dimensao':resultado}

    # Define the function that calls the model
    def chat_model_analizer(self,state: AgenteAnalizer) -> Command[Literal["planner", "__end__"]]:
        chain = prompt_agent_analizer | self.chat_model_with_router
        response = chain.invoke(input={"messages":state['messages']})
        # If there are tool calls, the LLM needs to hand off to another agent

        if len(response.tool_calls) > 0: #verificar pq o chat pode soliciar a execução de multiplas funções. Para cada uma delas precisamos de uma toolmessage com id da chamada de ferramenta pelo modelo
            tool_call = response.tool_calls        
            empresa = str(tool_call[0]["args"]['empresa'])

            return Command(goto="planner", update={"messages": [response],"empresa":empresa})

        return {"messages": [response]}
    
    def invoke(self,query:str):
        response = self.graph_analizer.invoke({'messages':HumanMessage(query)},config=self.config)
        return response["messages"][-1].content

    def stream(self,query:str):
        response = []
        events = self.graph_analizer.stream(
            input={'messages':HumanMessage(query)},
            config=self.config,
            stream_mode="values",#"updates",
            subgraphs=True,
        )
        for event in events:
            #event["messages"][-1].pretty_print()
            response.append(event)
            print('dentro da classe')
            yield event
