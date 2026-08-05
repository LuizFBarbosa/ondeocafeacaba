"""Gera feedbacks semanais anônimos para o Emocionômetro."""
from pathlib import Path
import hashlib
import random
import pandas as pd

PASTA = Path(__file__).parent
random.seed(42)

NOMES = ["Ana Silva", "Bruno Lima", "Carla Mendes", "David Oliveira",
         "Elena Costa", "Fábio Rocha", "Gabriela Santos", "Hugo Pereira"]
AREAS = ["Vendas", "Logística", "Financeiro", "TI", "RH"]
TEXTOS_POS = [
    "Semana produtiva, time alinhado.",
    "Gostei da nova ferramenta de pedidos.",
    "Reunião de feedback foi útil.",
    "Cliente satisfeito, meta batida.",
]
TEXTOS_NEU = [
    "Semana normal, nada de especial.",
    "Muita demanda, mas dentro do esperado.",
    "Sistemas ok, operação fluindo.",
]
TEXTOS_NEG = [
    "Pressão alta demais esta semana.",
    "Falta de comunicação entre áreas.",
    "Carga de trabalho insustentável.",
    "Me sinto invisível nas decisões.",
]

def anonimizar(nome: str) -> str:
    return hashlib.sha256(nome.encode()).hexdigest()[:12]

linhas = []
for semana in range(1, 9):
    for nome in NOMES:
        humor = random.choices([1, 2, 3, 4, 5], weights=[8, 15, 35, 30, 12])[0]
        if humor <= 2:
            texto = random.choice(TEXTOS_NEG)
        elif humor == 3:
            texto = random.choice(TEXTOS_NEU)
        else:
            texto = random.choice(TEXTOS_POS)
        linhas.append({
            "id_anon": anonimizar(nome),
            "area": random.choice(AREAS),
            "semana": semana,
            "humor": humor,
            "texto": texto,
        })

df = pd.DataFrame(linhas)
df.to_csv(PASTA / "feedbacks.csv", index=False)
print(f"✅ feedbacks.csv → {len(df)} linhas | humor médio: {df['humor'].mean():.2f}")
