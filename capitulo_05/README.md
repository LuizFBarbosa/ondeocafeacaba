# Capítulo 5 — Quando o Tempo Corre Demais

**Paralelismo • concurrent.futures • ThreadPoolExecutor**

---

## O problema

3.000 notas fiscais processadas em sequência (~7 s cada) → mais de 6 horas.  
O servidor tinha 16 núcleos, mas só um trabalhava.

---

## Solução

`ThreadPoolExecutor` com `max_workers` controlado (I/O-bound).  
No livro: de 6 horas para **25 minutos**.

---

## Como executar

```bash
python processar_notas.py
```

---

## Conceitos

| Ferramenta              | Quando usar                                 |
| ----------------------- | ------------------------------------------- |
| **ThreadPoolExecutor**  | Tarefas I/O-bound (arquivo, rede, banco)    |
| **ProcessPoolExecutor** | Tarefas CPU-bound (cálculos pesados)        |
| **GIL**                 | Limitação do Python com threads em CPU puro |

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_05/README.md
