"""
Capítulo 2 — O Tradutor Universal
Padroniza e faz o merge entre planilha de estoque e de faturamento.
Demonstra o problema clássico: códigos texto vs número e nomes diferentes.
"""

from pathlib import Path
import pandas as pd

PASTA = Path(__file__).parent


def carregar_e_padronizar():
    df_estoque = pd.read_csv(PASTA / "estoque.csv")
    df_faturamento = pd.read_excel(PASTA / "faturamento.xlsx")

    print("=== ANTES da padronização ===")
    print(f"Estoque  colunas: {list(df_estoque.columns)}")
    print(f"Faturamento colunas: {list(df_faturamento.columns)}")
    print(f"Tipo ID_Item (estoque): {df_estoque['ID_Item'].dtype}")
    print(f"Tipo Cod_Produto (fat): {df_faturamento['Cod_Produto'].dtype}")

    # 1. Padronizar nomes de coluna
    df_estoque = df_estoque.rename(columns={
        "ID_Item": "ID_Produto",
        "Descricao": "Produto",
    })
    df_faturamento = df_faturamento.rename(columns={
        "Cod_Produto": "ID_Produto",
        "Nome do Produto": "Produto",
    })

    # 2. Padronizar tipos (ambos como string)
    df_estoque["ID_Produto"] = df_estoque["ID_Produto"].astype(str)
    df_faturamento["ID_Produto"] = df_faturamento["ID_Produto"].astype(str)

    # 3. Padronizar estados
    if "Estado" in df_faturamento.columns:
        df_faturamento["Estado"] = df_faturamento["Estado"].replace(
            {"S.P.": "São Paulo", "SP": "São Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais"}
        )

    # 4. Merge
    df = pd.merge(df_estoque, df_faturamento, on="ID_Produto", how="inner", suffixes=("_est", "_fat"))

    # 5. Calcular lucro
    df["Lucro"] = (
        df["Preco_Venda"] * df["Qtd_Vendida"]
        - df["Custo_Unitario"] * df["Qtd_Vendida"]
    )

    print("\n=== DEPOIS do merge ===")
    print(f"Linhas combinadas: {len(df)}")
    print("\nTop 10 piores lucros (possíveis 'buracos negros'):")
    colunas = [c for c in ["Produto_est", "Produto_fat", "Lucro"] if c in df.columns]
    if "Produto_est" not in df.columns and "Produto" in df.columns:
        colunas = ["Produto", "Lucro"]
    print(df[colunas].sort_values("Lucro").head(10).to_string(index=False))

    return df


if __name__ == "__main__":
    carregar_e_padronizar()
