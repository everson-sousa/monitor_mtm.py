# # import flet as ft
# # import requests
# # import time
# # from datetime import datetime
# # import threading
# # from twilio.rest import Client

# # # --- CONSTANTES DE CONFIGURAÇÃO ---
# # # URLs que serão monitoradas.
# # URLS_PARA_VERIFICAR = [
# #     "https://www.saudesuzano.com.br/api/agendamento",
# #     "https://api-ints.mobilex.tech/api/mobile/integration/AUTOAGENDAMENTOFULL",
# #     "https://httpstat.us/500",  # URL de teste para simular um erro de servidor
# #     "https://httpstat.us/404",  # URL de teste para simular 'não encontrado'
# #     "https://non-existent-url-12345.com", # URL para simular erro de conexão
# # ]

# # # Intervalo em segundos entre cada ciclo de verificação.
# # INTERVALO_DE_VERIFICACAO = 28800 # Reduzido para testes, pode ser alterado para 28800 (8 horas)

# # # --- LÓGICA DE ENVIO DE SMS ---
# # # A função agora recebe as credenciais como argumentos e as utiliza.
# # def enviar_alerta_sms(account_sid, auth_token, remetente, destinatario, mensagem_erro):
# #     """Envia um alerta por SMS usando as credenciais fornecidas."""
# #     # REMOVIDO: Credenciais hardcoded não são mais usadas.
# #     # A função agora depende dos parâmetros passados.
# #     if not all([account_sid, auth_token, remetente, destinatario]):
# #         return "SMS não enviado: Credenciais do Twilio não foram fornecidas."
        
# #     try:
# #         client = Client(account_sid, auth_token)
# #         mensagem_corpo = f"ALERTA DE MONITORAMENTO: Falha detectada. Erro: {mensagem_erro[:100]}"
        
# #         message = client.messages.create(
# #             body=mensagem_corpo,
# #             from_=remetente,
# #             to=destinatario
# #         )
# #         return f"SMS de alerta enviado para {destinatario} (SID: {message.sid})"
# #     except Exception as e:
# #         return f"ERRO ao enviar SMS: {e}"

# # # --- APLICAÇÃO FLET ---
# # def main(page: ft.Page):
# #     page.title = "Monitor de Sites com Alerta SMS"
# #     page.vertical_alignment = ft.MainAxisAlignment.START
# #     page.window_width = 800
# #     page.window_height = 700
# #     page.theme_mode = ft.ThemeMode.DARK # Adicionado para um visual mais moderno

# #     # Variável para controlar o loop de monitoramento
# #     monitoramento_ativo = threading.Event()

# #     # --- COMPONENTES DA INTERFACE ---

# #     titulo_app = ft.Text("Monitor de Sites com Alerta SMS", size=24, weight=ft.FontWeight.BOLD)

# #     txt_twilio_sid = ft.TextField(label="Twilio Account SID", password=True, can_reveal_password=True, width=380)
# #     txt_twilio_token = ft.TextField(label="Twilio Auth Token", password=True, can_reveal_password=True, width=380)
# #     txt_remetente = ft.TextField(label="Seu nº de telefone Twilio (Ex: +15017122661)", width=380)
# #     txt_destinatario = ft.TextField(label="Seu celular para receber o SMS (Ex: +5511999999999)", width=380)
    
# #     # Agrupar campos de texto para poder desabilitá-los facilmente
# #     campos_twilio = [txt_twilio_sid, txt_twilio_token, txt_remetente, txt_destinatario]

# #     log_view = ft.ListView(expand=True, spacing=10, auto_scroll=True)

# #     def adicionar_log(mensagem: str, cor: str = ft.Colors.WHITE):
# #         """Adiciona uma nova entrada de log na interface de forma segura entre threads."""
# #         now = datetime.now().strftime('%H:%M:%S')
# #         log_entry = ft.Text(f"[{now}] {mensagem}", color=cor, selectable=True)
        
# #         # Acesso seguro à interface a partir de outra thread
# #         log_view.controls.append(log_entry)
# #         page.update()

# #     # --- LÓGICA DE MONITORAMENTO (em uma thread separada) ---
# #     def loop_de_monitoramento():
# #         """Função que roda em loop para verificar as URLs."""
# #         # Acessa os valores dos campos de texto UMA VEZ no início da thread
# #         # para garantir que sejam consistentes durante o ciclo.
# #         sid = txt_twilio_sid.value
# #         token = txt_twilio_token.value
# #         remetente = txt_remetente.value
# #         destinatario = txt_destinatario.value

