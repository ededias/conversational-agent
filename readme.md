# 🤖 Agente Conversacional para Concessionária de Veículos

Este projeto é um chatbot inteligente desenvolvido em Python, que entende mensagens dos usuários, classifica intenções e fornece respostas personalizadas com base em um dataset de veículos. Ele pode ser integrado ao WhatsApp via API e utiliza técnicas de NLP para tornar as respostas mais humanizadas.

---

## 🚀 Funcionalidades

- Classificação de intenções (ex: recomendação, curiosidade, saudação, etc.)
- Extração de parâmetros como marca, modelo e preço desejado
- Busca por veículos com base nos filtros informados
- Integração com FastAPI
- Suporte a mensagens no WhatsApp via Webhook
- Utilização de `TF-IDF` + `ML` para classificação
- Similaridade de modelo com `RapidFuzz`

---

## 🧠 Exemplo de frases que o bot entende

| Entrada do usuário                    | Intenção detectada | Resposta esperada                                  |
|--------------------------------------|---------------------|----------------------------------------------------|
| "Quero um carro até 50 mil"          | recomendação        | Lista de veículos abaixo de R$ 50.000             |
| "Qual o valor do Corolla?"           | consulta_preco      | Valor médio do Corolla no dataset                 |
| "Tem algum SUV automático?"          | recomendação        | Lista de SUVs automáticos                         |
| "Bom dia!"                            | saudação            | Saudação amigável                                 |

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- FastAPI
- Scikit-learn
- Pandas
- RapidFuzz
- Uvicorn
- Ngrok (para testes locais com WhatsApp)
- Langchain (opcional, futuro)

---


---

## ⚙️ Como Rodar o Projeto

### 1. Instale as dependências

```bash
pip install -r requirements.txt


