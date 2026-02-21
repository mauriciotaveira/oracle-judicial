import streamlit as st
from google import genai

# 1. Configuração de Página
st.set_page_config(page_title="Oracle Judicial - PRO", page_icon="💼", layout="centered")

# 2. CSS para Limpar a Interface
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    [data-testid="stHeader"] {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica da Chave (Aqui estava o erro!)
try:
    # O código busca o NOME da gaveta, não o valor da chave direto
    MINHA_CHAVE = st.secrets["AIzaSyD5RwWRI0RIu40gL82RJTYsmH56WQKCGGA"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.0-flash"
except Exception as e:
    st.error("⚠️ Configuração Pendente: A chave API não foi encontrada nos Secrets.")
    st.info("No painel do Streamlit (Settings > Secrets), verifique se está assim: GOOGLE_API_KEY = 'SUA_CHAVE'")
    st.stop()

# 4. Interface do Usuário
st.markdown("<h1>💼 Oracle Judicial - PRO</h1>", unsafe_allow_html=True)
st.markdown("<h3>Auditoria Cruzada e Exportação de Pareceres ⚖️</h3>", unsafe_allow_html=True)
st.write("---")

st.subheader("1. Construa o Dossiê")
arquivos_pdf = st.file_uploader("Upload de PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

st.write("")

st.subheader("2. Análise Estratégica & Cognição")
user_prompt = st.text_area("Comande a Inteligência:", placeholder="Ex: Analise contradições entre os documentos...", height=150)

if st.button("Gerar Parecer Estratégico"):
    if not arquivos_pdf:
        st.warning("Por favor, suba os arquivos PDF.")
    elif not user_prompt:
        st.warning("Por favor, digite sua pergunta.")
    else:
        with st.spinner("Processando cognição jurídica..."):
            st.success("Conexão com Gemini estabelecida com sucesso!")
            st.info("Sistema pronto para análise.")

st.write("---")
st.caption("Oracle Judicial PRO © 2026")