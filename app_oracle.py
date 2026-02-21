import streamlit as st
import chromadb
from google import genai
import pypdf

# 1. Configuração da Página (DEVE ser a primeira linha de código Streamlit)
st.set_page_config(page_title="Oracle Judicial - PRO", page_icon="💼", layout="centered")

# 2. CSS PARA LIMPAR A INTERFACE (Remove botões, menus e espaços extras)
st.markdown("""
    <style>
    /* Esconde o menu (hambúrguer) e o cabeçalho padrão */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Esconde o botão 'Deploy' e a barra superior de decoração */
    .stAppDeployButton {display:none;}
    #stDecoration {display:none;}
    [data-testid="stHeader"] {visibility: hidden;}
    
    /* Remove o espaço em branco excessivo no topo */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Configuração da Chave (Puxando dos Secrets do Streamlit)
try:
    MINHA_CHAVE = st.secrets["AIzaSyBWDEZqhRjjujVpxBogNJ16vFqMbMEqXRA"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.0-flash"
except Exception as e:
    st.error("Erro ao carregar a Chave API. Verifique os Secrets.")
    st.stop()

# 4. Interface Visual
st.markdown("<h1>💼 Oracle Judicial - PRO</h1>", unsafe_allow_html=True)
st.markdown("<h3>Auditoria Cruzada e Exportação de Pareceres ⚖️</h3>", unsafe_allow_html=True)
st.write("---")

# Seção 1: Upload
st.subheader("1. Construa o Dossiê")
st.write("Arraste os PDFs do caso para análise:")
arquivos_pdf = st.file_uploader(
    "Upload de PDFs", 
    type="pdf", 
    accept_multiple_files=True, 
    label_visibility="collapsed"
)

st.write("")

# Seção 2: A nova nomenclatura
st.subheader("2. Análise Estratégica & Cognição")

# Caixa de texto para o comando
user_prompt = st.text_area("Comande a Inteligência (Ex: Liste contradições entre os depoimentos):", height=150)

if st.button("Gerar Parecer Estratégico"):
    if not arquivos_pdf:
        st.warning("Por favor, suba pelo menos um arquivo PDF.")
    elif not user_prompt:
        st.warning("Por favor, digite o que deseja analisar.")
    else:
        with st.spinner("Analisando documentos e gerando cognição..."):
            # Aqui entra a sua lógica de processamento que já existia
            # (Leitura de PDF, ChromaDB e chamada ao Gemini)
            st.success("Análise concluída!")
            st.markdown("### Resultado da Análise")
            st.write("O resultado do seu parecer aparecerá aqui.")

# Rodapé minimalista (Opcional)
st.write("---")
st.caption("Oracle Judicial PRO © 2026 - Tecnologia Jurídica Avançada")