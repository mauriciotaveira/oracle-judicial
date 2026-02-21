import streamlit as st
from google import genai
from pypdf import PdfReader 
import pandas as pd

# 1. Configuração de Página (Identidade Visual)
st.set_page_config(page_title="Oracle Judicial PRO", page_icon="⚖️", layout="centered")

# 2. CSS Customizado para Design de Alto Nível
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 1rem !important;}
    
    /* Título Monumental */
    .main-title {
        color: #1E3A8A; 
        font-size: 50px !important; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    .subtitle {
        color: #64748B;
        text-align: center;
        font-size: 18px;
        margin-bottom: 2rem;
    }
    
    /* Estilização de Seções */
    h3 {
        color: #1E293B !important;
        font-size: 24px !important;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 10px;
        margin-top: 25px !important;
    }
    
    /* Botão de Execução */
    .stButton>button {
        background-color: #1E3A8A !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica de Segurança da Chave
try:
    MINHA_CHAVE = st.secrets["GOOGLE_API_KEY"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash" 
except Exception:
    st.error("Erro de Autenticação. Verifique os Secrets.")
    st.stop()

# --- MOTOR DE EXTRAÇÃO ---
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

# 4. Interface Redenhada
st.markdown('<p class="main-title">Oracle Judicial PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Inteligência Jurídica de Alta Performance</p>', unsafe_allow_html=True)

# Bloco de Instruções (O Guia que faltava)
with st.expander("📖 Guia de Utilização Rápidda", expanded=False):
    st.markdown("""
    1. **Carregamento:** Arraste os arquivos PDF do processo para a área abaixo.
    2. **Análise:** No campo de texto, descreva o que você busca (ex: "Aponte contradições na defesa").
    3. **Processamento:** O motor 2.5 Flash cruzará todos os dados em segundos.
    4. **Resultado:** O parecer será gerado com base estrita nos documentos fornecidos.
    """)

st.write("---")

# Seções com nomes melhores
st.subheader("📂 Central de Documentos")
arquivos_pdf = st.file_uploader("Selecione os autos do processo (PDF)", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

st.subheader("⚖️ Teses e Requerimentos")
user_prompt = st.text_area("Descreva a análise técnica pretendida:", 
                         placeholder="Ex: Elabore um resumo executivo focando nos riscos de sucumbência...", 
                         height=150)

# 5. Ação
if st.button("INICIAR ANÁLISE ESTRATÉGICA", use_container_width=True):
    if not arquivos_pdf or not user_prompt:
        st.warning("Aguardando documentos e instruções para prosseguir.")
    else:
        with st.spinner("⏳ Analisando evidências com motor 2.5 Flash..."):
            contexto = extrair_texto(arquivos_pdf)
            
            if len(contexto.strip()) < 10:
                st.error("Falha na leitura: Os documentos parecem ser imagens ou estão protegidos.")
            else:
                try:
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=[f"CONTEXTO:\n{contexto}", f"INSTRUÇÃO:\n{user_prompt}"],
                        config={"temperature": 0.1}
                    )
                    st.markdown("### 📜 Parecer do Oráculo")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")

st.markdown("<br><br><center><small>Oracle Judicial PRO | © 2026</small></center>", unsafe_allow_html=True)