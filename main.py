
import streamlit as st
import time
from src.agents.analyzer import Analyzer

# Streamed response emulator
def response_generator(response):
    time.sleep(0.03)
    for word in response.split(" "):
        yield word+ " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content":"olá"})
    st.session_state.var_exibicao=0

if "issues" not in st.session_state:
    st.session_state.issues = []

bot = Analyzer('6464')

with st.container():
    st.markdown("## Sentinela")
    

@st.fragment
def atualizar_chat(chat_container,prompt=None):
    with chat_container:
        if not prompt:
            #initial_message = st.chat_message("assistant")
            #initial_message.write("Olá, como posso ajudá-lo hoje?")
            messages = st.session_state.messages

            if st.session_state.var_exibicao==0:#len(messages)==0:
                with st.chat_message(messages[0]["role"]):
                    st.write_stream(response_generator(messages[0]["content"]))

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
                    response=bot.invoke(prompt)
                st.write_stream(response_generator(response))

            st.session_state.messages.append({"role": "assistant", "content": response})

chat_container = st.container(height=400,border=False)

atualizar_chat(chat_container)

if prompt:= st.chat_input("Faça uma pergunta", key="user_input"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    atualizar_chat(chat_container,prompt)
