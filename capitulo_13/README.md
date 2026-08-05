# Capítulo 13 — A Máquina de Sentir

**Emocionômetro • BERTimbau • regressão linear • anonimização**

---

## O problema do livro

A empresa media vendas, estoque, margem — mas não media **como as pessoas estavam**.  
Pedro quase saiu sem ninguém perceber a tempo.

O Emocionômetro nasceu para uma única finalidade (comentário no código do livro):

> garantir que nenhuma pessoa precise chegar ao limite  
> antes de alguém perceber que ela está sofrendo.

---

## O que este código faz

1. Gera feedbacks semanais **já anonimizados**
2. Calcula humor médio por área
3. Aplica score lexical simples nos textos
4. Detecta tendência (melhorando ou piorando)
5. Emite alerta quando área cai abaixo do limiar

---

## Como executar

```bash
pip install pandas
python gerar_dados.py
python emocionometro.py
```

---

## Explicação passo a passo

### 1. Anonimização por hash

```python
def anonimizar(nome: str) -> str:
    return hashlib.sha256(nome.encode()).hexdigest()[:12]
```

- Mesmo nome → mesmo ID (permite tendência individual sem identidade)
- Hash **não é reversível** na prática
- O dataset analítico **nunca** carrega nome, CPF ou matrícula

### 2. Score textual (PLUS didático)

Em produção o livro usa **BERTimbau** (modelo de linguagem em português).  
Aqui usamos um léxico leve para rodar sem GPU e sem download de modelo:

```python
POSITIVAS = {"produtiva", "alinhado", "gostei", ...}
NEGATIVAS = {"pressão", "falta", "insustentável", ...}
score = (pos - neg) / (pos + neg)
```

### 3. Alerta com responsabilidade

Quando uma área fica abaixo do limiar, a ação sugerida **não** é e-mail automático.  
É conversa humana. O sistema só aponta; a liderança age.

---

## Conceitos-chave

| Conceito             | Tradução                                        | Por que importa                       |
| -------------------- | ----------------------------------------------- | ------------------------------------- |
| **Anonimização**     | Remover identidade dos dados                    | LGPD + confiança de quem responde     |
| **BERTimbau**        | Modelo de linguagem treinado em português       | Entende sentimento em texto real      |
| **Limiar de alerta** | Valor abaixo do qual alguém precisa olhar       | Evita “só métrica” sem ação           |
| **Confiança**        | Pessoas só respondem com honestidade se confiam | Quebrar a confiança destrói o sistema |

---

## PLUS deste capítulo

- Gerador de feedbacks realistas
- Tendência temporal (melhorando/piorando)
- Score lexical como proxy leve do BERTimbau

---

## Frase de ouro

> “Nunca quebre a confiança das pessoas que respondem toda sexta.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_13/README.md
