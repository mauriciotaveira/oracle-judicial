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
    .main-title { color: #000000; font-size: 48px !important; font-weight: 850; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #000000; text-align: center; font-size: 16px; font-weight: 500; margin-bottom: 2rem; }
    h3 { color: #000000 !important; font-size: 22px !important; font-weight: 700 !important; border-bottom: 1px solid #000000; padding-bottom: 5px; }
    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background-color: #000000 !important; color: white !important; font-weight: bold !important;
        border-radius: 2px !important; padding: 10px 40px !important; width: auto !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica de Segurança e Instrução de Sistema (System Instruction)
try:
    MINHA_CHAVE = st.secrets["GOOGLE_API_KEY"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    
    # DEFINIÇÃO DO PERSONAGEM ESTRATÉGICO
    INSTRUCAO_SISTEMA = (
        "Você é o Oracle Judicial PRO, uma IA de elite especializada em análise estratégica de processos judiciais. "
        "Sua missão é ler documentos jurídicos e fornecer pareceres técnicos, sóbrios e altamente precisos. "
        "Ao responder: 1) Seja formal e direto. 2) Se encontrar contradições, destaque-as. "
        "3) Organize sua resposta em seções: 'RESUMO EXECUTIVO', 'PONTOS CRÍTICOS/RISCOS' e 'SUGESTÃO ESTRATÉGICA'. "
        "Sempre baseie suas conclusões exclusivamente nos documentos fornecidos."
    )
    
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
    * **Carregamento:** Arraste os arquivos PDF do processo abaixo.
    * **Análise:** Descreva o que você busca identificar nos autos.
    * **Processamento:** O motor 2.5 Flash aplicará a diretriz estratégica ao conteúdo.
    """)

st.write("---")
st.subheader("📂 Central de Documentos")
arquivos_pdf = st.file_uploader("Upload", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

st.subheader("⚖️ Teses e Requerimentos")
user_prompt = st.text_area("Descreva a análise técnica:", placeholder="Ex: Analise o depoimento da testemunha X em face da petição inicial...", height=150)

# 5. Ação com System Instruction integrada
if st.button("INICIAR ANÁLISE"):
    if not arquivos_pdf or not user_prompt:
        st.warning("Aguardando documentos e instruções.")
    else:
        with st.spinner("⏳ Oráculo processando sob diretrizes estratégicas..."):
            contexto = extrair_texto(arquivos_pdf)
            if len(contexto.strip()) < 10:
                st.error("Falha na leitura dos documentos.")
            else:
                try:
                    # O Motor 2.5 Flash agora recebe a instrução de sistema
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=[f"INSTRUÇÃO DE SISTEMA: {INSTRUCAO_SISTEMA}", f"CONTEXTO DOS AUTOS: {contexto}", f"PEDIDO DO USUÁRIO: {user_prompt}"],
                        config={"temperature": 0.1}
                    )
                    st.markdown("### 📜 Parecer Estratégico")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Erro: {e}")

st.markdown("<br><br><center><small>Oracle Judicial PRO | © 2026</small></center>", unsafe_allow_html=True)