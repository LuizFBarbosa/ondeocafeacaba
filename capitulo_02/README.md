# Capítulo 2 — O Império das Planilhas

**Limpeza de dados • pandas merge • DataFrames**

---

## O problema do livro

O relatório de lucratividade do Sr. Ricardo mostrava um “buraco negro”.  
Logística mandava uma planilha (`ID_Item`, `Custo_Unitario`).  
Financeiro mandava outra (`Cod_Produto`, `Preco_Venda`).  

Nomes diferentes, tipos diferentes (número vs texto) e estados escritos de três jeitos (`SP`, `S.P.`, `São Paulo`).  
O primeiro `merge` retornou **zero linhas**.

---

## O que este código faz

1. Lê `estoque.csv` e `faturamento.xlsx`
2. Padroniza nomes de colunas
3. Alinha tipos de dados (ambos `str`)
4. Normaliza nomes de estados
5. Faz o `merge` (inner join)
6. Calcula lucro por linha e mostra os piores resultados

---

## Como executar

```bash
pip install pandas openpyxl
python gerar_dados.py
python tradutor_universal.py
```

---

## Explicação passo a passo

### Por que o merge retornou zero linhas?

```python
# Estoque: ID_Item = 1023 (int)
# Faturamento: Cod_Produto = "1023" (str)
# Para o pandas: 1023 ≠ "1023"
```

Computador não adivinha. `Código`, `COD_PROD` e `ProdutoID` são três coisas completamente diferentes.

### A “alfândega dos dados”

Antes de qualquer `merge`:

1. **Padronizar nomes** → `rename`
2. **Alinhar tipos** → `astype(str)`
3. **Limpar valores categóricos** → `replace`
4. **Só então** → `pd.merge(..., on="ID_Produto")`

### Cálculo de lucro

```python
df["Lucro"] = (
    df["Preco_Venda"] * df["Qtd_Vendida"]
    - df["Custo_Unitario"] * df["Qtd_Vendida"]
)
```

No livro, o script encontrou um queijo importado com 30% de descarte por vencimento — o “buraco negro” que reuniões de meses não tinham enxergado.

---

## Conceitos-chave

| Conceito         | Tradução                                                  | Por que importa                    |
| ---------------- | --------------------------------------------------------- | ---------------------------------- |
| **merge / join** | Cruza duas tabelas pela chave comum                       | Une mundos que não se falavam      |
| **astype**       | Força o tipo de uma coluna                                | Evita o “zero linhas” silencioso   |
| **rename**       | Padroniza nomes de colunas                                | Computador não adivinha sinônimos  |
| **Tidy Data**    | Cada variável em uma coluna, cada observação em uma linha | Base de qualquer análise confiável |

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_02/README.md