# #         adicionar_log("Thread de monitoramento iniciada.", ft.Colors.BLUE_200)
        
# #         while monitoramento_ativo.is_set():
# #             adicionar_log(f"Iniciando novo ciclo de verificação para {len(URLS_PARA_VERIFICAR)} URLs.", ft.Colors.CYAN_200)
            
# #             for url in URLS_PARA_VERIFICAR:
# #                 if not monitoramento_ativo.is_set(): # Checagem extra para parar mais rápido
# #                     break
# #                 try:
# #                     response = requests.get(url, timeout=10)
# #                     if response.status_code >= 400:
# #                         erro = f"URL '{url}' respondeu com erro: {response.status_code}"
# #                         adicionar_log(erro, ft.Colors.ORANGE)
                        
# #                         resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
# #                         adicionar_log(resultado_sms, ft.Colors.YELLOW_200)
# #                     else:
# #                         adicionar_log(f"URL '{url}' está ONLINE ({response.status_code}).", ft.Colors.GREEN_300)

# #                 except requests.exceptions.RequestException as e:
# #                     erro = f"Falha de conexão na URL '{url}': {type(e).__name__}"
# #                     adicionar_log(erro, ft.Colors.RED_ACCENT)

# #                     resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
# #                     adicionar_log(resultado_sms, ft.Colors.YELLOW_200)
            
# #             if not monitoramento_ativo.is_set(): # Checagem final para sair do loop
# #                 break

# #             # CORREÇÃO: A espera agora ocorre DEPOIS de verificar TODAS as URLs.
# #             adicionar_log(f"Ciclo finalizado. Aguardando {INTERVALO_DE_VERIFICACAO} segundos...", ft.Colors.GREY_500)
# #             # A função `wait` do Evento permite que o loop seja interrompido imediatamente
# #             # se o evento for limpo (pelo botão parar), em vez de esperar o `sleep` terminar.
# #             monitoramento_ativo.wait(INTERVALO_DE_VERIFICACAO)
        
# #         adicionar_log("Thread de monitoramento finalizada.", ft.Colors.BLUE_200)

# #     # --- FUNÇÕES DOS BOTÕES ---
# #     def alternar_campos_edicao(disabled: bool):
# #         """Habilita ou desabilita os campos de texto do Twilio."""
# #         for campo in campos_twilio:
# #             campo.disabled = disabled
# #         page.update()

# #     def iniciar_monitoramento(e):
# #         if not all([campo.value for campo in campos_twilio]):
# #             # CORREÇÃO: Usando a nova sintaxe do Flet para cores.
# #             adicionar_log("ERRO: Preencha todos os campos do Twilio antes de iniciar.", ft.Colors.RED)
# #             return

# #         btn_iniciar.disabled = True
# #         btn_parar.disabled = False
# #         alternar_campos_edicao(disabled=True)
# #         monitoramento_ativo.set()
        
# #         thread = threading.Thread(target=loop_de_monitoramento, daemon=True)
# #         thread.start()
        
# #         adicionar_log("Monitoramento INICIADO.", ft.Colors.CYAN)
# #         page.update()

# #     def parar_monitoramento(e):
# #         btn_iniciar.disabled = False
# #         btn_parar.disabled = True
# #         alternar_campos_edicao(disabled=False)
        
# #         # Sinaliza para a thread parar. O uso de `event.wait()` no loop garante
# #         # uma parada mais responsiva.
# #         monitoramento_ativo.clear() 
# #         adicionar_log("Monitoramento PARANDO... O ciclo atual será finalizado.", ft.Colors.ORANGE_300)
# #         page.update()

# #     # Botões
# #     btn_iniciar = ft.ElevatedButton("Iniciar", on_click=iniciar_monitoramento, icon=ft.Icons.PLAY_ARROW)
# #     btn_parar = ft.ElevatedButton("Parar", on_click=parar_monitoramento, icon=ft.Icons.STOP, disabled=True)
    
# #     # --- MONTAGEM DA PÁGINA ---
# #     # CORREÇÃO: Atualizando ft.border e ft.border_radius
# #     page.add(
# #         ft.Column([
# #             titulo_app,
# #             ft.Text("Insira suas credenciais do Twilio para receber alertas por SMS."),
# #             ft.Row([txt_twilio_sid, txt_remetente], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
# #             ft.Row([txt_twilio_token, txt_destinatario], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
# #             ft.Row([btn_iniciar, btn_parar]),
# #             ft.Divider(),
# #             ft.Text("Logs em Tempo Real:", weight=ft.FontWeight.BOLD),
# #             ft.Container(
# #                 content=log_view,
# #                 border=ft.border.all(1, ft.Colors.BLUE_GREY_700),
# #                 border_radius=ft.border_radius.all(5),
# #                 padding=10,
# #                 expand=True
# #             )
# #         ], expand=True, spacing=15)
# #     )

