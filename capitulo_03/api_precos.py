"""
Capítulo 3 — O Garçom de Preços
API REST simples com FastAPI que expõe preços do ERP.

Como rodar:
  uvicorn api_precos:app --reload
  Depois abra: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="API de Preços — Atacado São Bento",
    description="Expõe preços do ERP de forma segura e documentada.",
    version="1.0.0",
)

# Base simulada (em produção viria do ERP)
BASE_DE_PRECOS = {
    101: {"nome": "Cerveja 600ml", "preco": 4.50, "promocao": False},
    102: {
        "nome": "Refrigerante 2L",
        "preco": 8.00,
        "promocao": True,
        "preco_promocional": 6.50,
    },
    103: {"nome": "Arroz 5kg", "preco": 18.90, "promocao": False},
    104: {"nome": "Feijão 1kg", "preco": 7.50, "promocao": False},
    105: {
        "nome": "Óleo 900ml",
        "preco": 6.20,
        "promocao": True,
        "preco_promocional": 5.20,
    },
}


@app.get("/")
async def root():
    return {
        "mensagem": "API de Preços — Atacado São Bento",
        "docs": "/docs",
        "endpoints": ["/precos/{produto_id}", "/precos"],
    }


@app.get("/precos")
async def listar_precos():
    """Lista todos os produtos com preço."""
    return BASE_DE_PRECOS


@app.get("/precos/{produto_id}")
async def obter_preco(produto_id: int):
    """Retorna o preço de um produto específico."""
    produto = BASE_DE_PRECOS.get(produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"produto_id": produto_id, **produto}
