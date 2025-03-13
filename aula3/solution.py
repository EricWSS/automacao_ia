from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

    
# Main Script
navegador = webdriver.Chrome()
navegador.get("https://seleniumshop.vercel.app")

with open(r'D:\automacao_ia\aula3\nomes.txt', 'r') as arquivo:
    linhas = arquivo.readlines()

# Itera sobre as linhas do arquivo
for linha in linhas:
    partes = linha.strip().split(", ")
    
    try:
        nome, telefone, email, data_nascimento, rg, cpf = partes
        sleep(3)
        navegador.find_element(By.XPATH, '//*[@id="nomeCompleto"]').send_keys(nome)
        navegador.find_element(By.XPATH, '//*[@id="telefone"]').send_keys(telefone)
        navegador.find_element(By.XPATH, '//*[@id="email"]').send_keys(email)
        navegador.find_element(By.XPATH, '//*[@id="dataNascimento"]').send_keys(data_nascimento)
        navegador.find_element(By.XPATH, '//*[@id="rg"]').send_keys(rg)
        navegador.find_element(By.XPATH, '//*[@id="cpf"]').send_keys(cpf)

        sleep(3)
        navegador.find_element(By.XPATH, '//*[@id="rg"]').click()

        sleep(3)
        if not navegador.find_element(By.XPATH, '//*[@id="erro"]').text:
            navegador.find_element(By.XPATH, '//*[@id="botaoEnviar"]').click()
        else:
            with open(r"D:\automacao_ia\aula3\erros.txt", "a") as arquivoErros:
                arquivoErros.write(f"{nome}, {telefone}, {email}, {data_nascimento}, {rg}, {cpf} com problema\n")
                print(f"{nome}, {telefone}, {email}, {data_nascimento}, {rg}, {cpf} com problema\n")
                
                # Restart the browser for a new attempt
                navegador.quit()
                navegador = webdriver.Chrome()
                navegador.get("https://seleniumshop.vercel.app")


    except Exception as e:
        with open(r"D:\automacao_ia\aula3\erros.txt", "a") as arquivoErros:
            arquivoErros.write(f"Erro ao processar linha: {linha}. Erro: {e}\n")
            print(f"Erro ao processar linha: {linha}. Erro: {e}\n")

