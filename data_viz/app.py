"""Python file to serve as the frontend"""
import sys
import os

sys.path.append(os.path.abspath('.'))

from data_viz.components.sidebar import sidebar
from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
import requests

st.set_page_config(
    page_title="FIAP - MLE Tech Challenge - 2MLET",
    layout="wide"
)

sidebar()

st.title('📊 Visualização de dados')

if 'df' not in st.session_state:
    st.session_state.df = None

if 'pyg_app' not in st.session_state:
    st.session_state.pyg_app = None

col1, col2, col3, col4 = st.columns(4)
with col1:
    ano_min = st.number_input('Insira o ano_min', value=1970, key='ano_min')
with col2:
    ano_max = st.number_input('Insira o ano_max', value=2023, key='ano_max')
with col3:
    origem = st.selectbox('Insira a origem',  ('Exportacao', 'Comercializacao', 'Importacao', 'Producao', 'Processamento'))
with col4:    
    limit = st.number_input('Insira o limit', value=10, key='limit')

if st.button('Execute'):
    if not st.session_state.get("open_api_key_configured"):
        st.error("Please configure your API Keys!")
    else:
        url = f"http://mle-api/api/v1/vitibrasil/origem/?skip=0&limit={limit}&origem={origem}&ano_min={ano_min}&ano_max={ano_max}"
        payload = {}
        headers = {
        'Authorization': f'Bearer {st.session_state["OPENAI_API_KEY"]}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        st.session_state.df = pd.DataFrame(response.json())

        st.session_state.pyg_app = StreamlitRenderer(st.session_state.df)
    
# Render pygwalker explorer if DataFrame exists
if st.session_state.df is not None:
    st.session_state.pyg_app.explorer()