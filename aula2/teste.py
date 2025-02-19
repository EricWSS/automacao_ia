# Importando bibliotecas necessárias
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Dados de exemplo
mensagens = ["Promoção imperdível, clique aqui!",
             "Oi, tudo bem?",
             "Ganhe dinheiro rápido, sem esforço!",
             "Sua conta foi atualizada com sucesso."]

rotulos = ["spam", "não spam", "spam", "não spam"]  # Rótulos das mensagens

# Convertendo texto para números
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(mensagens)

# Criando o modelo
modelo = MultinomialNB()
modelo.fit(X, rotulos)

# Testando uma nova mensagem
nova_mensagem = ["Você ganhou um prêmio, clique aqui!"]
X_novo = vectorizer.transform(nova_mensagem)
previsao = modelo.predict(X_novo)

print(f"A mensagem foi classificada como: {previsao[0]}")
