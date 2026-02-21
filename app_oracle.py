import streamlit as st
from google import genai
from pypdf import PdfReader 
import pandas as pd

# 1. Configuração de Página (Primeira linha sempre!)
st.set_page_config(page_title="Oracle Judicial - PRO", page_icon="💼", layout="centered")

# 2. CSS de Limpeza Profissional
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 2rem !important;}
    .main-title {color: #1E3A8A; font-size: 32px; font-weight: bold; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# 3. Lógica da Chave API (Corrigida para usar o nome da gaveta nos Secrets)
try:
    # Aqui usamos o nome da variável configurada no Streamlit Cloud
    # NO VS CODE (app_oracle.py)
try:
    # O comando abaixo NÃO deve ter o código AIza...
    # Ele deve ter apenas o NOME que você salvou no painel do Streamlit
    # FORMA CORRETA (Copie e cole estas 3 linhas)
try:
    # O segredo é chamar pelo NOME "GOOGLE_API_KEY", não pelo valor AIza...
    MINHA_CHAVE = st.secrets["GOOGLE_API_KEY"] 
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash"
except Exception as e:
    st.error("Erro na Chave API. Verifique os Secrets no painel do Streamlit.")
    st.stop()
    
    # MOTOR DE FÓRMULA 1 ATIVADO: Gemini 2.5 Flash
    MODELO_IA = "gemini-2.5-flash" 
except Exception as e:
    st.error(f"Erro na Chave API: {e}")
    st.info("Verifique se 'GOOGLE_API_KEY' está nos Secrets do Streamlit.")
    st.stop()

# --- FUNÇÃO DE EXTRAÇÃO (OTIMIZADA) ---
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
user_prompt = st.text_area("O que deseja que eu analise?", placeholder="Ex: Analise o risco de sucumbência baseado nesta contestação...", height=150)

# 5. Execução com Alta Performance
if st.button("Iniciar Auditoria Cognitiva", use_container_width=True):
    if not arquivos_pdf or not user_prompt:
        st.warning("Aguardando documentos e comandos...")
    else:
        with st.spinner("🚀 Motor 2.5 Flash em alta rotação... Analisando autos."):
            # Extração de texto
            texto_extraido = extrair_texto_pdf(arquivos_pdf)
            
            if len(texto_extraido.strip()) < 5:
                st.error("Documentos sem texto legível (precisam de OCR).")
            else:
                # Configuração de Resposta Rápida
                config_ia = {
                    "temperature": 0.1,  # Máxima precisão jurídica
                    "top_p": 0.95,
                }
                
                try:
                    # Envio direto para o Long Context do 2.5 Flash
                    response = client_gemini.models.generate_content(
                        model=MODELO_IA,
                        contents=[
                            f"CONTEXTO JURÍDICO DOS DOCUMENTOS:\n{texto_extraido}",
                            f"PERGUNTA DO ADVOGADO:\n{user_prompt}"
                        ],
                        config=config_ia
                    )
                    
                    st.markdown("### 📜 Parecer Estratégico (Elite):")
                    st.write(response.text)
                    st.success("Análise concluída com motor 2.5 Flash!")
                    
                except Exception as e:
                    st.error(f"Erro no processamento da IA: {e}")

st.write("---")
st.caption("Oracle Judicial PRO © 2026 | Powered by Gemini 2.5 Flash")