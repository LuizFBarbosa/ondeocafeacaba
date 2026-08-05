# Capítulo 14 — O Código e o Propósito

**Viés algorítmico • IA responsável • A/B Testing • scipy.stats**

---

## O problema do livro

A API de sugestões estava com ótimos números.  
Mas a linha de produtos **orgânicos** — investimento estratégico — apareceu **zero vezes** em milhares de recomendações.

O modelo não estava quebrado. Estava sendo **perfeitamente coerente com um passado que já não servia**.

Júnior foi quem levantou a mão: *“Acho que o modelo está enviesado.”*

---

## O que este código faz

1. Simula recomendações proporcionais ao histórico de vendas
2. Detecta subexposição de produtos estratégicos
3. Aplica **piso de exposição** (correção de justiça)
4. Roda A/B Testing com teste t de Student
5. Decide, com rigor estatístico, se escala a correção

---

## Como executar

```bash
pip install pandas numpy scipy
python auditor_vies.py
```

---

## Explicação passo a passo

### 1. Por que o orgânico sumiu?

```python
pesos = vendas_historicas
probs = pesos / pesos.sum()
# Produto com 40 vendas em 6 meses quase não é sorteado
```

Maximizar precisão no passado = ignorar o que nunca teve chance.

### 2. Piso de exposição

```python
pesos = np.maximum(pesos, pesos.sum() * 0.08)
```

Garante que produtos estratégicos tenham pelo menos ~8% de chance,  
mesmo com histórico pequeno. O passado deixa de condenar o futuro sozinho.

### 3. A/B Testing

- Grupo A: modelo antigo  
- Grupo B: modelo com piso  
- `scipy.stats.ttest_ind` → p-value  
- Só escala se p < 0.05 (diferença improvável de ser acaso)

---

## Conceitos-chave

| Conceito             | Tradução                                          | Por que importa                      |
| -------------------- | ------------------------------------------------- | ------------------------------------ |
| **Viés algorítmico** | Modelo reproduz preconceitos dos dados históricos | Produto novo pode virar invisível    |
| **A/B Testing**      | Dividir usuários e medir com rigor                | Evita escalar opinião no escuro      |
| **p-value**          | Chance de o resultado ser só sorte                | Separa melhoria real de coincidência |
| **IA responsável**   | Auditar modelos de propósito                      | Protege a empresa da própria inércia |

---

## PLUS deste capítulo

- Auditoria automática de exposição
- Simulação de conversão para o teste A/B
- Decisão de escala baseada em estatística, não em feeling

---

## Frase de ouro

> “Você não apenas corrigiu um bug. Você nos protegeu de nós mesmos.”  
> — Sr. Ricardo

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_14/README.md
