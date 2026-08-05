# Capítulo 16 — O DNA do Conhecimento

**Recomendação • personalização • pandas • Streamlit**

---

## O problema do livro

Sr. Ricardo: *“O que garante que daqui a três anos não seremos a próxima Kodak?”*

A resposta não era mais tecnologia. Era a capacidade da empresa de **aprender** — e de não deixar o conhecimento preso em algumas cabeças.

---

## O erro da primeira versão

O algoritmo recomendava o conteúdo **mais avançado** da habilidade mais fraca.  
Ana (nota 3,5 em venda estratégica) recebeu webinar de 90 minutos sobre “Psicologia da Persuasão em Vendas B2B Complexas”.

Abriu. Assistiu dois minutos. Fechou.  
Taxa de conclusão: **12%**.

Correção: básico primeiro + máximo 20 minutos na primeira sugestão.  
Taxa foi para **71%**.

---

## Como executar

```bash
pip install pandas
python dna_conhecimento.py
```

---

## Explicação passo a passo

### 1. Encontrar a habilidade mais fraca

```python
habilidade_fraca = min(performance, key=performance.get)
```

### 2. Ordenar do mais acessível para o mais avançado

```python
recs = catalogo[catalogo["habilidade"] == habilidade_fraca]
recs = recs.sort_values(["nivel", "duracao_min"]).query("duracao_min <= 20")
```

### 3. O espelho (PLUS do livro)

Ziul rodou o sistema na própria equipe de TI.  
Habilidade mais fraca do Júnior: **comunicação com áreas de negócio**.  
O algoritmo não sabe o nome. Só sabe os dados. E os dados falaram.

---

## Conceitos-chave

| Conceito                    | Tradução                                     | Por que importa                               |
| --------------------------- | -------------------------------------------- | --------------------------------------------- |
| **Sistema de recomendação** | Cruza desempenho com catálogo de conteúdo    | Treinamento individual, não genérico          |
| **Ordenação por nível**     | Básico antes de avançado                     | Conteúdo difícil demais vira abandono         |
| **Taxa de conclusão**       | % do conteúdo que a pessoa realmente termina | Termômetro real do sistema                    |
| **DNA corporativo**         | Aprendizado contínuo, não evento isolado     | Conhecimento sobrevive à saída de qualquer um |

---

## PLUS deste capítulo

- Estimativa de taxa de conclusão por nível/duração
- Dois perfis de exemplo (Ana + Júnior)
- Ordenação explícita Básico → Avançado

---

## Frase de ouro

> “O melhor teste de um sistema de recomendação não é rodar nos clientes.  
> É rodar em quem construiu ele e ver se ainda funciona quando o espelho aponta pra dentro.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_16/README.md
