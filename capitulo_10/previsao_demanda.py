"""
Capítulo 10 — A Bola de Cristal que Aprende
LSTM simplificada + fallback para cold start.
"""

from pathlib import Path
import numpy as np

# Tenta TensorFlow; se não estiver instalado, usa média móvel como fallback didático
try:
    from sklearn.preprocessing import MinMaxScaler
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.models import Sequential
    HAS_TF = True
except ImportError:
    HAS_TF = False
    print("⚠️  TensorFlow não encontrado — usando previsão por média móvel (didático).")

vendas = np.array([
    100, 120, 130, 125, 140, 150, 160, 155, 170, 180,
    190, 210, 220, 230, 225, 240, 250, 260, 255, 270,
    280, 300, 310, 320, 330, 340, 350, 360, 370, 380,
], dtype=float)

PASSO = 4


def prever_demanda(produto_id, historico_vendas):
    """Fallback para produto sem histórico (cold start)."""
    if historico_vendas is None or len(historico_vendas) < 4:
        return {
            "previsao": None,
            "aviso": "Histórico insuficiente — use média da categoria",
        }
    # média móvel simples (sempre funciona)
    media = float(np.mean(historico_vendas[-4:]))
    return {"previsao": int(media * 1.05), "aviso": None}  # +5% tendência


def treinar_lstm():
    if not HAS_TF:
        print("Pulando treino LSTM (TensorFlow ausente).")
        return None

    scaler = MinMaxScaler(feature_range=(0, 1))
    vendas_norm = scaler.fit_transform(vendas.reshape(-1, 1))

    X, y = [], []
    for i in range(len(vendas_norm) - PASSO):
        X.append(vendas_norm[i : i + PASSO, 0])
        y.append(vendas_norm[i + PASSO, 0])
    X = np.array(X).reshape(-1, PASSO, 1)
    y = np.array(y)

    modelo = Sequential([
        LSTM(32, input_shape=(PASSO, 1), return_sequences=False),
        Dropout(0.2),
        Dense(1),
    ])
    modelo.compile(optimizer="adam", loss="mean_squared_error")
    modelo.fit(X, y, epochs=30, batch_size=1, verbose=0)
    print("✅ LSTM treinada.")
    return modelo, scaler


if __name__ == "__main__":
    print("=== Cold start (produto novo) ===")
    print(prever_demanda(9901, None))

    print("\n=== Produto com histórico ===")
    print(prever_demanda(1023, vendas.tolist()))

    print("\n=== Treino LSTM (se disponível) ===")
    treinar_lstm()
