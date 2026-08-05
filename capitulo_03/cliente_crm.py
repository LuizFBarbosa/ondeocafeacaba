"""
Capítulo 3 — Cliente que consulta a API de preços
Simula o CRM pedindo preço ao "garçom" (API).
"""

import requests

BASE_URL = "http://127.0.0.1:8000"


def consultar_preco(produto_id: int):
    resp = requests.get(f"{BASE_URL}/precos/{produto_id}", timeout=5)
    if resp.status_code == 200:
        dados = resp.json()
        print(f"✅ {dados['nome']}: R$ {dados['preco']:.2f}", end="")
        if dados.get("promocao"):
            print(f"  → PROMO: R$ {dados['preco_promocional']:.2f}")
        else:
            print()
        return dados
    else:
        print(f"❌ Produto {produto_id}: {resp.status_code} — {resp.json()}")
        return None


if __name__ == "__main__":
    print("Consultando preços via API...\n")
    for pid in [101, 102, 105, 999]:
        consultar_preco(pid)
