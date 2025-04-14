import streamlit as st
from PIL import Image

image = Image.open("SentilenaAI.png")
image = image.resize((1200, 250))  # Ajuste conforme necessário


pages = {
    "SentinelAI": [
        st.Page("./pages/chat_page.py", title="Chat com assistente"),
    ],
    "Recursos": [
         st.Page("./pages/about_page.py", title="Sobre"),
         st.Page("./pages/score_page.py", title="Cálculo de Score"),
         st.Page("./pages/workflow_page.py", title="Workflow de Agentes"),
     ]
}

st.logo(image, size="large") 
pg = st.navigation(pages)
pg.run()