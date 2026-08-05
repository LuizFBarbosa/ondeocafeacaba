"""Gera base sintética de clientes para o Radar de Oportunidades."""
from pathlib import Path
import numpy as np
import pandas as pd

PASTA = Path(__file__).parent
np.random.seed(42)

n = 2000
df = pd.DataFrame({
    "produto_preco": np.random.uniform(5, 80, n).round(2),
    "cliente_frequencia": np.random.randint(1, 24, n),
    "tempo_ultima_compra": np.random.randint(7, 400, n),
})
# Probabilidade de recompra aumenta com frequência e diminui com tempo
logit = (
    0.02 * df["cliente_frequencia"]
    - 0.008 * df["tempo_ultima_compra"]
    + 0.01 * (50 - df["produto_preco"])
)
prob = 1 / (1 + np.exp(-logit))
df["comprou"] = (np.random.random(n) < prob).astype(int)

df.to_csv(PASTA / "clientes_inativos.csv", index=False)
print(f"✅ clientes_inativos.csv → {len(df)} linhas | taxa positiva: {df['comprou'].mean():.1%}")
