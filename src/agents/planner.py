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

from src.tools import tools_planner
from src.prompts.planner import prompt_agent_planner, prompt_structure

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class SearchPlan(TypedDict):
    dimensao: Annotated[str,'Dimensao da pesquisa']
    objetivo_de_pesquisa: Annotated[str,'Objetivo da pesquisa']
    perguntas: Annotated[str,'Lista de perguntas orientadoras para a pesquisa']
    raciocínio: Annotated[str,'Raciocínio por detrás da pesquisa']
    termos_de_pesquisa: Annotated[str, "Termos de pesquisa"]

class RoteiroPesquisa(TypedDict):
    """Roteiro para execução da pesquisa"""
    planejamento_de_pesquisa: Annotated[list[SearchPlan], "Lista com roteiro de pesquisa para avaliação reputacional da empresa"]
    identidade_empresa: Annotated[str, "Principais informações e pontos cahves da identidade corporativa da empresa"]

class AgentStatePlanner(MessagesState):
    # Final structured response from the agent
    roteiro_pesquisa: Annotated[RoteiroPesquisa, "Roteiro para a pesquisa"]



llm_formater = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18", temperature=0.3,openai_api_key=OPENAI_API_KEY)

llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3,openai_api_key=OPENAI_API_KEY)

model_with_tool_planner = llm.bind_tools(tools_planner)

model_with_structured_output_planner = llm_formater.with_structured_output(RoteiroPesquisa)


memory_planner = MemorySaver()

# Define the function that calls the model
def call_model_planner(state: AgentStatePlanner):
    chain = prompt_agent_planner | model_with_tool_planner
    response = chain.invoke(input={"messages":state['messages']})
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function that determines whether to continue or not
def should_continue_planner(state: AgentStatePlanner):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we respond to the user
    if not last_message.tool_calls:
        return 'finish_plan'
    # Otherwise if there is, we continue
    else:
        return "continue"
    
# Define the function that determines whether to continue or not
def format_plan(state: AgentStatePlanner):
    chain = prompt_structure | model_with_structured_output_planner
    planejamento_de_pesquisa = chain.invoke(input={"messages":[HumanMessage(content=state["messages"][-1].content)]})
    # We return the final answer
    return {'roteiro_pesquisa':planejamento_de_pesquisa}


# Define a new graph
workflow_planner = StateGraph(AgentStatePlanner)

# Define the two nodes we will cycle between
workflow_planner.add_node("agent_planner", call_model_planner)
workflow_planner.add_node("tools", ToolNode(tools_planner))
workflow_planner.add_node("format_plan", format_plan)
# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow_planner.set_entry_point("agent_planner")

# We now add a conditional edge
workflow_planner.add_conditional_edges(
    "agent_planner",
    should_continue_planner,
    {
        "continue": "tools",
        'finish_plan': 'format_plan',
    },
)

workflow_planner.add_edge("tools", "agent_planner")
workflow_planner.add_edge("format_plan", END)

graph_planner = workflow_planner.compile(checkpointer=memory_planner)