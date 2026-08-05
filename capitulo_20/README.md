# Capítulo 20 — O Universo Paralelo

**Simulação Monte Carlo • análise de risco • decisão sob incerteza**

---

## O problema do livro

Sr. Ricardo: *“200 mil unidades de refrigerante paradas. Queima com 30% de desconto. Quase um milhão em margem reduzida. O que você acha?”*

Dona Fátima: *“E se for fracasso? E se for sucesso demais e faltar produto?”*

Não faltava informação. Faltava um jeito seguro de **testar o futuro sem pagar por ele no mundo real**.

---

## A ideia: mil universos antes de gastar um real

Simulação de Monte Carlo com **agentes**:

- Cada cliente simulado tem sensibilidade diferente a preço  
- Roda o cenário milhares de vezes  
- Resultado: **distribuição** de possibilidades, não um número único  

---

## O erro da primeira versão

Ziul perguntou ao simulador: *“Se eu subir 10% o preço do produto 1023, o que acontece?”*  
Resposta: volume cai 3%.  

Na realidade o 1023 era item básico — cliente compra mesmo com reajuste moderado.  
O modelo tratava **todos os produtos iguais**. Não são.

Lição: ferramenta que admite o que não sabe > ferramenta que finge saber tudo.

---

## Como executar

```bash
pip install pandas
python monte_carlo.py
```

---

## Explicação passo a passo

### 1. Agente = cliente com personalidade

```python
@dataclass
class AgenteCliente:
    sensibilidade: float   # 0.5–1.5
    chance_base: float     # probabilidade sem desconto

    def vai_comprar(self, desconto):
        chance = chance_base * (1 + desconto * sensibilidade * 3)
        return random.random() < chance
```

### 2. Uma simulação = um universo possível

Estoque começa em 200 mil. Clientes “chegam”. Compram ou não.  
Se o estoque zera → **ruptura**.

### 3. Centenas de simulações = mapa de risco

| Métrica          | O que responde           |
| ---------------- | ------------------------ |
| Lucro médio      | Expectativa central      |
| P5 (pior)        | Quão ruim pode ficar     |
| P95 (melhor)     | Quão bom pode ficar      |
| Risco de ruptura | Chance de faltar produto |

No livro, Sr. Ricardo escolheu **20%** — menos agressivo, risco controlável.  
Três meses depois: venderam 94% do estoque, dentro da faixa mais provável.

---

## Conceitos-chave

| Conceito                  | Tradução                                               | Por que importa                            |
| ------------------------- | ------------------------------------------------------ | ------------------------------------------ |
| **Monte Carlo**           | Rodar cenário milhares de vezes com variação aleatória | Mostra o leque, não um chute único         |
| **Agentes**               | Clientes artificiais com comportamentos diferentes     | Representa heterogeneidade real do mercado |
| **Risco de ruptura**      | Chance de faltar produto                               | Logística precisa se preparar              |
| **Decisão sob incerteza** | Escolher sabendo que há vários futuros                 | Tira a empresa da aposta cega              |

---

## PLUS deste capítulo

- Percentis P5 / P50 / P95
- Comparação automática 30% vs 20%
- Recomendação textual baseada no risco relativo
- Margem unitária reportada

---

## Frase de ouro

> “A simulação não dá a resposta certa — ela nos torna sábios sobre as perguntas a fazer.”  
>  
> “A gente não comprou uma resposta. Comprou uma bússola.” — Dona Fátima

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_20/README.md
