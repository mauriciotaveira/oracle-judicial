import streamlit as st
from google import genai
from pypdf import PdfReader 
import pandas as pd

# 1. Configuração de Página
st.set_page_config(page_title="Oracle Judicial - PRO", page_icon="💼", layout="centered")

# 2. Estilo Visual
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 2rem !important;}
    .main-title {color: #1E3A8A; font-size: 32px; font-weight: bold; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# 3. Conexão com a Chave (FORMA SEGURA)
try:
    # O comando abaixo NUNCA deve ser alterado para conter a chave AIza.
    # Ele deve ficar exatamente assim, pois "GOOGLE_API_KEY" é apenas o NOME da variável no site.
    MINHA_CHAVE = st.secrets["GOOGLE_API_KEY"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash" 
except Exception:
    st.error("Erro: A etiqueta 'GOOGLE_API_KEY' não foi encontrada nos Secrets do Streamlit.")
    st.stop()

# --- FUNÇÃO DE LEITURA ---
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

# 4. Interface
st.markdown('<p class="main-title">💼 Oracle Judicial - PRO</p>', unsafe_allow_html=True)
st.write("---")

st.subheader("1. Dossiê Digital")
arquivos_pdf = st.file_uploader("Upload de PDFs", type="pdf", accept_multiple_files=True)

st.subheader("2. Comando do Oráculo")
user_prompt = st.text_area("Análise desejada:", placeholder="Ex: Resuma os pedidos...", height=150)

# 5. Execução
if st.button("Executar Análise de Elite", use_container_width=True):
    if not arquivos_pdf or not user_prompt:
        st.warning("Envie os documentos e o comando.")
    else:
        with st.spinner("🚀 Motor 2.5 Flash processando..."):
            texto_extraido = extrair_texto_pdf(arquivos_pdf)
            if len(texto_extraido.strip()) < 10:
                st.error("Não foi possível ler o texto do PDF.")
            else:
                try:
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=[f"CONTEXTO:\n{texto_extraido}", f"PERGUNTA:\n{user_prompt}"],
                        config={"temperature": 0.1}
                    )
                    st.markdown("### 📜 Parecer Estratégico:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")

st.write("---")
st.caption("Oracle Judicial PRO © 2026")