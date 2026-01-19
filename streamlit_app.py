import streamlit as st

st.set_page_config(layout="wide")

st.title("📊 Painel Geral")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💰 FINANCEIRO", use_container_width=True):
        st.session_state["pagina"] = "financeiro"

with col2:
    if st.button("🛠 MANUTENÇÃO", use_container_width=True):
        st.session_state["pagina"] = "manutencao"

with col3:
    if st.button("🚚 LOGÍSTICA", use_container_width=True):
        st.session_state["pagina"] = "logistica"
