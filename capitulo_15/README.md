# Capítulo 15 — O Mentor Digital

**RAG • LLMs • ZiulBot • assistente conversacional**

---

## O problema do livro

RCAs gastavam tempo demais ligando para o back-office: estoque, preço, promoção.  
A informação existia. O acesso era lento. Tempo morto em campo = venda perdida.

---

## A ideia: ZiulBot

Não um bot de menu. Um assistente que entende português natural e responde com a **verdade do sistema** — estoque real, preço real, promoção real.

Tecnologia por trás: **RAG (Retrieval-Augmented Generation)**

1. **Retrieval** — busca na base da empresa o que é relevante  
2. **Generation** — gera a resposta só com o que encontrou  

Diferença crucial: o bot **não inventa**. Se não sabe, admite.

---

## Como executar

```bash
python ziulbot.py
```

---

## Explicação passo a passo

### Retrieval (busca)

```python
def recuperar_produto(pergunta: str) -> Optional[str]:
    for alias, canonico in ALIASES.items():
        if alias in pergunta.lower():
            return canonico
    return None
```

Em produção: busca vetorial (embeddings) em catálogo + estoque + promoções.

### Generation (resposta ancorada)

```python
qtd = estoque.get(produto, 0)
if qtd <= 0:
    return "está em falta..."  # dado real, não chute
```

### Anti-alucinação

```python
if produto is None:
    return "Não encontrei... Pode reformular?"
```

No livro, a IA respondeu com confiança que um produto era isento de imposto — e não era.  
Lição: resposta **provável** ≠ resposta **garantida**. Confirmação humana em temas fiscais.

---

## Conceitos-chave

| Conceito               | Tradução                     | Por que importa                                     |
| ---------------------- | ---------------------------- | --------------------------------------------------- |
| **LLM**                | Modelo que sabe conversar    | Entende pergunta em linguagem natural               |
| **RAG**                | Ancorar o LLM em dados reais | Evita alucinação                                    |
| **Latência**           | Tempo de resposta            | Se demora, ninguém usa                              |
| **Confirmação humana** | Pessoa valida temas críticos | Imposto, contrato, saúde — não automatiza no escuro |

---

## PLUS deste capítulo

- Sinônimos (aliases) para retrieval mais robusto
- Produto em falta tratado explicitamente
- Resposta “não sei” quando está fora da base

---

## Frase de ouro

> “Quando o bot resolve, o humano evolui. O bot dá informação. O RCA vende.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_15/README.md
