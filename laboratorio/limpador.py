"""Limpador de Planilhas Automático — Laboratório do Ziul."""
from pathlib import Path
import pandas as pd

def limpar_planilha(entrada, saida):
    try:
        df = pd.read_excel(entrada) if str(entrada).endswith(".xlsx") else pd.read_csv(entrada)
        df.dropna(how="all", inplace=True)
        df.drop_duplicates(inplace=True)
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        for col in df.select_dtypes(include=["number"]).columns:
            df[col] = df[col].fillna(df[col].mean())
        if str(saida).endswith(".xlsx"):
            df.to_excel(saida, index=False)
        else:
            df.to_csv(saida, index=False)
        print(f"✅ Planilha limpa salva em: {saida}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("Uso: limpar_planilha('vendas_sujo.xlsx', 'vendas_limpo.xlsx')")
    print("Função pronta para importar ou adaptar.")
