def classificar_intencao(texto: str) -> str:
    texto = texto.lower()

    if any(palavra in texto for palavra in ["indica", "recomenda", "quero", "procuro", "me mostra"]):
        return "recomendar"

    elif any(palavra in texto for palavra in ["melhor", "versus", "vs", "comparar"]):
        return "comparar"

    elif any(palavra in texto for palavra in ["quanto custa", "preço", "valor"]):
        return "preco_info"

    elif any(palavra in texto for palavra in ["quantos", "potência", "cavalos", "consumo"]):
        return "especificações"

    elif any(palavra in texto for palavra in ["mais vendido", "popular", "preferido"]):
        return "curiosidade"

    return "desconhecida"
