import streamlit as st
from google import genai
from pypdf import PdfReader 

# 1. Configuração de Página
st.set_page_config(page_title="Oracle Judicial PRO", page_icon="⚖️", layout="centered")

# Inicialização da Memória (State)
if "historico" not in st.session_state:
    st.session_state.historico = []
if "texto_acumulado" not in st.session_state:
    st.session_state.texto_acumulado = ""

# 2. CSS Customizado - Foco em Preto, Branco e Usabilidade
st.markdown("""
    <style>
    [data-testid="stHeader"], header, footer, .stAppDeployButton, #MainMenu {visibility: hidden; display: none;}
    .block-container {padding-top: 1rem !important;}
    .main-title { color: #000000; font-size: 48px !important; font-weight: 850; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #000000; text-align: center; font-size: 16px; font-weight: 500; margin-bottom: 2rem; }
    h3 { color: #000000 !important; font-size: 22px !important; font-weight: 700 !important; border-bottom: 1px solid #000000; padding-bottom: 5px; margin-top: 20px !important;}
    
    /* Botão Centralizado e Menor */
    .stButton { display: flex; justify-content: center; margin-top: 20px;}
    .stButton>button {
        background-color: #000000 !important; color: white !important; font-weight: bold !important;
        border-radius: 2px !important; padding: 10px 40px !important; width: auto !important; border: none !important;
    }
    
    /* Histórico de Conversa */
    .chat-card { padding: 15px; border-radius: 5px; border-left: 5px solid #000; background-color: #f9f9f9; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Configuração do Motor
try:
    MINHA_CHAVE = st.secrets["GOOGLE_API_KEY"]
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
    MODELO_IA = "gemini-2.5-flash"
    
    INSTRUCAO_SISTEMA = (
        "Você é o Oracle Judicial PRO, auditor jurídico de alta performance. "
        "Sua missão é realizar análises cirúrgicas, apontando contradições de centavos, termos e cláusulas. "
        "Estruture sempre com: RESUMO EXECUTIVO, PONTOS CRÍTICOS/DIVERGÊNCIAS e SUGESTÃO ESTRATÉGICA."
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
                if content: texto_total += f"\n--- DOCUMENTO: {pdf.name} ---\n{content}\n"
        except: continue
    return texto_total

# 4. Interface Principal
st.markdown('<p class="main-title">Oracle Judicial PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">INTELIGÊNCIA JURÍDICA DE ALTA PERFORMANCE</p>', unsafe_allow_html=True)

with st.expander("📖 Guia de Utilização Rápida", expanded=True):
    st.markdown("""
    * **Múltiplos Arquivos:** Clique em 'Browse files' e selecione vários PDFs segurando a tecla 'Ctrl' ou 'Command'.
    * **Histórico:** O Oráculo agora lembra o que foi discutido sobre os documentos atuais.
    * **Download:** Baixe o parecer técnico gerado para usar em suas petições.
    """)

st.write("---")

# ÁREA DE UPLOAD (Corrigida para múltiplos arquivos)
st.subheader("📂 Central de Documentos")
arquivos_pdf = st.file_uploader("Selecione um ou mais PDFs", type="pdf", accept_multiple_files=True)

# Processa o texto se houver arquivos novos
if arquivos_pdf:
    st.session_state.texto_acumulado = extrair_texto(arquivos_pdf)

# Exibição do Histórico em Cartões
if st.session_state.historico:
    st.subheader("💬 Histórico da Auditoria")
    for msg in st.session_state.historico:
        role = "⚖️ Oráculo" if msg["role"] == "assistant" else "👤 Você"
        st.markdown(f"**{role}**")
        st.info(msg["content"]) if msg["role"] == "assistant" else st.write(msg["content"])

st.subheader("⚖️ Instruções de Análise")
user_prompt = st.text_area("O que o Oráculo deve investigar agora?", placeholder="Ex: Analise a Cláusula 10 de ambos os contratos...", height=120)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("EXECUTAR ANÁLISE"):
        if not st.session_state.texto_acumulado or not user_prompt:
            st.warning("Suba os arquivos e digite sua dúvida.")
        else:
            with st.spinner("⏳ Auditando documentos..."):
                try:
                    # Monta o contexto enviando o histórico + documentos + pergunta nova
                    contexto_conversa = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.historico])
                    prompt_final = f"{INSTRUCAO_SISTEMA}\n\nCONTEXTO:\n{st.session_state.texto_acumulado}\n\nHISTÓRICO:\n{contexto_conversa}\n\nPERGUNTA: {user_prompt}"
                    
                    response = client_gemini.models.generate_content(model=MODELO_IA, contents=prompt_final)
                    
                    # Atualiza Histórico
                    st.session_state.historico.append({"role": "user", "content": user_prompt})
                    st.session_state.historico.append({"role": "assistant", "content": response.text})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro no Motor: {e}")

with col2:
    if st.button("LIMPAR TUDO"):
        st.session_state.historico = []
        st.session_state.texto_acumulado = ""
        st.rerun()

# 5. Download do Último Parecer
if st.session_state.historico:
    ultima_analise = st.session_state.historico[-1]["content"]
    st.download_button(
        label="📄 BAIXAR PARECER TÉCNICO",
        data=ultima_analise,
        file_name="parecer_tecnico_oracle.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("<br><br><center><small>Oracle Judicial PRO | © 2026</small></center>", unsafe_allow_html=True)