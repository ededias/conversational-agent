import re
import spacy
import unicodedata
from rapidfuzz import fuzz, process
from app.agents import carregar_carros

nlp = spacy.load("pt_core_news_sm")



def extrair_modelo_da_frase(frase, df, limite_similaridade=80):
    from rapidfuzz import process, fuzz

    tokens = re.findall(r'\w+', frase.lower())
    frase_filtrada = " ".join([t for t in tokens if t not in {"qual", "o", "de", "um", "a", "é", "valor", "do", "da"}])
    
    modelos_unicos = df["Model"].dropna().unique().tolist()

    resultado = process.extractOne(frase_filtrada, modelos_unicos, scorer=fuzz.partial_ratio, score_cutoff=limite_similaridade)
    
    if resultado:
        return resultado[0]
    return None



def normalize(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8', 'ignore')


def extrair_tokens(texto):
    doc = nlp(texto.lower())
    tokens = [token.text for token in doc]
    return tokens

def extrair_carros(texto):
    
    tokens = extrair_tokens(texto)
    carros = carregar_carros()
    

    print(extrair_modelo_da_frase(texto, carros))
    
    
    marca_carros = [normalize(m) for m in carros["Make"].dropna().unique().tolist()]
    modelo_encontrada = extrair_modelo_da_frase(texto, carros)
    marca_encontrada = next((m for m in marca_carros if m.lower() in tokens), None)

    return modelo_encontrada, marca_encontrada
    
def extrair_parametros(texto):
    doc = nlp(texto.lower())

    # Extrair preço
    preco = None
    match = re.search(r"(\d{2,3})\s*(mil|k|milhões)?", texto.lower())
    if match:
        valor = int(match.group(1))
        unidade = match.group(2)
        if unidade in ["mil", "k"]:
            preco = valor * 1000
        elif unidade == "milhões":
            preco = valor * 1_000_000
        else:
            preco = valor
    # Transmissão
    if "automático" in texto:
        transmissao = "automatic"
    elif "manual" in texto:
        transmissao = "manual"
    else:
        transmissao = None

    # Combustível
    combustivel = None
    for token in doc:
        if token.text in ["flex", "petrol", 'gasolina', "etanol", "diesel"]:
            if token.text == "gasolina": 
                combustivel = "petrol"
            else:
                combustivel = token.text
    
    modelo_encontrada, marca_encotnrada = extrair_carros(texto)

    return {
        "preco_max": preco,
        "transmissao": transmissao,
        "combustivel": combustivel,
        "modelo": modelo_encontrada,
        "marca": marca_encotnrada
    }
