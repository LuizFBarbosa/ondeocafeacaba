# Capítulo 1 — O Dia em que o Café Acabou

**Automação de relatórios • pandas • openpyxl • smtplib**

---

## O problema do livro

Dona Fátima gastava **45 minutos todo dia** montando o relatório matinal de vendas em planilha.  
Valores vinham formatados como texto (`R$ 1.250,00`), fórmulas quebravam e o relatório às vezes saía depois das 8h30.

Ziul automatizou tudo. O script roda em **~4 segundos**.

---

## O que este código faz

1. Lê a planilha `vendas_ontem.xlsx`
2. Converte valores formatados como texto em números reais
3. Agrupa o faturamento por representante
4. Calcula o Top 10 clientes
5. Imprime o relatório formatado

---

## Arquivos desta pasta

| Arquivo               | Descrição                                                |
| --------------------- | -------------------------------------------------------- |
| `gerar_dados.py`      | Gera planilha realista de vendas (como a de Dona Fátima) |
| `relatorio_vendas.py` | Script principal do relatório automatizado               |
| `README.md`           | Este arquivo                                             |

---

## Como executar

```bash
# 1. Instale as dependências (se ainda não instalou)
pip install pandas openpyxl

# 2. Gere os dados de exemplo
python gerar_dados.py

# 3. Rode o relatório
python relatorio_vendas.py
```

### Saída esperada (exemplo)

```
==================================================
  RELATÓRIO DE VENDAS — ATACADO SÃO BENTO
==================================================

📊 Total por Representante:
 Representante  Valor_Venda
   Ana Souza      15234.50
  Bruno Lima      14890.20
  ...

🏆 Top 10 Clientes:
 ID_Cliente        Nome_Cliente  Valor_Venda
      1004     Atacarejo Norte     4230.80
      ...

💰 Faturamento total: R$ 98.456,30
```

---

## Explicação do código (passo a passo)

### 1. Função `limpar_valor`

```python
def limpar_valor(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        texto = (
            v.replace("R$", "")
            .replace(" ", "")
            .replace(".", "")   # tira ponto de milhar
            .replace(",", ".")  # vírgula → ponto decimal
            .strip()
        )
        return float(texto)
    return float(v)
```

**Por que é necessária?**  
No Excel brasileiro, números monetários muitas vezes são salvos como texto formatado. O pandas lê `"R$ 1.250,00"` como string. Sem essa limpeza, qualquer cálculo (`sum`, `mean`, etc.) falha ou produz resultado errado.

### 2. Leitura e limpeza

```python
df = pd.read_excel(caminho)
df["Valor_Venda"] = df["Valor_Venda"].apply(limpar_valor)
```

`pd.read_excel` usa **openpyxl** por baixo dos panos.  
O `.apply` aplica a função em cada célula da coluna.

### 3. GroupBy por representante

```python
relatorio = (
    df.groupby("Representante")["Valor_Venda"]
    .sum()
    .reset_index()
    .sort_values("Valor_Venda", ascending=False)
)
```

Equivale a um `SOMASE` do Excel, só que em uma linha e milhares de vezes mais rápido.

### 4. Top 10 clientes

```python
top10 = (
    df.groupby(["ID_Cliente", "Nome_Cliente"])["Valor_Venda"]
    .sum()
    .reset_index()
    .sort_values("Valor_Venda", ascending=False)
    .head(10)
)
```

Agrupa por cliente, soma o valor e pega os 10 maiores.

---

## Conceitos-chave (linguagem de atacado)

| Conceito      | Tradução sem tecniquês                                                 | Por que importa                                 |
| ------------- | ---------------------------------------------------------------------- | ----------------------------------------------- |
| **pandas**    | Biblioteca que transforma planilhas em objetos manipuláveis por código | Lê, limpa, filtra e agrega em segundos          |
| **DataFrame** | A “tabela inteligente” do pandas                                       | Formato central de trabalho com dados tabulares |
| **groupby()** | Agrupa linhas por uma coluna e calcula estatísticas                    | Substitui SOMASE / TABELA DINÂMICA              |
| **openpyxl**  | Biblioteca que o pandas usa para ler/escrever `.xlsx`                  | Entende o formato real do Excel                 |

---

## Impacto no negócio (do livro)

| Situação           | Antes                      | Depois                 |
| ------------------ | -------------------------- | ---------------------- |
| Tempo de geração   | 45 min/dia                 | ~4 segundos            |
| Horário de entrega | Variável (às vezes > 8h30) | Sempre 7h30 (agendado) |
| Horas economizadas | —                          | ~16h30 por mês         |

---

## Próximos passos (opcional)

- Agendar no **Agendador de Tarefas do Windows** (ou `cron` no Linux) para rodar às 7h30
- Enviar o resultado por e-mail com `smtplib` (veja extensão no livro)
- Salvar o relatório em Excel ou PDF automaticamente

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_01/README.md
