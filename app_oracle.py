import streamlit as st
from google import genai
from pypdf import PdfReader # Ajustado para pypdf conforme seu requirements
import pandas as pd

# 1. Configuração de Página
st.set_page_config(page_title="Oracle Judicial - PRO", page_icon="💼", layout="centered")

# 2. CSS de Limpeza
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 2rem !important;}
    .main-title {color: #1E3A8A; font-size: 32px; font-weight: bold; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica da Chave API
try:
    MINHA_CHAVE = st.secrets["AIzaSyD5RwWRI0RIu40gL82RJTYsmH56WQKCGGA"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.0-flash"
except:
    st.error("Erro na Chave API.")
    st.stop()

# --- FUNÇÃO DE EXTRAÇÃO (USANDO PYPDF) ---
def extrair_texto_pdf(arquivos_pdf):
    texto_completo = ""
    for pdf in arquivos_pdf:
        try:
            leitor = PdfReader(pdf)
            for pagina in leitor.pages:
                conteudo = pagina.extract_text()
                if conteudo:
                    texto_completo += conteudo + "\n"
        except Exception as e:
            st.error(f"Erro ao processar PDF: {e}")
    return texto_completo

# 4. Interface do Usuário
st.markdown('<p class="main-title">💼 Oracle Judicial - PRO</p>', unsafe_allow_html=True)
st.write("---")

st.subheader("1. Dossiê Digital (Upload)")
arquivos_pdf = st.file_uploader("Suba seus arquivos PDF", type="pdf", accept_multiple_files=True)

st.subheader("2. Comandos do Oráculo")
user_prompt = st.text_area("O que deseja que eu analise?", placeholder="Ex: Resuma os principais riscos desta ação...", height=150)

if st.button("Iniciar Auditoria Cognitiva", use_container_width=True):
    if not arquivos_pdf or not user_prompt:
        st.warning("Aguardando documentos e comandos...")
    else:
        with st.spinner("O Oráculo está lendo os autos..."):
            # Extração
            texto_extraido = extrair_texto_pdf(arquivos_pdf)
            
            if len(texto_extraido.strip()) < 5:
                st.error("Não consegui ler o texto desses PDFs. Eles podem ser imagens ou estar protegidos.")
            else:
                # Construção do Contexto para o Gemini
                prompt_sistema = f"""
                Você é o Oracle Judicial PRO.
                Abaixo está o texto extraído de documentos judiciais reais.
                Analise com precisão técnica.
                
                CONTEXTO:
                {texto_extraido}
                
                SOLICITAÇÃO DO ADVOGADO:
                {user_prompt}
                """
                
                try:
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=prompt_sistema
                    )
                    
                    st.markdown("### 📜 Parecer Estratégico:")
                    st.write(response.text)
                    st.success("Análise concluída!")
                    
                except Exception as e:
                    st.error(f"Erro na IA: {e}")

st.write("---")
st.caption("Oracle Judicial PRO © 2026")