import streamlit as st
from google import genai
from pypdf import PdfReader 

# 1. Configuração de Página
st.set_page_config(page_title="Oracle Judicial PRO", page_icon="⚖️", layout="centered")

# Inicialização da Memória
if "historico" not in st.session_state:
    st.session_state.historico = []
if "texto_acumulado" not in st.session_state:
    st.session_state.texto_acumulado = ""

# 2. CSS Customizado - Máxima Legibilidade (Preto no Branco)
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 1rem !important; background-color: #ffffff;}
    
    /* Títulos e Fontes */
    .main-title { color: #000000; font-size: 48px !important; font-weight: 850; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #000000; text-align: center; font-size: 16px; font-weight: 500; margin-bottom: 2rem; }
    
    /* Estilo do Texto do Oráculo (Parecer) */
    .parecer-texto {
        color: #000000 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        background-color: #ffffff;
        padding: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    h3 { color: #000000 !important; font-size: 22px !important; font-weight: 700 !important; border-bottom: 2px solid #000000; padding-bottom: 5px; margin-top: 30px !important;}

    /* Botões Sóbrios */
    .stButton>button {
        background-color: #000000 !important; color: white !important; font-weight: bold !important;
        border-radius: 2px !important; padding: 10px 40px !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Configuração do Motor
try:
    MINHA_CHAVE = st.secrets["GOOGLE_API_KEY"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash"
    
    INSTRUCAO_SISTEMA = (
        "Você é o Oracle Judicial PRO, auditor jurídico. "
        "Sua análise deve ser cirúrgica. Estruture com: RESUMO EXECUTIVO, PONTOS CRÍTICOS e SUGESTÃO ESTRATÉGICA. "
        "Use negrito para destacar valores e nomes. Mantenha sobriedade máxima."
    )
except:
    st.error("Erro de Autenticação.")
    st.stop()

def extrair_texto(arquivos):
    texto_total = ""
    for pdf in arquivos:
        try:
            reader = PdfReader(pdf)
            for page in reader.pages:
                content = page.extract_text()
                if content: texto_total += f"\n--- DOC: {pdf.name} ---\n{content}\n"
        except: continue
    return texto_total

# 4. Interface
st.markdown('<p class="main-title">Oracle Judicial PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">INTELIGÊNCIA JURÍDICA DE ALTA PERFORMANCE</p>', unsafe_allow_html=True)

st.write("---")

# UPLOAD
st.subheader("📂 Central de Documentos")
arquivos_pdf = st.file_uploader("Selecione os PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

if arquivos_pdf:
    st.session_state.texto_acumulado = extrair_texto(arquivos_pdf)

# EXIBIÇÃO DO HISTÓRICO (Limpando o visual azul)
if st.session_state.historico:
    st.subheader("📜 Relatório de Auditoria")
    for msg in st.session_state.historico:
        if msg["role"] == "assistant":
            # Caixa Branca com borda fina para o Oráculo
            st.markdown(f'<div class="parecer-texto">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            # Texto simples para a sua pergunta
            st.markdown(f"**👤 Sua Instrução:** {msg['content']}")

st.subheader("⚖️ Nova Instrução")
user_prompt = st.text_area("O que deseja investigar?", placeholder="Ex: Compare as multas rescisórias...", height=100, label_visibility="collapsed")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("EXECUTAR"):
        if not st.session_state.texto_acumulado or not user_prompt:
            st.warning("Suba os arquivos e digite a instrução.")
        else:
            with st.spinner("⏳ Auditando..."):
                try:
                    contexto_conversa = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.historico])
                    prompt_final = f"{INSTRUCAO_SISTEMA}\n\nDOCS:\n{st.session_state.texto_acumulado}\n\nHISTÓRICO:\n{contexto_conversa}\n\nPERGUNTA: {user_prompt}"
                    response = client_gemini.models.generate_content(model=MODELO_IA, contents=prompt_final)
                    
                    st.session_state.historico.append({"role": "user", "content": user_prompt})
                    st.session_state.historico.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")

with col2:
    if st.button("LIMPAR"):
        st.session_state.historico = []
        st.session_state.texto_acumulado = ""
        st.rerun()

if st.session_state.historico:
    st.download_button(
        label="📄 BAIXAR RELATÓRIO",
        data=st.session_state.historico[-1]["content"],
        file_name="relatorio_oracle.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("<br><br><center><small>Oracle Judicial PRO | © 2026</small></center>", unsafe_allow_html=True)