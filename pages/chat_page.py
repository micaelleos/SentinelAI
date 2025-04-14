
import streamlit as st
import time
from src.agents.analyzer import Analyzer
from langchain_core.messages import HumanMessage,  SystemMessage, AIMessage, ToolMessage
import uuid
from src.text import saudacao

# Streamed response emulator
def response_generator(response):
    time.sleep(0.03)
    for word in response.split(" "):
        yield word+ " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content":saudacao})
    st.session_state.var_exibicao=0

if "issues" not in st.session_state:
    st.session_state.issues = []

bot = Analyzer(str(uuid.uuid4()))

with st.container():
    st.markdown("## SentinelAI")
    
@st.fragment
def atualizar_chat(chat_container,prompt=None):
    with chat_container:
        if not prompt:
            #initial_message = st.chat_message("assistant")
            #initial_message.write("Olá, como posso ajudá-lo hoje?")
            messages = st.session_state.messages

            if st.session_state.var_exibicao==0:#len(messages)==0:
                with st.chat_message(messages[0]["role"]):
                    st.write_stream(response_generator(saudacao))

                st.session_state.var_exibicao=1
            else:
                for i in range(0,len(messages)):
                    message = messages[i]       
                                        
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])    

        else:
            message = st.session_state.messages.copy()
            with st.chat_message(message[-1]["role"]):
                    st.markdown(message[-1]["content"])  

            with st.chat_message("assistant"):
                with st.spinner(''):
                    for role, response in bot.stream(prompt):
                        
                        if role:
                            role_str = role[0]
                            role_name, role_id = role_str.split(":")
                            if not isinstance(response['messages'][-1],HumanMessage):

                                if isinstance(response['messages'][-1],ToolMessage):
                                    with st.expander(f"Agente {str(role_name).title()} usando ferramenta ..."):  
                                        st.write(response['messages'][-1].content)
                                else:
                                    with st.expander(f"Agente {str(role_name).title()} pensando ..."):  
                                        st.write(response['messages'][-1].content)
                        else:
                            if not isinstance(response['messages'][-1],HumanMessage):
                                #st.write(response['messages'][-1].content)
                                st.write_stream(response_generator(response['messages'][-1].content))
                                st.session_state.messages.append({"role": "assistant", "content": response['messages'][-1].content})

chat_container = st.container(height=400,border=False)

atualizar_chat(chat_container)

if prompt:= st.chat_input("Faça uma pergunta", key="user_input"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    atualizar_chat(chat_container,prompt)
