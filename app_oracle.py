import streamlit as st
from google import genai
from pypdf import PdfReader 
import pandas as pd

# 1. Configuração de Página
st.set_page_config(page_title="Oracle Judicial PRO", page_icon="⚖️", layout="centered")

# 2. CSS Customizado - Black & White Style
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 1rem !important;}
    
    /* Fontes e Títulos em Preto */
    .main-title {
        color: #000000; 
        font-size: 48px !important; 
        font-weight: 850; 
        text-align: center; 
        margin-bottom: 5px;
    }
    .subtitle {
        color: #000000;
        text-align: center;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    
    h3 {
        color: #000000 !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        border-bottom: 1px solid #000000;
        padding-bottom: 5px;
    }

    /* Botão Preto e Menor */
    .stButton {
        display: flex;
        justify-content: center;
    }
    .stButton>button {
        background-color: #000000 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 2px !important;
        padding: 10px 40px !important; /* Tamanho reduzido */
        width: auto !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica de Segurança
try:
    MINHA_CHAVE = st.secrets["GOOGLE_API_KEY"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash" 
except Exception:
    st.error("Erro de Autenticação nos Secrets.")
    st.stop()

def extrair_texto(arquivos):
    texto = ""
    for pdf in arquivos:
        try:
            reader = PdfReader(pdf)
            for page in reader.pages:
                content = page.extract_text()
                if content: texto += content + "\n"
        except: continue
    return texto

# 4. Interface
st.markdown('<p class="main-title">Oracle Judicial PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">INTELIGÊNCIA JURÍDICA DE ALTA PERFORMANCE</p>', unsafe_allow_html=True)

with st.expander("📖 Guia de Utilização Rápida", expanded=True):
    st.markdown("""
    * **Carregamento:** Arraste os arquivos PDF do processo para a área abaixo.
    * **Análise:** No campo de texto, descreva o que você busca (ex: "Aponte contradições na defesa").
    * **Processamento:** O motor 2.5 Flash cruzará todos os dados em segundos.
    """)

st.write("---")

st.subheader("📂 Central de Documentos")
arquivos_pdf = st.file_uploader("Upload", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

st.subheader("⚖️ Teses e Requerimentos")
user_prompt = st.text_area("Descreva a análise técnica:", 
                         placeholder="Ex: Identifique nulidades processuais...", 
                         height=150)

# 5. Ação
if st.button("INICIAR ANÁLISE"):
    if not arquivos_pdf or not user_prompt:
        st.warning("Aguardando documentos e instruções.")
    else:
        with st.spinner("⏳ Processando..."):
            contexto = extrair_texto(arquivos_pdf)
            if len(contexto.strip()) < 10:
                st.error("Falha na leitura dos documentos.")
            else:
                try:
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=[f"CONTEXTO:\n{contexto}", f"INSTRUÇÃO:\n{user_prompt}"],
                        config={"temperature": 0.1}
                    )
                    st.markdown("### 📜 Parecer Estratégico")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Erro: {e}")

st.markdown("<br><br><center><small>Oracle Judicial PRO | © 2026</small></center>", unsafe_allow_html=True)