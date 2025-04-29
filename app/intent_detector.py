import joblib
import os

# Caminho para o modelo treinado
MODEL_PATH = 'app/models/intent_classifier.pkl'

# Carrega o modelo treinado (Tfidf + Classificador)
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Modelo não encontrado em {MODEL_PATH}. Rode o script de treinamento primeiro.")

modelo = joblib.load(MODEL_PATH)

def detectar_intencao(frase: str) -> str:
    """
    Retorna a intenção prevista para uma frase de usuário.
    """
    intencao_prevista = modelo.predict([frase])[0]
    return intencao_prevista
