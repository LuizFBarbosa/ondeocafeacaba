# Capítulo 8 — O Cérebro Digital

**API de ML • FastAPI • cache • Redis • joblib**

---

## Ideia central

O modelo de ML estava preso no notebook do Ziul.  
Transformou-se em **serviço**: qualquer sistema consulta e recebe sugestão em < 100 ms.

---

## Lição do cache

Cache em memória (dict Python) morre com o processo e não aguenta concorrência.  
**Redis** sobrevive a reinícios e escala.

> “Testei a API. Não testei a carga.”

---

## Como executar

```bash
pip install fastapi uvicorn pydantic
uvicorn api_sugestoes:app --reload
# Abra http://127.0.0.1:8000/docs e teste o POST /sugerir/
```

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_08/README.md
