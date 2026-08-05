# Capítulo 10 — A Máquina que Aprende Sozinha

**LSTM • TensorFlow/Keras • overfitting • cold start**

---

## Problemas enfrentados

1. **Overfitting temporal** — modelo memorizava o passado  
2. **Cold start** — produto novo → NaN silencioso (mais perigoso que erro)

---

## Post-it do Ziul

> “O modelo não sabe que não sabe. Cuide disso antes de ele ir pra produção.”

---

## Como executar

```bash
# Com TensorFlow (recomendado)
pip install tensorflow scikit-learn numpy
python previsao_demanda.py

# Sem TensorFlow: o script usa média móvel automaticamente
```

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_10/README.md
