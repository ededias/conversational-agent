from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from app.agents import carregar_carros, buscar_carros
from app.nlp_utils import extrair_parametros
from dotenv import load_dotenv
import os
import joblib
import requests


load_dotenv()
FB_TOKEN = os.getenv("FB_TOKEN")

classifier = joblib.load('app/models/intent_classifier.pkl')
embedder = joblib.load('app/models/sentence_embedder.pkl')

app = FastAPI()

@app.get("/")
def home():
    print('hello')
    return {"msg": "Bot da concessionária está online!"}

@app.get("/webhook")
def verificar_webhook(
    req: Request,
):
    VERIFY_TOKEN = "ODMZDIQQWGIUBRNRRASH"
    token = req.query_params.get("hub.verify_token");
    challange = req.query_params.get("hub.challenge");
    print(challange);
    if token == VERIFY_TOKEN:
        return PlainTextResponse(content=challange, status_code=200)
    else:
        return PlainTextResponse(content="Erro de verificação", status_code=403)

@app.post("/webhook")    
async def receber_mensagem(request: Request):
    data = await request.json()
    print("🔔 Webhook recebido:")
    
    try:
        mensagens = data["entry"][0]["changes"][0]["value"]["messages"]
        for mensagem in mensagens:
            texto = mensagem["text"]["body"]

            emb = embedder.encode([texto])
            probas = classifier.predict_proba(emb)[0]
            idx = probas.argmax()
            confianca = probas[idx]
            intent = classifier.classes_[idx]
            print(f"Intenção: {intent}, Confiança: {confianca:.2f}")
            resposta = "Oi, tudo bem? Não entendi sua mensagem. Pode reformular?"

            if intent == "saudacao":
                resposta = "Olá! Como posso ajudar você hoje?"
            elif intent == "despedida":
                resposta = "Se precisar de mais alguma coisa, é só avisar."
            
            if intent == "perguntar_preco":
                resposta = ''
                df = carregar_carros()
                parametros = extrair_parametros(texto)
                resultado = buscar_carros(parametros, df)
                for carro in resultado[["Model", "Price", "transmission", 'Fuel Type', 'Make']].to_dict(orient="records"):
                    resposta += (f"Marca: {carro['Make']}, Modelo: {carro['Model']}, Preço: {carro['Price']}, Transmissão: {carro['transmission']}, Combustivel: {carro['Fuel Type']} \n")

            if intent == "recomendar_carro":
                print("Recomendação de carro")
                resposta = '';
                df = carregar_carros()
                parametros = extrair_parametros(texto)
                resultado = buscar_carros(parametros, df)
                if not len(resultado):
                    resposta = "Não encontrei nenhum carro com estas especificações ou valores"
                for carro in resultado[["Model", "Price", "transmission", 'Fuel Type', 'Make']].to_dict(orient="records"):
                    resposta += (f"Marca: {carro['Make']}, Modelo: {carro['Model']}, Preço: {carro['Price']}, Transmissão: {carro['transmission']}, Combustivel: {carro['Fuel Type']} \n")

                    
            requests.post(
                f"https://graph.facebook.com/v22.0/666867103166534/messages",
                headers={
                    "Authorization": "Bearer " + FB_TOKEN,
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": '5541987265256',
                    "text": {
                        "body": f"{resposta}"
                    }
                })
            
    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")
        print("Nenhuma mensagem recebida ou formato inesperado.")

    return {"status": "mensagem recebida"}