import streamlit as st

from data_viz.components.faq import faq

def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True

def sidebar():
    with st.sidebar:
        st.markdown(
            "## Como utilizar\n"
            "1. Insira o token abaixo 🔑\n"  # noqa: E501
        )
        open_api_key_input = st.text_input(
            "API token",
            type="password",
            placeholder="Paste your API key here (sk-...)",
            help="Você pode obter o seu token em: http://localhost/docs#/default/login_api_v1_token_post",  # noqa: E501
            value=st.session_state.get("OPEN_API_KEY", ""),
        )

        if open_api_key_input:
            # print(f'Entered API is {open_api_key_input}')
            set_open_api_key(open_api_key_input)

        if not st.session_state.get("open_api_key_configured"):
            st.error("Insira o seu token!")
        else:
            st.markdown("Token inserido!")

        st.markdown("---")
        st.markdown("# Sobre")
        st.markdown(
            """📖 Tech Challenge 
Machine Learning Engineering"""
        )
        st.markdown("Turma 2")
        st.markdown("""### Integrantes do grupo: 
- Alecrim 
- Diogo Padilha 
- Felipe Bizzo 
- Gabriel Ronny 
- Thales Gomes""")
        st.markdown("---")
