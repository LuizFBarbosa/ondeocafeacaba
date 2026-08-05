"""
Capítulo 7 — O Código que Aprende
Random Forest + SMOTE + validação cruzada estratificada.
"""

from pathlib import Path
import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

PASTA = Path(__file__).parent
DADOS = PASTA / "clientes_inativos.csv"
MODELO = PASTA / "modelo_oportunidades.pkl"


def treinar_modelo(caminho: Path = DADOS):
    df = pd.read_csv(caminho)
    X = df[["produto_preco", "cliente_frequencia", "tempo_ultima_compra"]]
    y = df["comprou"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    X_tr, y_tr = SMOTE(random_state=42).fit_resample(X_tr, y_tr)

    m = RandomForestClassifier(n_estimators=100, random_state=42)
    m.fit(X_tr, y_tr)

    pred = m.predict(X_te)
    print(f"Acurácia (split único): {accuracy_score(y_te, pred):.2%}")
    print(classification_report(y_te, pred, digits=3))
    joblib.dump(m, MODELO)
    print(f"Modelo salvo em {MODELO}")
    return m


def validar_com_k_fold(caminho: Path = DADOS, n_splits: int = 5):
    """'74% foi sorte de terça-feira?' — pergunta do Sr. Ricardo."""
    df = pd.read_csv(caminho)
    X = df[["produto_preco", "cliente_frequencia", "tempo_ultima_compra"]]
    y = df["comprou"]

    pipeline = ImbPipeline([
        ("smote", SMOTE(random_state=42)),
        ("modelo", RandomForestClassifier(n_estimators=100, random_state=42)),
    ])
    kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=kfold, scoring="accuracy")
    print(f"Acurácia média (k-fold): {scores.mean():.2%} ± {scores.std():.2%}")
    return scores


if __name__ == "__main__":
    print("=== Treino ===")
    treinar_modelo()
    print("\n=== Validação cruzada ===")
    validar_com_k_fold()
