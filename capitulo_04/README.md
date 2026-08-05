# Capítulo 4 — Uma Casa Decimal de Distância

**Governança de preços • circuit breaker • validação de campanhas**

---

## O problema do livro

Wagner ditou “0,02” (2%). Márcia digitou e a célula mostrou “0,2” (20%).  
Em menos de um dia, mais de mil pedidos saíram com desconto dez vezes maior.  
Prejuízo estimado: **R$ 190 mil** de margem.  

Seu Bento decidiu: *“O cliente não teve culpa. O erro foi nosso. Vamos entregar.”*

---

## O que o código implementa

1. **Validação de desconto** — exige confirmação acima do limite usual  
2. **Campanha registrada** — cada promoção entra com limites de desconto e volume  
3. **Circuit breaker** — pausa só aquela combinação produto+praça, **sem cancelar** o que já foi vendido  

---

## Como executar

```bash
python circuit_breaker.py
```

---

## Lição central

> O verdadeiro problema foi **ausência de validação**, não Python, nem ERP, nem a planilha.

Alguns dos sistemas mais importantes de uma empresa não têm uma linha de código.  
Têm um nome pendurado numa fachada e alguém disposto a honrá-lo mesmo quando custa caro.

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_04/README.md
