# Importando bibliotecas necessárias
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Dados de exemplo
mensagens = ["Promoção imperdível, clique aqui!", #1
             "Oi, tudo bem?", #2
             "Ganhe dinheiro rápido, sem esforço!", #3
             "Sua conta foi atualizada com sucesso.",#4
             "Você ganhou um prêmio, clique aqui!"]#5

rotulos = ["spam", #1
           "não spam",  #2
           "spam", #3
           "não spam",  #4
           'spam']  # Rótulos das mensagens

# Convertendo texto para números
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(mensagens)

# Criando o modelo
modelo = MultinomialNB()
modelo.fit(X, rotulos)

# Testando uma nova mensagem
# nova_mensagem = ["Você ganhou um prêmio, clique aqui!"]
nova_mensagem = []
nova_mensagem.append(input('Digite uma mensagem: '))
X_novo = vectorizer.transform(nova_mensagem)
previsao = modelo.predict(X_novo)
print(f"A mensagem foi classificada como: {previsao[0]}")