# # if __name__ == "__main__":
# #     ft.app(target=main)

# import flet as ft
# import requests
# import time
# from datetime import datetime
# import threading
# from twilio.rest import Client
# import logging # NOVO: Importa a biblioteca de logging
# import os      # NOVO: Para criar diretórios

# # --- CONSTANTES DE CONFIGURAÇÃO ---
# URLS_PARA_VERIFICAR = [
#     "https://www.saudesuzano.com.br/api/agendamento",
#     "https://api-ints.mobilex.tech/api/mobile/integration/AUTOAGENDAMENTOFULL",
#     "https://httpstat.us/500",
#     "https://httpstat.us/404",
#     "https://non-existent-url-12345.com",
# ]
# INTERVALO_DE_VERIFICACAO = 28800 # 8 horas

# # --- NOVO: CONFIGURAÇÃO DO SISTEMA DE LOGS ---
# def setup_logging():
#     """Cria a pasta 'logs' e configura o logger para salvar em arquivos diários."""
#     log_dir = "logs"
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
    
#     # Gera um nome de arquivo de log com a data atual
#     log_filename = os.path.join(log_dir, f"monitor_{datetime.now().strftime('%Y-%m-%d')}.log")
    
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         handlers=[
#             logging.FileHandler(log_filename, encoding='utf-8'),
#             # Se quiser ver os logs no console onde o script roda, descomente a linha abaixo
#             # logging.StreamHandler() 
#         ]
#     )

# # --- LÓGICA DE ENVIO DE SMS ---
# def enviar_alerta_sms(account_sid, auth_token, remetente, destinatario, mensagem_erro):
#     if not all([account_sid, auth_token, remetente, destinatario]):
#         return "SMS não enviado: Credenciais do Twilio não foram fornecidas."
#     try:
#         client = Client(account_sid, auth_token)
#         mensagem_corpo = f"ALERTA DE MONITORAMENTO: Falha detectada. Erro: {mensagem_erro[:100]}"
#         message = client.messages.create(body=mensagem_corpo, from_=remetente, to=destinatario)
#         return f"SMS de alerta enviado para {destinatario} (SID: {message.sid})"
#     except Exception as e:
#         # ALTERADO: Loga o erro detalhado no arquivo
#         logging.error(f"Falha CRÍTICA ao tentar enviar SMS: {e}")
#         return f"ERRO ao enviar SMS: {e}"

# # --- APLICAÇÃO FLET ---
# def main(page: ft.Page):
#     # NOVO: Chama a função de configuração de logs no início
#     setup_logging()

#     page.title = "Monitor de Sites com Alerta SMS"
#     page.vertical_alignment = ft.MainAxisAlignment.START
#     page.window_width = 800
#     page.window_height = 700
#     page.theme_mode = ft.ThemeMode.DARK

#     monitoramento_ativo = threading.Event()

#     # ... (Restante dos componentes da interface permanece o mesmo) ...
#     titulo_app = ft.Text("Monitor de Sites com Alerta SMS", size=24, weight=ft.FontWeight.BOLD)
#     txt_twilio_sid = ft.TextField(label="Twilio Account SID", password=True, can_reveal_password=True, width=380)
#     txt_twilio_token = ft.TextField(label="Twilio Auth Token", password=True, can_reveal_password=True, width=380)
#     txt_remetente = ft.TextField(label="Seu nº de telefone Twilio (Ex: +15017122661)", width=380)
#     txt_destinatario = ft.TextField(label="Seu celular para receber o SMS (Ex: +5511999999999)", width=380)
#     campos_twilio = [txt_twilio_sid, txt_twilio_token, txt_remetente, txt_destinatario]
#     log_view = ft.ListView(expand=True, spacing=10, auto_scroll=True)

#     # --- ALTERADO: Função de log agora salva em arquivo e na UI ---
#     def log_and_display(mensagem: str, nivel: str, cor_ui: str):
#         """
#         Registra a mensagem no arquivo de log e a exibe na interface do usuário.
#         Níveis: 'INFO', 'WARNING', 'ERROR'
#         """
#         # 1. Grava no arquivo de log
#         if nivel.upper() == 'INFO':
#             logging.info(mensagem)
#         elif nivel.upper() == 'WARNING':
#             logging.warning(mensagem)
#         elif nivel.upper() == 'ERROR':
#             logging.error(mensagem)
        
#         # 2. Exibe na interface do Flet
#         now = datetime.now().strftime('%H:%M:%S')
#         log_entry = ft.Text(f"[{now}] {mensagem}", color=cor_ui, selectable=True)
#         log_view.controls.append(log_entry)
        
#         # O page.update() precisa ser chamado a partir da função que invoca o log
#         # para garantir que seja executado no contexto correto da UI.

#     # --- LÓGICA DE MONITORAMENTO (Adaptada para usar o novo sistema de log) ---
#     def loop_de_monitoramento():
#         sid = txt_twilio_sid.value
#         token = txt_twilio_token.value
#         remetente = txt_remetente.value
#         destinatario = txt_destinatario.value

#         log_and_display("Thread de monitoramento iniciada.", "INFO", ft.Colors.BLUE_200)
        
#         while monitoramento_ativo.is_set():
#             log_and_display(f"Iniciando novo ciclo de verificação para {len(URLS_PARA_VERIFICAR)} URLs.", "INFO", ft.Colors.CYAN_200)
            
#             for url in URLS_PARA_VERIFICAR:
#                 if not monitoramento_ativo.is_set(): break
#                 try:
#                     response = requests.get(url, timeout=10)
#                     if response.status_code >= 400:
#                         erro = f"URL '{url}' respondeu com erro: {response.status_code}"
#                         log_and_display(erro, "WARNING", ft.Colors.ORANGE)
                        
#                         resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
#                         log_and_display(resultado_sms, "INFO", ft.Colors.YELLOW_200)
#                     else:
#                         log_and_display(f"URL '{url}' está ONLINE ({response.status_code}).", "INFO", ft.Colors.GREEN_300)

#                 except requests.exceptions.RequestException as e:
#                     erro = f"Falha de conexão na URL '{url}': {type(e).__name__}"
#                     log_and_display(erro, "ERROR", ft.Colors.RED_ACCENT)

#                     resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
#                     log_and_display(resultado_sms, "INFO", ft.Colors.YELLOW_200)
            
#             page.update() # Atualiza a UI após cada ciclo de verificação
#             if not monitoramento_ativo.is_set(): break

#             log_and_display(f"Ciclo finalizado. Aguardando {int(INTERVALO_DE_VERIFICACAO / 3600)} horas...", "INFO", ft.Colors.GREY_500)
#             page.update()
#             monitoramento_ativo.wait(INTERVALO_DE_VERIFICACAO)
        
#         log_and_display("Thread de monitoramento finalizada.", "INFO", ft.Colors.BLUE_200)
#         page.update()

#     # ... (Restante do código, como as funções de botão, permanece praticamente o mesmo) ...
#     def alternar_campos_edicao(disabled: bool):
#         for campo in campos_twilio: campo.disabled = disabled
    
#     def iniciar_monitoramento(e):
#         if not all([campo.value for campo in campos_twilio]):
#             log_and_display("ERRO: Preencha todos os campos do Twilio antes de iniciar.", "ERROR", ft.Colors.RED)
#             page.update()
#             return

#         btn_iniciar.disabled = True
#         btn_parar.disabled = False
#         alternar_campos_edicao(disabled=True)
#         monitoramento_ativo.set()
        
#         thread = threading.Thread(target=loop_de_monitoramento, daemon=True)
#         thread.start()
        
#         log_and_display("Monitoramento INICIADO.", "INFO", ft.Colors.CYAN)
#         page.update()

#     def parar_monitoramento(e):
#         btn_iniciar.disabled = False
#         btn_parar.disabled = True
#         alternar_campos_edicao(disabled=False)
#         monitoramento_ativo.clear() 
#         log_and_display("Monitoramento PARANDO... O ciclo atual será finalizado.", "WARNING", ft.Colors.ORANGE_300)
#         page.update()
        
#     btn_iniciar = ft.ElevatedButton("Iniciar", on_click=iniciar_monitoramento, icon=ft.Icons.PLAY_ARROW)
#     btn_parar = ft.ElevatedButton("Parar", on_click=parar_monitoramento, icon=ft.Icons.STOP, disabled=True)
    
#     page.add(
#         ft.Column([
#             titulo_app,
#             ft.Text("Insira suas credenciais do Twilio para receber alertas por SMS."),
#             ft.Row([txt_twilio_sid, txt_remetente], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#             ft.Row([txt_twilio_token, txt_destinatario], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#             ft.Row([btn_iniciar, btn_parar]),
#             ft.Divider(), ft.Text("Logs em Tempo Real:", weight=ft.FontWeight.BOLD),
#             ft.Container(content=log_view, border=ft.border.all(1, ft.Colors.BLUE_GREY_700), border_radius=ft.border_radius.all(5), padding=10, expand=True)
#         ], expand=True, spacing=15)
#     )

# if __name__ == "__main__":
#     ft.app(target=main)

# import flet as ft
# import requests
# import time
# from datetime import datetime
# import threading
# from twilio.rest import Client

# # --- CONSTANTES DE CONFIGURAÇÃO ---
# # URLs que serão monitoradas.
# URLS_PARA_VERIFICAR = [
#     "https://www.saudesuzano.com.br/api/agendamento",
#     "https://api-ints.mobilex.tech/api/mobile/integration/AUTOAGENDAMENTOFULL",
#     "https://httpstat.us/500",  # URL de teste para simular um erro de servidor
#     "https://httpstat.us/404",  # URL de teste para simular 'não encontrado'
#     "https://non-existent-url-12345.com", # URL para simular erro de conexão
# ]

# # Intervalo em segundos entre cada ciclo de verificação.
# INTERVALO_DE_VERIFICACAO = 28800 # Reduzido para testes, pode ser alterado para 28800 (8 horas)

# # --- LÓGICA DE ENVIO DE SMS ---
# # A função agora recebe as credenciais como argumentos e as utiliza.
# def enviar_alerta_sms(account_sid, auth_token, remetente, destinatario, mensagem_erro):
#     """Envia um alerta por SMS usando as credenciais fornecidas."""
#     # REMOVIDO: Credenciais hardcoded não são mais usadas.
#     # A função agora depende dos parâmetros passados.
#     if not all([account_sid, auth_token, remetente, destinatario]):
#         return "SMS não enviado: Credenciais do Twilio não foram fornecidas."
        
#     try:
#         client = Client(account_sid, auth_token)
#         mensagem_corpo = f"ALERTA DE MONITORAMENTO: Falha detectada. Erro: {mensagem_erro[:100]}"
        
#         message = client.messages.create(
#             body=mensagem_corpo,
#             from_=remetente,
#             to=destinatario
#         )
#         return f"SMS de alerta enviado para {destinatario} (SID: {message.sid})"
#     except Exception as e:
#         return f"ERRO ao enviar SMS: {e}"

# # --- APLICAÇÃO FLET ---
# def main(page: ft.Page):
#     page.title = "Monitor de Sites com Alerta SMS"
#     page.vertical_alignment = ft.MainAxisAlignment.START
#     page.window_width = 800
#     page.window_height = 700
#     page.theme_mode = ft.ThemeMode.DARK # Adicionado para um visual mais moderno

#     # Variável para controlar o loop de monitoramento
#     monitoramento_ativo = threading.Event()

#     # --- COMPONENTES DA INTERFACE ---

#     titulo_app = ft.Text("Monitor de Sites com Alerta SMS", size=24, weight=ft.FontWeight.BOLD)

#     txt_twilio_sid = ft.TextField(label="Twilio Account SID", password=True, can_reveal_password=True, width=380)
#     txt_twilio_token = ft.TextField(label="Twilio Auth Token", password=True, can_reveal_password=True, width=380)
#     txt_remetente = ft.TextField(label="Seu nº de telefone Twilio (Ex: +15017122661)", width=380)
#     txt_destinatario = ft.TextField(label="Seu celular para receber o SMS (Ex: +5511999999999)", width=380)
    
#     # Agrupar campos de texto para poder desabilitá-los facilmente
#     campos_twilio = [txt_twilio_sid, txt_twilio_token, txt_remetente, txt_destinatario]

#     log_view = ft.ListView(expand=True, spacing=10, auto_scroll=True)

#     def adicionar_log(mensagem: str, cor: str = ft.Colors.WHITE):
#         """Adiciona uma nova entrada de log na interface de forma segura entre threads."""
#         now = datetime.now().strftime('%H:%M:%S')
#         log_entry = ft.Text(f"[{now}] {mensagem}", color=cor, selectable=True)
        
#         # Acesso seguro à interface a partir de outra thread
#         log_view.controls.append(log_entry)
#         page.update()

#     # --- LÓGICA DE MONITORAMENTO (em uma thread separada) ---
#     def loop_de_monitoramento():
#         """Função que roda em loop para verificar as URLs."""
#         # Acessa os valores dos campos de texto UMA VEZ no início da thread
#         # para garantir que sejam consistentes durante o ciclo.
#         sid = txt_twilio_sid.value
#         token = txt_twilio_token.value
#         remetente = txt_remetente.value
#         destinatario = txt_destinatario.value

#         adicionar_log("Thread de monitoramento iniciada.", ft.Colors.BLUE_200)
        
#         while monitoramento_ativo.is_set():
#             adicionar_log(f"Iniciando novo ciclo de verificação para {len(URLS_PARA_VERIFICAR)} URLs.", ft.Colors.CYAN_200)
            
#             for url in URLS_PARA_VERIFICAR:
#                 if not monitoramento_ativo.is_set(): # Checagem extra para parar mais rápido
#                     break
#                 try:
#                     response = requests.get(url, timeout=10)
#                     if response.status_code >= 400:
#                         erro = f"URL '{url}' respondeu com erro: {response.status_code}"
#                         adicionar_log(erro, ft.Colors.ORANGE)
                        
#                         resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
#                         adicionar_log(resultado_sms, ft.Colors.YELLOW_200)
#                     else:
#                         adicionar_log(f"URL '{url}' está ONLINE ({response.status_code}).", ft.Colors.GREEN_300)

#                 except requests.exceptions.RequestException as e:
#                     erro = f"Falha de conexão na URL '{url}': {type(e).__name__}"
#                     adicionar_log(erro, ft.Colors.RED_ACCENT)

#                     resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
#                     adicionar_log(resultado_sms, ft.Colors.YELLOW_200)
            
#             if not monitoramento_ativo.is_set(): # Checagem final para sair do loop
#                 break

#             # CORREÇÃO: A espera agora ocorre DEPOIS de verificar TODAS as URLs.
#             adicionar_log(f"Ciclo finalizado. Aguardando {INTERVALO_DE_VERIFICACAO} segundos...", ft.Colors.GREY_500)
#             # A função `wait` do Evento permite que o loop seja interrompido imediatamente
#             # se o evento for limpo (pelo botão parar), em vez de esperar o `sleep` terminar.
#             monitoramento_ativo.wait(INTERVALO_DE_VERIFICACAO)
        
#         adicionar_log("Thread de monitoramento finalizada.", ft.Colors.BLUE_200)

#     # --- FUNÇÕES DOS BOTÕES ---
#     def alternar_campos_edicao(disabled: bool):
#         """Habilita ou desabilita os campos de texto do Twilio."""
#         for campo in campos_twilio:
#             campo.disabled = disabled
#         page.update()

#     def iniciar_monitoramento(e):
#         if not all([campo.value for campo in campos_twilio]):
#             # CORREÇÃO: Usando a nova sintaxe do Flet para cores.
#             adicionar_log("ERRO: Preencha todos os campos do Twilio antes de iniciar.", ft.Colors.RED)
#             return

#         btn_iniciar.disabled = True
#         btn_parar.disabled = False
#         alternar_campos_edicao(disabled=True)
#         monitoramento_ativo.set()
        
#         thread = threading.Thread(target=loop_de_monitoramento, daemon=True)
#         thread.start()
        
#         adicionar_log("Monitoramento INICIADO.", ft.Colors.CYAN)
#         page.update()

#     def parar_monitoramento(e):
#         btn_iniciar.disabled = False
#         btn_parar.disabled = True
#         alternar_campos_edicao(disabled=False)
        
#         # Sinaliza para a thread parar. O uso de `event.wait()` no loop garante
#         # uma parada mais responsiva.
#         monitoramento_ativo.clear() 
#         adicionar_log("Monitoramento PARANDO... O ciclo atual será finalizado.", ft.Colors.ORANGE_300)
#         page.update()

#     # Botões
#     btn_iniciar = ft.ElevatedButton("Iniciar", on_click=iniciar_monitoramento, icon=ft.Icons.PLAY_ARROW)
#     btn_parar = ft.ElevatedButton("Parar", on_click=parar_monitoramento, icon=ft.Icons.STOP, disabled=True)
    
#     # --- MONTAGEM DA PÁGINA ---
#     # CORREÇÃO: Atualizando ft.border e ft.border_radius
#     page.add(
#         ft.Column([
#             titulo_app,
#             ft.Text("Insira suas credenciais do Twilio para receber alertas por SMS."),
#             ft.Row([txt_twilio_sid, txt_remetente], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#             ft.Row([txt_twilio_token, txt_destinatario], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#             ft.Row([btn_iniciar, btn_parar]),
#             ft.Divider(),
#             ft.Text("Logs em Tempo Real:", weight=ft.FontWeight.BOLD),
#             ft.Container(
#                 content=log_view,
#                 border=ft.border.all(1, ft.Colors.BLUE_GREY_700),
#                 border_radius=ft.border_radius.all(5),
#                 padding=10,
#                 expand=True
#             )
#         ], expand=True, spacing=15)
#     )

# if __name__ == "__main__":
#     ft.app(target=main)

import flet as ft
import requests
import time
from datetime import datetime
import threading
from twilio.rest import Client
import logging # NOVO: Importa a biblioteca de logging
import os      # NOVO: Para criar diretórios

# --- CONSTANTES DE CONFIGURAÇÃO ---
URLS_PARA_VERIFICAR = [
    "https://www.saudesuzano.com.br/api/agendamento",
    "https://api-ints.mobilex.tech/api/mobile/integration/AUTOAGENDAMENTOFULL",
    "https://httpstat.us/500",
    "https://httpstat.us/404",
    "https://non-existent-url-12345.com",
]
INTERVALO_DE_VERIFICACAO = 28800 # 8 horas

# --- NOVO: CONFIGURAÇÃO DO SISTEMA DE LOGS ---
def setup_logging():
    """Cria a pasta 'logs' e configura o logger para salvar em arquivos diários."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Gera um nome de arquivo de log com a data atual
    log_filename = os.path.join(log_dir, f"monitor_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            # Se quiser ver os logs no console onde o script roda, descomente a linha abaixo
            # logging.StreamHandler() 
        ]
    )

# --- LÓGICA DE ENVIO DE SMS ---
def enviar_alerta_sms(account_sid, auth_token, remetente, destinatario, mensagem_erro):
    if not all([account_sid, auth_token, remetente, destinatario]):
        return "SMS não enviado: Credenciais do Twilio não foram fornecidas."
    try:
        client = Client(account_sid, auth_token)
        mensagem_corpo = f"ALERTA DE MONITORAMENTO: Falha detectada. Erro: {mensagem_erro[:100]}"
        message = client.messages.create(body=mensagem_corpo, from_=remetente, to=destinatario)
        return f"SMS de alerta enviado para {destinatario} (SID: {message.sid})"
    except Exception as e:
        # ALTERADO: Loga o erro detalhado no arquivo
        logging.error(f"Falha CRÍTICA ao tentar enviar SMS: {e}")
        return f"ERRO ao enviar SMS: {e}"

# --- APLICAÇÃO FLET ---
def main(page: ft.Page):
    # NOVO: Chama a função de configuração de logs no início
    setup_logging()

    page.title = "Monitor de Sites com Alerta SMS"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 800
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK

    monitoramento_ativo = threading.Event()

    # ... (Restante dos componentes da interface permanece o mesmo) ...
    titulo_app = ft.Text("Monitor de Sites com Alerta SMS", size=24, weight=ft.FontWeight.BOLD)
    txt_twilio_sid = ft.TextField(label="Twilio Account SID", password=True, can_reveal_password=True, width=380)
    txt_twilio_token = ft.TextField(label="Twilio Auth Token", password=True, can_reveal_password=True, width=380)
    txt_remetente = ft.TextField(label="Seu nº de telefone Twilio (Ex: +15017122661)", width=380)
    txt_destinatario = ft.TextField(label="Seu celular para receber o SMS (Ex: +5511999999999)", width=380)
    campos_twilio = [txt_twilio_sid, txt_twilio_token, txt_remetente, txt_destinatario]
    log_view = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # --- ALTERADO: Função de log agora salva em arquivo e na UI ---
    def log_and_display(mensagem: str, nivel: str, cor_ui: str):
        """
        Registra a mensagem no arquivo de log e a exibe na interface do usuário.
        Níveis: 'INFO', 'WARNING', 'ERROR'
        """
        # 1. Grava no arquivo de log
        if nivel.upper() == 'INFO':
            logging.info(mensagem)
        elif nivel.upper() == 'WARNING':
            logging.warning(mensagem)
        elif nivel.upper() == 'ERROR':
            logging.error(mensagem)
        
        # 2. Exibe na interface do Flet
        now = datetime.now().strftime('%H:%M:%S')
        log_entry = ft.Text(f"[{now}] {mensagem}", color=cor_ui, selectable=True)
        log_view.controls.append(log_entry)
        
        # O page.update() precisa ser chamado a partir da função que invoca o log
        # para garantir que seja executado no contexto correto da UI.

    # --- LÓGICA DE MONITORAMENTO (Adaptada para usar o novo sistema de log) ---
    def loop_de_monitoramento():
        sid = txt_twilio_sid.value
        token = txt_twilio_token.value
        remetente = txt_remetente.value
        destinatario = txt_destinatario.value

        log_and_display("Thread de monitoramento iniciada.", "INFO", ft.Colors.BLUE_200)
        
        while monitoramento_ativo.is_set():
            log_and_display(f"Iniciando novo ciclo de verificação para {len(URLS_PARA_VERIFICAR)} URLs.", "INFO", ft.Colors.CYAN_200)
            
            for url in URLS_PARA_VERIFICAR:
                if not monitoramento_ativo.is_set(): break
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code >= 400:
                        erro = f"URL '{url}' respondeu com erro: {response.status_code}"
                        log_and_display(erro, "WARNING", ft.Colors.ORANGE)
                        
                        resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
                        log_and_display(resultado_sms, "INFO", ft.Colors.YELLOW_200)
                    else:
                        log_and_display(f"URL '{url}' está ONLINE ({response.status_code}).", "INFO", ft.Colors.GREEN_300)

                except requests.exceptions.RequestException as e:
                    erro = f"Falha de conexão na URL '{url}': {type(e).__name__}"
                    log_and_display(erro, "ERROR", ft.Colors.RED_ACCENT)

                    resultado_sms = enviar_alerta_sms(sid, token, remetente, destinatario, erro)
                    log_and_display(resultado_sms, "INFO", ft.Colors.YELLOW_200)
            
            page.update() # Atualiza a UI após cada ciclo de verificação
            if not monitoramento_ativo.is_set(): break

            log_and_display(f"Ciclo finalizado. Aguardando {int(INTERVALO_DE_VERIFICACAO / 3600)} horas...", "INFO", ft.Colors.GREY_500)
            page.update()
            monitoramento_ativo.wait(INTERVALO_DE_VERIFICACAO)
        
        log_and_display("Thread de monitoramento finalizada.", "INFO", ft.Colors.BLUE_200)
        page.update()

    # ... (Restante do código, como as funções de botão, permanece praticamente o mesmo) ...
    def alternar_campos_edicao(disabled: bool):
        for campo in campos_twilio: campo.disabled = disabled
    
    def iniciar_monitoramento(e):
        if not all([campo.value for campo in campos_twilio]):
            log_and_display("ERRO: Preencha todos os campos do Twilio antes de iniciar.", "ERROR", ft.Colors.RED)
            page.update()
            return

        btn_iniciar.disabled = True
        btn_parar.disabled = False
        alternar_campos_edicao(disabled=True)
        monitoramento_ativo.set()
        
        thread = threading.Thread(target=loop_de_monitoramento, daemon=True)
        thread.start()
        
        log_and_display("Monitoramento INICIADO.", "INFO", ft.Colors.CYAN)
        page.update()

    def parar_monitoramento(e):
        btn_iniciar.disabled = False
        btn_parar.disabled = True
        alternar_campos_edicao(disabled=False)
        monitoramento_ativo.clear() 
        log_and_display("Monitoramento PARANDO... O ciclo atual será finalizado.", "WARNING", ft.Colors.ORANGE_300)
        page.update()
        
    btn_iniciar = ft.ElevatedButton("Iniciar", on_click=iniciar_monitoramento, icon=ft.Icons.PLAY_ARROW)
    btn_parar = ft.ElevatedButton("Parar", on_click=parar_monitoramento, icon=ft.Icons.STOP, disabled=True)
    
    page.add(
        ft.Column([
            titulo_app,
            ft.Text("Insira suas credenciais do Twilio para receber alertas por SMS."),
            ft.Row([txt_twilio_sid, txt_remetente], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([txt_twilio_token, txt_destinatario], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([btn_iniciar, btn_parar]),
            ft.Divider(), ft.Text("Logs em Tempo Real:", weight=ft.FontWeight.BOLD),
            ft.Container(content=log_view, border=ft.border.all(1, ft.Colors.BLUE_GREY_700), border_radius=ft.border_radius.all(5), padding=10, expand=True)
        ], expand=True, spacing=15)
    )

if __name__ == "__main__":
    ft.app(target=main)