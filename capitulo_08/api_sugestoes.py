"""
Capítulo 8 — O Garçom Inteligente
API de ML que sugere promoção personalizada.
"""

from collections import Counter
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API de Sugestões — Atacado São Bento", version="2.0")


def modelo_sugerir(id_cliente: int, historico: list) -> str:
    if not historico:
        return "produto_generico"
    return f"promo_{Counter(historico).most_common(1)[0][0]}"


class ClienteInput(BaseModel):
    id_cliente: int
    ultima_categoria: str
    ticket_medio: float


@app.post("/sugerir/")
async def sugerir_promocao(cliente: ClienteInput):
    historico = [cliente.ultima_categoria] * 3
    sugestao = modelo_sugerir(cliente.id_cliente, historico)
    return {
        "id_cliente": cliente.id_cliente,
        "sugestao": sugestao,
        "confianca": 0.87,
        "mensagem": f"Oferta em {cliente.ultima_categoria} tem alta chance de sucesso.",
    }


@app.get("/")
async def root():
    return {"status": "ok", "docs": "/docs"}
