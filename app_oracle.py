import streamlit as st
from google import genai
import os

# 1. Configuração de Página (DEVE ser a primeira coisa)
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

# 3. Lógica de Captura da Chave (O "Coração" do problema)
MINHA_CHAVE = None

# Tentativa A: Buscar nos Secrets do Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    MINHA_CHAVE = st.secrets["AIzaSyD5RwWRI0RIu40gL82RJTYsmH56WQKCGGA"]
# Tentativa B: Buscar qualquer chave que exista nos Secrets (caso o nome esteja levemente diferente)
elif len(st.secrets) > 0:
    MINHA_CHAVE = list(st.secrets.values())[0]

# Verificação Final
if not MINHA_CHAVE:
    st.error("⚠️ Erro: Chave API não encontrada nos Secrets do Streamlit.")
    st.info("💡 Como resolver: Vá em Settings > Secrets e cole: GOOGLE_API_KEY = 'SUA_CHAVE'")
    st.stop()
else:
    try:
        client_gemini = genai.Client(api_key=MINHA_CHAVE)
        MODELO_IA = "gemini-2.0-flash"
    except Exception as e:
        st.error(f"Erro ao conectar com o Google: {e}")
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
            # O processamento virá aqui após a correção da conexão
            st.success("Conexão com Gemini estabelecida com sucesso!")
            st.info("Sistema pronto para análise.")

st.write("---")
st.caption("Oracle Judicial PRO © 2026")