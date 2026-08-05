"""
Capítulo 2 — Gerador de dados para o Império das Planilhas
Cria estoque.csv e faturamento.xlsx com nomes de colunas diferentes
e tipos inconsistentes (o problema clássico de merge).
"""

from pathlib import Path
import random
import pandas as pd

PASTA = Path(__file__).parent
random.seed(42)

PRODUTOS = [
    (1023, "Cerveja 600ml", 2.80, 4.50),
    (1024, "Refrigerante 2L", 3.50, 8.00),
    (1025, "Arroz 5kg", 12.00, 18.90),
    (1026, "Feijão 1kg", 4.20, 7.50),
    (1027, "Óleo 900ml", 3.80, 6.20),
    (1028, "Açúcar 1kg", 2.10, 3.90),
    (1029, "Café 500g", 8.50, 14.90),
    (1030, "Leite 1L", 2.90, 4.80),
    (1031, "Macarrão 500g", 1.80, 3.50),
    (1032, "Farinha 1kg", 2.40, 4.20),
    (1033, "Queijo Importado", 45.00, 89.90),  # o "buraco negro"
    (1034, "Presunto 1kg", 18.00, 32.00),
]

ESTADOS = ["São Paulo", "SP", "S.P.", "Rio de Janeiro", "RJ", "Minas Gerais", "MG"]


def gerar():
    # --- Estoque (ID numérico, nomes diferentes) ---
    estoque = []
    for pid, nome, custo, _ in PRODUTOS:
        estoque.append({
            "ID_Item": pid,                    # número
            "Descricao": nome,
            "Custo_Unitario": custo,
            "Qtd_Estoque": random.randint(50, 800),
        })
    df_est = pd.DataFrame(estoque)
    df_est.to_csv(PASTA / "estoque.csv", index=False)
    print(f"✅ estoque.csv  → {len(df_est)} produtos")

    # --- Faturamento (código como texto, nomes diferentes, estados bagunçados) ---
    fat = []
    for _ in range(120):
        pid, nome, _, preco = random.choice(PRODUTOS)
        qtd = random.randint(1, 30)
        fat.append({
            "Cod_Produto": str(pid),           # texto!
            "Nome do Produto": nome,
            "Preco_Venda": preco,
            "Qtd_Vendida": qtd,
            "Estado": random.choice(ESTADOS),
        })
    df_fat = pd.DataFrame(fat)
    df_fat.to_excel(PASTA / "faturamento.xlsx", index=False)
    print(f"✅ faturamento.xlsx → {len(df_fat)} linhas")
    return df_est, df_fat


if __name__ == "__main__":
    gerar()
