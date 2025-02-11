# Importando a biblioteca time para criar intervalos entre as mensagens
import time

# Lista de mensagens simulando uma automação
mensagens = [
    "Olá, obrigado por comprar conosco!",
    "Seu pedido foi confirmado e está sendo preparado.",
    "Em breve você receberá informações de envio. Acompanhe seu pedido pelo site."
]

# Função para enviar mensagens no terminal
def enviar_mensagens():
    print("Iniciando envio automático de mensagens...\n")
    for mensagem in mensagens:
        print(f"Enviando mensagem: {mensagem}")
        time.sleep(2)  # Simula um intervalo de 2 segundos entre as mensagens
    print("\nTodas as mensagens foram enviadas com sucesso!")

# Executando a função
enviar_mensagens()
