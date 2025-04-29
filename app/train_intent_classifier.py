import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

# 🔤 Frases de exemplo com intenções
dados = {
    'frase': [
        'quero um carro até 50 mil',
        'procuro um SUV automático',
        'tem carro da Honda?',
        'qual o preço do Onix?',
        'quanto custa o corolla?',
        'olá',
        'bom dia',
        'obrigado',
        'até logo',
        'tenho interesse em um sedan usado',
        'vocês vendem carros financiados?',
        'adeus'
    ],
    'intencao': [
        'recomendar_carro',
        'recomendar_carro',
        'recomendar_carro',
        'perguntar_preco',
        'perguntar_preco',
        'saudacao',
        'saudacao',
        'despedida',
        'despedida',
        'recomendar_carro',
        'perguntar_financiamento',
        'despedida'
    ]
}

# 📄 DataFrame
df = pd.DataFrame(dados)

# 🧠 Embeddings com modelo multilíngue
embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
X = embedder.encode(df['frase'].tolist())
y = df['intencao']

# 🎯 Treinar classificador
clf = LogisticRegression(max_iter=1000)
clf.fit(X, y)

# 💾 Salvar modelo e embedder
joblib.dump(clf, 'app/models/intent_classifier.pkl')
joblib.dump(embedder, 'app/models/sentence_embedder.pkl')

print("✅ Modelos salvos como 'intent_classifier.pkl' e 'sentence_embedder.pkl'")
