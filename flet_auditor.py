import flet as ft
import google.generativeai as genai
import PyPDF2
import subprocess # A nossa nova arma secreta!

# ==========================================
# 1. CONFIGURAÇÃO DA IA
# ==========================================
CHAVE_API = "SUA_CHAVE_API_AQUI" 
genai.configure(api_key=CHAVE_API)
modelo = genai.GenerativeModel('gemini-2.5-flash') 

def main(page: ft.Page):
    # ==========================================
    # 2. CONFIGURAÇÕES VISUAIS DA JANELA (UX)
    # ==========================================
    page.title = "Auditor Jurídico AI"
    page.theme_mode = "light" 
    page.bgcolor = "#F8FAFC" 
    page.window_width = 800
    page.window_height = 900
    page.padding = 40 
    page.scroll = "auto"

    texto_contrato = [""]
    resultado_ia = [""]

    # ==========================================
    # 3. UPLOAD E DOWNLOAD NATIVOS DO MAC (APPLE SCRIPT)
    # ==========================================
    def on_upload(e):
        try:
            # Chama a janela de ficheiros nativa do Mac!
            script = 'POSIX path of (choose file with prompt "Selecione o Contrato em PDF" of type {"pdf"})'
            resultado = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            
            if resultado.returncode == 0: # Se o utilizador escolheu um ficheiro
                caminho_ficheiro = resultado.stdout.strip()
                nome_ficheiro = caminho_ficheiro.split('/')[-1]
                
                nome_arquivo_texto.value = f"📄 Ficheiro carregado: {nome_ficheiro}"
                nome_arquivo_texto.color = "#0F172A"
                
                with open(caminho_ficheiro, 'rb') as f:
                    leitor = PyPDF2.PdfReader(f)
                    texto_extraido = ""
                    for p in leitor.pages:
                        texto_extraido += p.extract_text() + "\n"
                
                texto_contrato[0] = texto_extraido
                status_texto.value = "✅ PDF lido com sucesso! Clique em Executar Auditoria."
                status_texto.color = "#15803D" 
                botao_auditar.disabled = False 
                botao_auditar.bgcolor = "#1E3A8A" 
                
        except Exception as ex:
            status_texto.value = "❌ Erro ao ler PDF. Tente novamente."
            status_texto.color = "#B91C1C" 
            
        page.update()

    def on_download(e):
        try:
            # Chama a janela de guardar nativa do Mac
            script = 'POSIX path of (choose file name with prompt "Guardar Relatório de Auditoria" default name "Relatorio_Auditoria.txt")'
            resultado = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                caminho_salvar = resultado.stdout.strip()
                with open(caminho_salvar, 'w', encoding='utf-8') as f:
                    f.write(resultado_ia[0])
                status_texto.value = f"💾 Relatório guardado em: {caminho_salvar.split('/')[-1]}"
                status_texto.color = "#15803D"
        except Exception as ex:
            pass
            
        page.update()

    # ==========================================
    # 4. A LÓGICA DA AUDITORIA
    # ==========================================
    def auditar_contrato(e):
        if not texto_contrato[0]:
            return 
            
        area_resultado.value = "⏳ *A analisar cláusulas, jurisprudência e armadilhas legais. Por favor, aguarde...*"
        botao_download.visible = False
        page.update()
        
        try:
            prompt = f"""
            Você é um advogado sênior e auditor rigoroso. 
            Analise o contrato abaixo, aponte os 3 principais riscos para quem assina 
            e sugira melhorias. Seja direto, profissional e separe em tópicos claros. Você é o Auditor Jurídico PRO, um auditor jurídico de elite. "
        "Sua análise deve ser cirúrgica. Estruture com: RESUMO EXECUTIVO, PONTOS CRÍTICOS e SUGESTÃO ESTRATÉGICA. "
        "Use negrito para destacar valores e nomes. Mantenha sobriedade máxima.
            
            CONTRATO:
            {texto_contrato[0]}
            """
            
            resposta = modelo.generate_content(prompt)
            resultado_ia[0] = resposta.text
            area_resultado.value = resposta.text
            
            botao_download.visible = True 
            status_texto.value = "✨ Análise concluída com sucesso! Descarregue o seu relatório."
            
        except Exception as erro:
            area_resultado.value = f"❌ **Falha na comunicação com a IA:** {erro}"
            
        page.update()

    # ==========================================
    # 5. CONSTRUINDO A INTERFACE (CARDS E UX)
    # ==========================================
    cabecalho = ft.Text("Auditor Jurídico AI", size=32, weight="bold", color="#0F172A")
    
    card_instrucoes = ft.Container(
        content=ft.Column([
            ft.Text("Como funciona:", weight="bold", size=18, color="#0F172A"),
            ft.Text("1. Clique no botão de Anexar e selecione o contrato em PDF.", color="#334155", size=15),
            ft.Text("2. A Inteligência Artificial irá cruzar os dados com a legislação vigente.", color="#334155", size=15),
            ft.Text("3. Descarregue um relatório a apontar riscos ocultos e sugestões de melhoria.", color="#334155", size=15),
        ]),
        bgcolor="white", padding=25, border_radius=10, 
        border=ft.border.all(1, "#CBD5E1")
    )

    nome_arquivo_texto = ft.Text("Nenhum ficheiro selecionado.", color="#64748B", italic=True, size=15)
    status_texto = ft.Text("", weight="bold", size=15)
    
    botao_upload = ft.Container(
        content=ft.Text("📂 Anexar PDF", color="#0F172A", weight="bold", size=16),
        bgcolor="#E2E8F0", padding=15,
        border_radius=8, on_click=on_upload, ink=True
    )

    botao_auditar = ft.Container(
        content=ft.Text("⚖️ Executar Auditoria", color="white", weight="bold", size=16),
        bgcolor="#94A3B8", padding=15,
        border_radius=8, on_click=auditar_contrato, disabled=True, ink=True
    )
    
    botao_download = ft.Container(
        content=ft.Text("💾 Guardar Relatório", color="white", weight="bold", size=16),
        bgcolor="#15803D", padding=15,
        border_radius=8, on_click=on_download,
        ink=True, visible=False 
    )

    linha_botoes = ft.Row([botao_upload, botao_auditar, botao_download], alignment="start")

    card_acoes = ft.Container(
        content=ft.Column([nome_arquivo_texto, linha_botoes, status_texto]),
        bgcolor="white", padding=25, border_radius=10, 
        border=ft.border.all(1, "#CBD5E1")
    )

    area_resultado = ft.Markdown("A análise aparecerá aqui...", selectable=True)
    
    card_resultado = ft.Container(
        content=area_resultado,
        bgcolor="white", padding=25, border_radius=10,
        border=ft.border.all(1, "#CBD5E1"), expand=True 
    )

    page.add(
        cabecalho,
        ft.Divider(height=10, color="transparent"),
        card_instrucoes,
        card_acoes,
        ft.Text("Resultado da Análise:", size=20, weight="bold", color="#0F172A"),
        card_resultado
    )

ft.app(target=main)
