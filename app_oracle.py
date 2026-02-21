import streamlit as st
import chromadb
from google import genai
import pypdf

st.set_page_config(page_title="Oracle Judicial - PRO", page_icon="💼", layout="centered")

# ==========================================
# 👇 SEGURANÇA E CONFIGURAÇÃO DA IA (NUVEM)
# ==========================================
try:
    MINHA_CHAVE = st.secrets.get("AIzaSyBWDEZqhRjjujVpxBogNJ16vFqMbMEqXRA")
except:
    MINHA_CHAVE = None

MODELO_IA = "gemini-2.5-flash"

if MINHA_CHAVE:
    client_gemini = genai.Client(api_key=MINHA_CHAVE)
else:
    st.error("⚠️ Chave API não encontrada. Configure os Secrets no painel do Streamlit.")
    st.stop() # Trava o app até a chave ser colocada

# ==========================================
# 🧠 BANCO DE DADOS (MEMÓRIA DO ORÁCULO)
# ==========================================
@st.cache_resource
def inicializar_banco():
    chroma_client = chromadb.Client()
    colecao = chroma_client.create_collection(name="base_auditoria_pro")
    return colecao

colecao_processos = inicializar_banco()

# ==========================================
# 🎨 A INTERFACE WEB
# ==========================================

st.title("💼 Oracle Judicial - PRO")
st.subheader("Auditoria Cruzada e Exportação de Pareceres 🖨️")
st.markdown("---")

# 📥 1. ÁREA DE UPLOAD E LEITURA DE PDF
st.markdown("### 1. Construa o Dossiê")
ficheiros_pdf = st.file_uploader("Arraste todos os PDFs do caso de uma vez", type=["pdf"], accept_multiple_files=True)

if ficheiros_pdf:
    with st.spinner(f'A processar {len(ficheiros_pdf)} documento(s)...'):
        documentos_adicionados = 0
        
        for ficheiro in ficheiros_pdf:
            nome_doc = ficheiro.name
            
            # Evita ler o mesmo PDF duas vezes
            try:
                existente = colecao_processos.get(ids=[nome_doc])
                if existente and len(existente['ids']) > 0:
                    continue 
            except:
                pass

            # Extração de texto do PDF
            leitor_pdf = pypdf.PdfReader(ficheiro)
            texto_completo = ""
            for pagina in leitor_pdf.pages:
                texto_extraido = pagina.extract_text()
                if texto_extraido:
                    texto_completo += texto_extraido + "\n"
            
            # Salva no banco de dados se conseguiu extrair texto
            if texto_completo.strip():
                colecao_processos.add(
                    documents=[texto_completo],
                    metadatas=[{"origem": "Upload", "nome_arquivo": nome_doc}],
                    ids=[nome_doc]
                )
                documentos_adicionados += 1
        
        if documentos_adicionados > 0:
            st.success(f"✅ {documentos_adicionados} novo(s) documento(s) indexado(s) e pronto(s) para auditoria!")

st.markdown("---")

# 🔎 2. ÁREA DE INVESTIGAÇÃO (IA)
st.markdown("### 2. Motor de Inteligência")
pergunta_advogado = st.text_area(
    "Comande a IA:", 
    placeholder="Ex: Elabore um parecer apontando as contradições entre o contrato A e B.",
    height=100
)

if st.button("⚖️ Gerar Parecer Oficial", use_container_width=True):
    if pergunta_advogado:
        # Verifica se o usuário colocou algum PDF antes de perguntar
        if colecao_processos.count() == 0:
            st.warning("⚠️ O banco está vazio. Faça o upload dos PDFs primeiro.")
        else:
            with st.spinner('A redigir o documento oficial...'):
                
                # O Oráculo procura as 4 partes mais importantes dos PDFs
                resultados = colecao_processos.query(query_texts=[pergunta_advogado], n_results=4)
                
                if not resultados['documents'] or not resultados['documents'][0]:
                    st.warning("Não foi possível encontrar informações nos PDFs para essa pergunta.")
                else:
                    # Monta o dossiê para enviar ao Gemini
                    dossie_contexto = ""
                    for i in range(len(resultados['documents'][0])):
                        texto_encontrado = resultados['documents'][0][i]
                        nome_documento = resultados['metadatas'][0][i]['nome_arquivo']
                        dossie_contexto += f"\n\n--- DOCUMENTO: {nome_documento} ---\n{texto_encontrado}"

                    prompt_sistema = f"""
                    Você é o Oracle Judicial, um auditor jurídico sênior.
                    Responda com formatação impecável, pronta para ser anexada em um processo ou enviada a um cliente.
                    
                    REGRAS:
                    1. Não alucine. Baseie-se APENAS no dossiê abaixo.
                    2. Cite sempre o nome do documento fonte ao afirmar algo.
                    
                    DOSSIÊ:
                    {dossie_contexto}

                    COMANDO:
                    {pergunta_advogado}
                    """

                    try:
                        # Chama a IA atualizada para responder
                        resposta = client_gemini.models.generate_content(
                            model=MODELO_IA, 
                            contents=prompt_sistema
                        )
                        texto_final = resposta.text
                        
                        st.success("Parecer redigido com sucesso!")
                        st.markdown("### 📄 Visualização do Parecer:")
                        st.info(texto_final)
                        
                        # Botão de Exportação TXT
                        st.markdown("---")
                        st.download_button(
                            label="💾 Baixar Parecer em .TXT (Para Word/E-mail)",
                            data=texto_final,
                            file_name="Parecer_Oracle_Judicial.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Erro na comunicação com a IA: {e}")
    else:
        st.warning("⚠️ Por favor, dê um comando à IA.")