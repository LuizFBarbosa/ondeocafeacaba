# Capítulo 6 — O Caçador de Erros

**Auditoria de dados • logging • try/except • throttle de alertas**

---

## Problemas do livro

1. Pedidos duplicados sob alta carga  
2. Logging configurado **depois** da primeira chamada → log vazio  
3. 47 e-mails iguais → **alert fatigue** (Sr. Ricardo criou regra no Outlook)  
4. Falso senso de cobertura (monitoramento periódico vs eventos reais)

---

## Como executar

```bash
python auditor.py
```

O log é gravado em `auditoria.log`.

---

## Lição

> Mais alerta ≠ mais segurança.  
> Um sistema que grita demais ensina as pessoas a ignorar.

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_06/README.md
