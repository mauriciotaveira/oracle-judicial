import streamlit as st
from google import genai
from pypdf import PdfReader 
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

# 3. Lógica da Chave API (Agora com Indentação Correta)
try:
    # Esta linha abaixo TEM que estar empurrada para a direita
    MINHA_CHAVE = st.secrets["AIzaSyAKLtUNtd6mrwP11Tj1YGC5vZu6F1U0yQo"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash"
except Exception as e:
    st.error("Erro na Chave API. Verifique os Secrets.")
    st.stop()

# --- FUNÇÃO DE EXTRAÇÃO ---
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

st.subheader("2. Comandos do Oráculo 2.5 Flash")
user_prompt = st.text_area("O que deseja que eu analise?", placeholder="Ex: Analise o mérito desta petição...", height=150)

# 5. Execução
if st.button("Iniciar Auditoria Cognitiva", use_container_width=True):
    if not arquivos_pdf or not user_prompt:
        st.warning("Documentos e comandos ausentes.")
    else:
        with st.spinner("🚀 Oráculo 2.5 Flash em alta performance..."):
            texto_extraido = extrair_texto_pdf(arquivos_pdf)
            
            if len(texto_extraido.strip()) < 5:
                st.error("Documentos sem texto legível.")
            else:
                config_ia = {"temperature": 0.1}
                try:
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=[
                            f"CONTEXTO JURÍDICO:\n{texto_extraido}",
                            f"PERGUNTA:\n{user_prompt}"
                        ],
                        config=config_ia
                    )
                    st.markdown("### 📜 Parecer Estratégico:")
                    st.write(response.text)
                    st.success("Análise concluída!")
                except Exception as e:
                    st.error(f"Erro na IA: {e}")

st.write("---")
st.caption("Oracle Judicial PRO © 2026")