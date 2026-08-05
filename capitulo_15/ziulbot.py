"""
Capítulo 15 — ZiulBot (RAG ilustrativo)
Assistente conversacional ancorado em dados reais da empresa.

PLUS:
  - Retrieval simples por palavras-chave
  - Respostas diferentes conforme estoque/promoção
  - Aviso explícito quando não sabe (anti-alucinação didática)
"""

from typing import Optional

estoque = {
    "Arroz Tio João 5kg": 120,
    "Feijão Carioca 1kg": 300,
    "Óleo de Soja 900ml": 50,
    "Cerveja 600ml": 0,  # em falta
}

promocoes = {
    "Arroz Tio João 5kg": "Compre 10 e leve 2 grátis.",
    "Óleo de Soja 900ml": "3% off combinando com arroz.",
}

precos = {
    "Arroz Tio João 5kg": 18.90,
    "Feijão Carioca 1kg": 7.50,
    "Óleo de Soja 900ml": 5.20,
    "Cerveja 600ml": 4.50,
}

# Mapa de sinônimos → chave canônica (retrieval simplificado)
ALIASES = {
    "arroz": "Arroz Tio João 5kg",
    "tio joão": "Arroz Tio João 5kg",
    "feijão": "Feijão Carioca 1kg",
    "feijao": "Feijão Carioca 1kg",
    "óleo": "Óleo de Soja 900ml",
    "oleo": "Óleo de Soja 900ml",
    "cerveja": "Cerveja 600ml",
}


def recuperar_produto(pergunta: str) -> Optional[str]:
    """Etapa 1 do RAG: Retrieval — encontra o produto relevante."""
    p = pergunta.lower()
    for alias, canonico in ALIASES.items():
        if alias in p:
            return canonico
    return None


def gerar_resposta(produto: str, pergunta: str) -> str:
    """Etapa 2 do RAG: Generation — monta resposta com dados reais."""
    qtd = estoque.get(produto, 0)
    preco = precos.get(produto)
    promo = promocoes.get(produto)
    p = pergunta.lower()

    if qtd <= 0:
        return (
            f"Infelizmente {produto} está em falta no momento. "
            "Posso sugerir um similar ou avisar quando chegar?"
        )

    partes = [f"Temos {qtd} unidades de {produto}."]
    if preco is not None and ("preço" in p or "preco" in p or "valor" in p or "custa" in p):
        partes.append(f"Preço: R$ {preco:.2f}.")
    elif preco is not None:
        partes.append(f"Preço: R$ {preco:.2f}.")
    if promo:
        partes.append(f"Promoção ativa: {promo}")
    partes.append("Quer que eu monte o pedido?")
    return " ".join(partes)


def ziulbot_responde(pergunta: str) -> str:
    """
    Pipeline RAG ilustrativo:
      1. Retrieval  → busca produto na base
      2. Generation → responde só com o que encontrou
    Se não achar: admite que não sabe (não alucina).
    """
    produto = recuperar_produto(pergunta)
    if produto is None:
        return (
            "Não encontrei esse item na base agora. "
            "Pode reformular com o nome do produto? "
            "Quero garantir que estou buscando a informação certa."
        )
    return gerar_resposta(produto, pergunta)


if __name__ == "__main__":
    perguntas = [
        "Qual o estoque do óleo de soja e o preço?",
        "Tem arroz tio joão?",
        "E a cerveja?",
        "Quanto custa o feijão?",
        "Tem açaí premium?",  # fora da base → não inventa
    ]
    for q in perguntas:
        print(f"P: {q}")
        print(f"R: {ziulbot_responde(q)}\n")
