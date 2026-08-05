# Capítulo 12 — O Jogo das Ideias

**Gamificação • pandas • Streamlit • SQLite • validação GPS**

---

## O problema do livro

RCAs ganhavam pontos por “bater ponto” de visita.  
Quatro deles combinaram no WhatsApp de registrar visitas fictícias uns pelos outros — fraude organizada, pequena, mas real.

Ziul admitiu: *“Eu desenhei um jogo que dava mais pontos por aparecer fazendo do que por fazer de verdade.”*

A solução não foi só punir: foi **mudar a régua** — validar a visita com GPS.

---

## O que este código faz

1. Armazena pontos de RCA em SQLite
2. Calcula distância real (Haversine) entre o celular do RCA e o cliente
3. Só conta o ponto se estiver dentro de 500 m
4. Gera ranking e histórico

---

## Arquivos

| Arquivo          | Descrição                                 |
| ---------------- | ----------------------------------------- |
| `gamificacao.py` | Motor de pontos + validação GPS + ranking |
| `pontos.db`      | Banco SQLite (criado automaticamente)     |
| `README.md`      | Este arquivo                              |

---

## Como executar

```bash
python gamificacao.py
```

### Saída esperada

```
=== Simulação de visitas com GPS ===

Ana @ Mercado Bom Preço → {'ok': True, 'pontos': 10, ...}
Bruno @ Padaria Central → {'ok': False, 'pontos': 0, 'motivo': 'GPS fora do raio ...'}
...

=== Ranking ===
  Ana         20 pts  (2/2 visitas válidas)
  Carla       10 pts  (1/1 visitas válidas)
  Bruno        0 pts  (0/1 visitas válidas)
```

---

## Explicação passo a passo

### 1. Fórmula de Haversine

Calcula a distância em linha reta (km) entre duas coordenadas GPS.  
É a mesma matemática usada por apps de corrida e delivery.

```python
dist = haversine_km(lat_rca, lon_rca, lat_cliente, lon_cliente)
valido = dist <= 0.5  # 500 metros
```

### 2. Anti-fraude

Se o RCA registra visita estando a 5 km do cliente, o sistema:
- grava o registro (auditoria)
- **não dá ponto**
- marca `valido = 0`

No livro, isso substituiu a confiança cega por evidência.

### 3. Ranking justo

```sql
SELECT rca, SUM(pontos), COUNT(*),
       SUM(CASE WHEN valido=1 THEN 1 ELSE 0 END)
FROM pontos GROUP BY rca ORDER BY total DESC
```

Só pontos de visitas válidas entram no placar.

---

## Conceitos-chave

| Conceito             | Tradução                                                            | Por que importa                                            |
| -------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Gamificação**      | Usar mecânicas de jogo (pontos, ranking) para motivar comportamento | Pode motivar — ou ensinar a trapacear, se a régua for ruim |
| **Haversine**        | Fórmula de distância entre dois pontos na esfera terrestre          | Valida presença física sem hardware caro                   |
| **SQLite**           | Banco de dados embutido em um arquivo                               | Zero instalação de servidor para protótipos                |
| **Régua do sistema** | O que o sistema premia, as pessoas otimizam                         | Desenhar a métrica é tão importante quanto o código        |

---

## PLUS deste capítulo

- Validação GPS com raio configurável
- Histórico por RCA para auditoria
- Registro mesmo de tentativas inválidas (rastreabilidade)

---

## Frase de ouro

> “Toda régua ensina alguém a medir errado, se a régua for mal pensada.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_12/README.md
