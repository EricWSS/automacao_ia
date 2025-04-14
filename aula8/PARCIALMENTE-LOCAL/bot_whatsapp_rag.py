
from webwhatsapi import WhatsAPIDriver
import time
import requests

driver = WhatsAPIDriver()
print("🔄 Escaneie o QR Code:")
print(driver.get_qr())

driver.wait_for_login()
print("✅ Bot do WhatsApp está pronto!")

while True:
    for contact in driver.get_unread():
        for message in contact.messages:
            if message.type == 'chat':
                print(f"📩 {contact.name} disse: {message.content}")

                # Envia a pergunta para a API do RAG local
                try:
                    response = requests.post("http://localhost:3000/chat", json={
                        "prompt": message.content
                    })

                    if response.status_code == 200:
                        bot_response = response.json().get("response", "⚠️ Erro na resposta do bot.")
                    else:
                        bot_response = "⚠️ A API retornou erro."

                except Exception as e:
                    bot_response = f"⚠️ Erro ao conectar à API: {str(e)}"

                # Envia resposta ao contato
                contact.chat.send_message(bot_response)
                print(f"🤖 Resposta enviada: {bot_response}")
    time.sleep(5)
