"""
Capítulo 1 — O Relatório que Nunca Dorme
Automatiza o relatório matinal de vendas do Atacado São Bento.

Corrige o problema clássico de valores formatados como texto
("R$ 1.250,00") e gera:
  - Total por representante
  - Top 10 clientes

Uso:
  1. python gerar_dados.py          # cria vendas_ontem.xlsx
  2. python relatorio_vendas.py     # processa e imprime o relatório
"""

from pathlib import Path
import pandas as pd

PASTA = Path(__file__).parent
ARQUIVO_VENDAS = PASTA / "vendas_ontem.xlsx"


def limpar_valor(v):
    """Converte 'R$ 1.250,00' → 1250.00 (float)."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        texto = (
            v.replace("R$", "")
            .replace(" ", "")
            .replace(".", "")   # remove separador de milhar
            .replace(",", ".")  # vírgula decimal → ponto
            .strip()
        )
        return float(texto)
    return float(v)


def gerar_relatorio_vendas(caminho: str | Path):
    """
    Lê a planilha, limpa os valores e retorna:
      - relatorio: total por representante
      - top10: os 10 clientes com maior valor de venda
    """
    caminho = Path(caminho)
    try:
        df = pd.read_excel(caminho)
        df["Valor_Venda"] = df["Valor_Venda"].apply(limpar_valor)

        relatorio = (
            df.groupby("Representante")["Valor_Venda"]
            .sum()
            .reset_index()
            .sort_values("Valor_Venda", ascending=False)
        )

        top10 = (
            df.groupby(["ID_Cliente", "Nome_Cliente"])["Valor_Venda"]
            .sum()
            .reset_index()
            .sort_values("Valor_Venda", ascending=False)
            .head(10)
        )

        return relatorio, top10

    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho}")
        print("   Execute antes: python gerar_dados.py")
        return None, None


def main():
    rel, top = gerar_relatorio_vendas(ARQUIVO_VENDAS)
    if rel is None:
        return

    print("\n" + "=" * 50)
    print("  RELATÓRIO DE VENDAS — ATACADO SÃO BENTO")
    print("=" * 50)

    print("\n📊 Total por Representante:")
    print(rel.to_string(index=False))

    print("\n🏆 Top 10 Clientes:")
    print(top.to_string(index=False))

    total = rel["Valor_Venda"].sum()
    print(f"\n💰 Faturamento total: R$ {total:,.2f}")
    print("=" * 50)


if __name__ == "__main__":
    main()
