# Capítulo 17 — O Condutor Invisível

**Celery • Celery Beat • Redis • automação de rotinas**

---

## O problema do livro

Sr. Ricardo: *“Cada peça dessa sinfonia funciona lindamente... mas eu preciso levantar a batuta toda vez pra a música começar.”*

Relatório, auditoria, sugestão de compra, emocionômetro — cada um no seu agendador, sem se falar.  
Quatro notificações ao mesmo tempo. Ninguém sabia qual olhar primeiro.

Faltava um **maestro**.

---

## A solução

Sistema nervoso autônomo: rotinas críticas acontecem no horário certo sem depender de ninguém lembrar.

| Componente      | Papel                                    |
| --------------- | ---------------------------------------- |
| **Celery**      | Executa trabalho em segundo plano        |
| **Celery Beat** | Define *quando* cada tarefa roda         |
| **Redis**       | Fila que entrega a ordem ao worker certo |
| **crontab**     | Expressão de horário precisa e auditável |

---

## Como executar

```bash
python tasks.py
```

(A versão completa com Celery+Redis está comentada no código para referência.)

---

## Explicação passo a passo

### 1. Cada tarefa é uma função pura

```python
def gerar_relatorio_diario():
    # reutiliza a lógica do Capítulo 1
    ...
```

### 2. O schedule é a partitura

```python
SCHEDULE = [
    {"nome": "relatorio-diario", "hora": "07:30", "task": gerar_relatorio_diario},
    ...
]
```

### 3. Lição do check-in automático (do livro)

Ziul automatizou conversas de carreira com RCAs novos.  
Engajamento (número de respostas): 98%.  
Qualidade do que era dito: quase zero.

> “Processo se automatiza. Gente que escuta gente, não.”

Ele desligou a automação e contratou pessoa para acompanhamento presencial.

---

## Conceitos-chave

| Conceito                  | Tradução                      | Por que importa                             |
| ------------------------- | ----------------------------- | ------------------------------------------- |
| **Celery**                | Worker em background          | Libera o sistema principal                  |
| **Beat**                  | Agendador                     | Substitui lembretes manuais                 |
| **Broker (Redis)**        | Fila de mensagens             | Garante entrega mesmo com vários servidores |
| **Automação responsável** | Saber o que *não* automatizar | Conversa humana ≠ pesquisa de satisfação    |

---

## PLUS deste capítulo

- Roda sem Redis (demo pura em Python)
- Inclui emocionômetro no schedule
- Referência Celery real comentada no código

---

## Frase de ouro

> “A melhor automação é aquela que você esquece que existe — mas sente em tudo que funciona.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_17/README.md
