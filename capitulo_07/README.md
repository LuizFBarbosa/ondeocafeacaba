# Capítulo 7 — O Radar de Oportunidades

**Machine Learning • scikit-learn • Random Forest • SMOTE**

---

## Problema

Campanha genérica: 2,3% de conversão.  
Ziul propôs: lista dos 500 clientes com maior chance de comprar de novo.

---

## Armadilhas mostradas no livro

1. **Data leakage** → 97% de acurácia falsa  
2. **Desequilíbrio de classe** → modelo “mentiroso”  
3. **Split único** → “foi sorte de terça-feira?”

Solução: SMOTE + StratifiedKFold + intervalo de confiança.

---

## Como executar

```bash
pip install scikit-learn imbalanced-learn joblib pandas
python gerar_dados.py
python radar_oportunidades.py
```

---

## Frase de ouro

> “Uma métrica sem intervalo de confiança é uma opinião com casas decimais.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_07/README.md
