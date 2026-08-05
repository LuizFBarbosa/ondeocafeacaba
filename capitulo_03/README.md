# Capítulo 3 — O Mensageiro Digital

**APIs REST • FastAPI • Pydantic • Requests • JSON**

---

## O problema do livro

O ERP era antigo. O CRM era moderno. Os dois não conversavam.  
Preço no CRM era atualizado uma vez por dia via CSV manual.  
Se a precificação mudasse às 10h, os vendedores vendiam errado até o dia seguinte.

Márcia: *“Nossos sistemas operam como ilhas. Preciso de uma ponte.”*

---

## A metáfora do restaurante

| Papel   | Sistema   |
| ------- | --------- |
| Cliente | CRM / RCA |
| Garçom  | **API**   |
| Cozinha | ERP       |

O cliente nunca entra na cozinha. Ele pede ao garçom. O garçom busca e entrega.

---

## Como executar

```bash
# Terminal 1 — sobe a API
pip install fastapi uvicorn requests
uvicorn api_precos:app --reload

# Terminal 2 — consulta como o CRM faria
python cliente_crm.py
```

Abra também: http://127.0.0.1:8000/docs (documentação automática interativa)

---

## Endpoints

| Método | Rota                   | Descrição             |
| ------ | ---------------------- | --------------------- |
| GET    | `/`                    | Informações da API    |
| GET    | `/precos`              | Lista todos os preços |
| GET    | `/precos/{produto_id}` | Preço de um produto   |

---

## Lições do capítulo

- **Sempre TRIM** — espaços no final de IDs quebram integração
- A solução mais inteligente muitas vezes não é trocar o sistema: é construir a **ponte certa**
- FastAPI gera documentação automática (`/docs`) — ouro para quem integra

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_03/README.md
