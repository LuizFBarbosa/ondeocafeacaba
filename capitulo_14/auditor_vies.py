"""
Capítulo 14 — O Auditor de Consciência
Detecta viés de recomendação + A/B Testing com teste estatístico.

PLUS:
  - Piso de exposição para produtos estratégicos
  - Simulação de conversão
  - t-test (scipy) para decidir se escala a correção
"""

import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(42)

historico_vendas = pd.DataFrame({
    "produto": [
        "Cerveja A", "Refrigerante B", "Arroz C",
        "Produto Orgânico X", "Snack Inovador Y",
    ],
    "vendas_ultimos_6_meses": [4200, 3800, 3100, 40, 25],
})

ESTRATEGICOS = ["Produto Orgânico X", "Snack Inovador Y"]


def modelo_recomendacao(historico: pd.DataFrame, n: int = 1000, piso_exposicao: float = 0.0):
    """
    Recomenda proporcionalmente ao histórico.
    piso_exposicao garante chance mínima mesmo sem histórico
    (sem isso, quem nunca vendeu nunca é recomendado).
    """
    pesos = historico["vendas_ultimos_6_meses"].to_numpy(dtype=float)
    pesos = np.maximum(pesos, pesos.sum() * piso_exposicao)
    probs = pesos / pesos.sum()
    escolhas = np.random.choice(historico["produto"], size=n, p=probs)
    return pd.Series(escolhas).value_counts()


def auditar_vies(contagem: pd.Series, produtos: list, n: int, limite: float = 0.05) -> bool:
    exposicao = contagem.reindex(produtos, fill_value=0).sum() / n
    if exposicao < limite:
        print(f"⚠️  VIÉS: produtos estratégicos em só {exposicao:.1%} das recomendações.")
        return False
    print(f"✅ Produtos estratégicos em {exposicao:.1%} das recomendações.")
    return True


def simular_conversao(contagem: pd.Series, produto: str, taxa: float = 0.12) -> np.ndarray:
    vezes = int(contagem.get(produto, 0))
    if vezes == 0:
        return np.array([])
    return np.random.binomial(1, taxa, size=vezes)


def ab_test(conv_a: np.ndarray, conv_b: np.ndarray):
    print(f"\nGrupo A (original):  {conv_a.sum()} conversões em {len(conv_a)} exposições")
    print(f"Grupo B (corrigido): {conv_b.sum()} conversões em {len(conv_b)} exposições")
    if len(conv_a) < 2 or len(conv_b) < 2:
        print("Dados insuficientes no grupo A — o próprio viés se confirma.")
        return
    t, p = stats.ttest_ind(conv_a, conv_b)
    print(f"p-value: {p:.4f}")
    if p < 0.05:
        print("✅ Diferença significativa — escalar modelo corrigido.")
    else:
        print("⚠️  Ainda sem significância estatística — coletar mais dados.")


if __name__ == "__main__":
    print("— Modelo original (sem piso) —")
    r0 = modelo_recomendacao(historico_vendas, piso_exposicao=0.0)
    print(r0.to_string())
    auditar_vies(r0, ESTRATEGICOS, 1000)

    print("\n— Modelo corrigido (piso 8%) —")
    r1 = modelo_recomendacao(historico_vendas, piso_exposicao=0.08)
    print(r1.to_string())
    auditar_vies(r1, ESTRATEGICOS, 1000)

    print("\n— A/B Testing —")
    conv_a = simular_conversao(r0, "Produto Orgânico X")
    conv_b = simular_conversao(r1, "Produto Orgânico X")
    ab_test(conv_a, conv_b)
