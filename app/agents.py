import kagglehub
import pandas as pd




def carregar_carros():
    
    df = pd.read_csv('/home/edenilson/dev/puc/chatbot-wpp/app/dataset/cars.csv')

    # Limpeza básica
    df.dropna(subset=["Price", "Model", "Transmission"], inplace=True)
    df["selling_price"] = pd.to_numeric(df["Price"], errors='coerce')
    
    # Converter transmissões pra lowercase (manual, automático)
    df["transmission"] = df["Transmission"].str.lower()

    return df

def buscar_carros(parameters: dict, df: pd.DataFrame, limite=2):
    result = df.copy()
    
    if 'preco_max' in parameters and parameters['preco_max'] is not None:
        result = result[result["selling_price"] <= parameters['preco_max']]
    
    if 'transmissao' in parameters and parameters['transmissao'] is not None:
        result = result[result["transmission"].str.lower() == parameters['transmissao'].lower()]

    if "combustivel" in parameters and parameters['combustivel'] is not None:
        result = result[result["Fuel Type"].str.lower() == parameters["combustivel"].lower()]
    
    if "marca" in parameters and parameters['marca'] is not None:
        result = result[result["Make"].str.lower() == parameters["marca"].lower()]
    if "modelo" in parameters and parameters['modelo'] is not None:
        result = result[result["Model"].str.lower() == parameters["modelo"].lower()]

    result = result.sort_values(by="selling_price", ascending=True)

    return result.head(limite)

