"""
Capítulo 16 — O DNA do Conhecimento
Sistema de recomendação de conteúdo por habilidade fraca.

PLUS:
  - Ordenação por nível (básico primeiro)
  - Limite de duração para 1ª sugestão
  - Simulação de taxa de conclusão
"""

from pathlib import Path
import pandas as pd

catalogo = pd.DataFrame({
    "id": ["V001", "A001", "C001", "V002", "V003", "A002"],
    "tipo": ["Video", "Artigo", "Checklist", "Video", "Video", "Artigo"],
    "titulo": [
        "Como Vender Inovação",
        "Técnicas de Negociação",
        "Onboarding de Novos Clientes",
        "Gestão de Tempo Avançada",
        "Primeiros Passos em Venda Estratégica",
        "Comunicando com Áreas de Negócio",
    ],
    "habilidade": [
        "venda_estrategica",
        "negociacao",
        "prospeccao",
        "produtividade",
        "venda_estrategica",
        "comunicacao",
    ],
    "nivel": ["Intermediário", "Básico", "Básico", "Avançado", "Básico", "Básico"],
    "duracao_min": [18, 12, 8, 45, 10, 12],
})

# Performance de exemplo (1–10)
performance = {
    "Ana": {
        "venda_estrategica": 3.5,
        "negociacao": 8.0,
        "prospeccao": 9.0,
        "produtividade": 6.0,
        "comunicacao": 7.0,
    },
    "Junior": {
        "venda_estrategica": 7.0,
        "negociacao": 6.0,
        "prospeccao": 5.0,
        "produtividade": 8.0,
        "comunicacao": 3.0,  # o espelho do livro
    },
}


def recomendar(perf: dict, catalogo: pd.DataFrame, max_min: int = 20) -> tuple:
    """
    Encontra a habilidade mais fraca e recomenda o conteúdo
    mais básico e curto disponível (evita o erro da 1ª versão do livro).
    """
    habilidade_fraca = min(perf, key=perf.get)
    ordem_nivel = {"Básico": 0, "Intermediário": 1, "Avançado": 2}

    recs = catalogo[catalogo["habilidade"] == habilidade_fraca].copy()
    recs["_ordem"] = recs["nivel"].map(ordem_nivel)
    recs = (
        recs.sort_values(["_ordem", "duracao_min"])
        .query(f"duracao_min <= {max_min}")
        .drop(columns=["_ordem"])
    )
    return recs, habilidade_fraca


def simular_conclusao(nivel: str, duracao: int) -> float:
    """
    PLUS: estima taxa de conclusão.
    Conteúdo avançado/longo → menor adesão (lição do livro: 12% → 71%).
    """
    base = {"Básico": 0.75, "Intermediário": 0.55, "Avançado": 0.30}
    penalidade = max(0, (duracao - 15) * 0.01)
    return max(0.05, base.get(nivel, 0.5) - penalidade)


if __name__ == "__main__":
    for pessoa, perf in performance.items():
        recs, h = recomendar(perf, catalogo)
        print(f"\n{'='*50}")
        print(f"  {pessoa} — habilidade a desenvolver: {h} (nota {perf[h]})")
        print(f"{'='*50}")
        if recs.empty:
            print("  Nenhum conteúdo curto disponível.")
            continue
        for _, row in recs.iterrows():
            taxa = simular_conclusao(row["nivel"], row["duracao_min"])
            print(
                f"  → {row['titulo']} ({row['tipo']}, {row['nivel']}, "
                f"{row['duracao_min']} min) | conclusão estimada: {taxa:.0%}"
            )
