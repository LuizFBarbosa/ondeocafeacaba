"""
Capítulo 1 — Gerador de dados realistas de vendas
Gera o arquivo vendas_ontem.xlsx usado pelo relatório automatizado.
"""

from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd

PASTA = Path(__file__).parent
ARQUIVO = PASTA / "vendas_ontem.xlsx"

REPRESENTANTES = [
    "Ana Souza", "Bruno Lima", "Carla Mendes", "David Oliveira",
    "Elena Costa", "Fábio Rocha", "Gabriela Santos", "Hugo Pereira",
]

CLIENTES = [
    (1001, "Mercado Bom Preço"),
    (1002, "Padaria Central"),
    (1003, "Minimercado São José"),
    (1004, "Atacarejo Norte"),
    (1005, "Distribuidora Sul"),
    (1006, "Empório da Vila"),
    (1007, "Supermercado Popular"),
    (1008, "Casa de Carnes Boa"),
    (1009, "Hortifruti Verde"),
    (1010, "Conveniência 24h"),
    (1011, "Mercadinho da Esquina"),
    (1012, "Atacado Familiar"),
]

PRODUTOS = [
    "Arroz Tio João 5kg", "Feijão Carioca 1kg", "Óleo de Soja 900ml",
    "Açúcar Cristal 1kg", "Café Torrado 500g", "Leite Integral 1L",
    "Cerveja 600ml", "Refrigerante 2L", "Macarrão Espaguete 500g",
    "Farinha de Trigo 1kg",
]


def gerar():
    random.seed(42)
    linhas = []
    data_base = datetime.now().date() - timedelta(days=1)

    for _ in range(180):
        id_cli, nome_cli = random.choice(CLIENTES)
        rep = random.choice(REPRESENTANTES)
        produto = random.choice(PRODUTOS)
        qtd = random.randint(2, 40)
        # Preço unitário realista (R$)
        preco = round(random.uniform(3.5, 28.0), 2)
        valor = round(qtd * preco, 2)

        # Formata como texto "bonito" (como Dona Fátima fazia)
        valor_texto = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        linhas.append({
            "Data": data_base.strftime("%d/%m/%Y"),
            "ID_Cliente": id_cli,
            "Nome_Cliente": nome_cli,
            "Representante": rep,
            "Produto": produto,
            "Quantidade": qtd,
            "Valor_Venda": valor_texto,  # texto formatado (o problema clássico)
        })

    df = pd.DataFrame(linhas)
    df.to_excel(ARQUIVO, index=False)
    print(f"✅ Arquivo gerado: {ARQUIVO}")
    print(f"   {len(df)} linhas | Representantes: {df['Representante'].nunique()}")
    return df


if __name__ == "__main__":
    gerar()
