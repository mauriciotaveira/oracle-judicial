import streamlit as st
from google import genai
from pypdf import PdfReader 
import pandas as pd

# 1. Configuração de Página
st.set_page_config(page_title="Oracle Judicial - PRO", page_icon="💼", layout="centered")

# 2. Estilo Visual Profissional
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 2rem !important;}
    .main-title {color: #1E3A8A; font-size: 32px; font-weight: bold; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# 3. Conexão com a Chave (CORRIGIDO PARA BUSCAR DOS SECRETS)
try:
    # AQUI ESTAVA O ERRO: Não colocamos o código AIza aqui, colocamos o NOME da gaveta.
    if "GOOGLE_API_KEY" in st.secrets:
        MINHA_CHAVE = st.secrets["AIzaSyBrO6dUaduR4KctMMvOErW_4UtvvPyvcY4"]
    else:
        # Tenta buscar em uma estrutura secundária se o Streamlit mudar
        MINHA_CHAVE = st.secrets.get("default", {}).get("GOOGLE_API_KEY")

    if not MINHA_CHAVE:
        st.error("Chave 'GOOGLE_API_KEY' não encontrada nos Secrets do Streamlit.")
        st.stop()

    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash" 
    
except Exception as e:
    st.error(f"Erro na conexão com a API: {e}")
    st.stop()

# --- FUNÇÃO TÉCNICA DE LEITURA ---
def extrair_texto_pdf(arquivos_pdf):
    texto_completo = ""
    for pdf in arquivos_pdf:
        try:
            leitor = PdfReader(pdf)
            for pagina in leitor.pages:
                conteudo = pagina.extract_text()
                if conteudo:
                    texto_completo += conteudo + "\n"
        except Exception:
            continue
    return texto_completo

# 4. Interface do Usuário
st.markdown('<p class="main-title">💼 Oracle Judicial - PRO</p>', unsafe_allow_html=True)
st.write("---")

st.subheader("1. Dossiê Digital (Upload de PDFs)")
arquivos_pdf = st.file_uploader("Arraste seus arquivos aqui", type="pdf", accept_multiple_files=True)

st.subheader("2. Comando Estratégico")
user_prompt = st.text_area("O que o Oráculo deve analisar?", 
                         placeholder="Ex: Identifique as contradições entre a contestação e as provas anexadas.", 
                         height=150)

# 5. Execução com o Motor 2.5 Flash
if st.button("Executar Análise de Elite", use_container_width=True):
    if not arquivos_pdf or not user_prompt:
        st.warning("Por favor, forneça documentos e um comando.")
    else:
        with st.spinner("🚀 Oráculo 2.5 Flash em alta rotação..."):
            texto_extraido = extrair_texto_pdf(arquivos_pdf)
            
            if len(texto_extraido.strip()) < 10:
                st.error("Não foi possível extrair texto. O PDF pode ser uma imagem protegida.")
            else:
                try:
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=[
                            f"CONTEXTO DOS DOCUMENTOS:\n{texto_extraido}",
                            f"SOLICITAÇÃO DO ADVOGADO:\n{user_prompt}"
                        ],
                        config={"temperature": 0.1}
                    )
                    
                    st.markdown("### 📜 Parecer Estratégico:")
                    st.write(response.text)
                    st.success("Análise finalizada pelo motor 2.5 Flash!")
                except Exception as e:
                    st.error(f"Erro no processamento da IA: {e}")

st.write("---")
st.caption("Oracle Judicial PRO © 2026 | Tecnologia de Contexto Longo 2.5 Flash")