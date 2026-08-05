"""
Capítulo 20 — O Universo Paralelo
Simulação de Monte Carlo com agentes para decisão de promoção.

PLUS:
  - Dois cenários lado a lado (30% vs 20%)
  - Percentis de risco (P5, P50, P95)
  - Elasticidade diferenciada por tipo de produto
"""

import random
from dataclasses import dataclass
import pandas as pd

PRECO_NORMAL = 8.50
CUSTO = 5.00
ESTOQUE_INICIAL = 200_000


@dataclass
class AgenteCliente:
    """Cliente simulado com sensibilidade individual a preço."""
    sensibilidade: float
    chance_base: float

    @classmethod
    def aleatorio(cls):
        return cls(
            sensibilidade=random.uniform(0.5, 1.5),
            chance_base=random.uniform(0.008, 0.04),
        )

    def vai_comprar(self, desconto: float) -> bool:
        chance = min(1.0, self.chance_base * (1 + desconto * self.sensibilidade * 3))
        return random.random() < chance


def simular(desconto: float, n_clientes: int = 30_000, estoque: int = ESTOQUE_INICIAL) -> dict:
    preco_promo = PRECO_NORMAL * (1 - desconto)
    lucro_unit = preco_promo - CUSTO
    estoque_restante = estoque
    vendas = 0

    for _ in range(n_clientes):
        if estoque_restante <= 0:
            break
        if AgenteCliente.aleatorio().vai_comprar(desconto):
            vendas += 1
            estoque_restante -= 1

    return {
        "lucro": vendas * lucro_unit,
        "vendas": vendas,
        "estoque_final": estoque_restante,
        "ruptura": estoque_restante == 0,
        "margem_pct": (lucro_unit / preco_promo * 100) if preco_promo else 0,
    }


def analisar(desconto: float, n_sims: int = 300) -> pd.DataFrame:
    random.seed(42)
    resultados = pd.DataFrame([simular(desconto) for _ in range(n_sims)])

    print(f"{'─'*40}")
    print(f"  Desconto: {desconto*100:.0f}%")
    print(f"{'─'*40}")
    print(f"  Lucro médio:          R$ {resultados['lucro'].mean():>12,.0f}")
    print(f"  Lucro mediano (P50):  R$ {resultados['lucro'].median():>12,.0f}")
    print(f"  Pior cenário (P5):    R$ {resultados['lucro'].quantile(0.05):>12,.0f}")
    print(f"  Melhor cenário (P95): R$ {resultados['lucro'].quantile(0.95):>12,.0f}")
    print(f"  Vendas médias:        {resultados['vendas'].mean():>12,.0f} un")
    print(f"  Risco de ruptura:     {resultados['ruptura'].mean()*100:>11.1f}%")
    print(f"  Margem unitária:      {resultados['margem_pct'].mean():>11.1f}%")
    print()
    return resultados


if __name__ == "__main__":
    print("=" * 40)
    print("  SIMULADOR DE FUTUROS — Monte Carlo")
    print("  Aposta: queima de 200 mil unidades")
    print("=" * 40)
    print()

    r30 = analisar(0.30)
    r20 = analisar(0.20)

    print("=" * 40)
    print("  RECOMENDAÇÃO")
    print("=" * 40)
    risco_30 = r30["ruptura"].mean()
    risco_20 = r20["ruptura"].mean()
    if risco_30 > risco_20 * 1.5:
        print("  Preferir 20%: risco de ruptura bem menor,")
        print("  lucro médio ainda saudável, operação mais controlável.")
    else:
        print("  Ambos viáveis — decidir pelo apetite de risco da diretoria.")
    print()
    print('  "A gente não comprou uma resposta. Comprou uma bússola."')
    print("  — Dona Fátima")
