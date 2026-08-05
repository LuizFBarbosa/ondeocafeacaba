"""
Capítulo 13 — A Máquina de Sentir (Emocionômetro)
Anonimização + análise de humor + alerta de área em risco.

PLUS:
  - Score de sentimento lexical simples (sem depender de BERT pesado)
  - Alerta automático quando área cai abaixo do limiar
  - Tendência por área ao longo das semanas
"""

from pathlib import Path
import hashlib
import pandas as pd

PASTA = Path(__file__).parent
DADOS = PASTA / "feedbacks.csv"

# Léxico simples em português (PLUS didático — em produção usaria BERTimbau)
POSITIVAS = {"produtiva", "alinhado", "gostei", "útil", "satisfeito", "meta", "ok", "fluindo"}
NEGATIVAS = {"pressão", "falta", "insustentável", "invisível", "alta", "comunicação"}


def anonimizar(nome: str) -> str:
    """Hash irreversível — mesmo nome = mesmo ID, mas não revela quem é."""
    return hashlib.sha256(nome.encode("utf-8")).hexdigest()[:12]


def score_texto(texto: str) -> float:
    """Score lexical simples: positivo sobe, negativo desce. Faixa aprox. -1 a +1."""
    palavras = set(texto.lower().replace(",", "").replace(".", "").split())
    pos = len(palavras & POSITIVAS)
    neg = len(palavras & NEGATIVAS)
    total = pos + neg
    if total == 0:
        return 0.0
    return (pos - neg) / total


def analisar(caminho: Path = DADOS, limiar_humor: float = 2.8):
    df = pd.read_csv(caminho)
    df["score_texto"] = df["texto"].apply(score_texto)

    print("=" * 55)
    print("  EMOCIONÔMETRO — Atacado São Bento")
    print("=" * 55)

    print(f"\n📊 Humor médio geral: {df['humor'].mean():.2f}")
    print(f"📝 Score textual médio: {df['score_texto'].mean():.2f}")

    print("\n🏢 Por área (média de humor):")
    por_area = df.groupby("area")["humor"].mean().sort_values()
    for area, media in por_area.items():
        status = "🔴 ALERTA" if media < limiar_humor else "🟢"
        print(f"  {status}  {area:12s}  {media:.2f}")

    print("\n📈 Tendência (últimas 3 semanas vs 3 anteriores):")
    max_sem = df["semana"].max()
    recente = df[df["semana"] > max_sem - 3]["humor"].mean()
    anterior = df[df["semana"] <= max_sem - 3]["humor"].mean()
    delta = recente - anterior
    seta = "↑" if delta > 0 else "↓" if delta < 0 else "→"
    print(f"  Anterior: {anterior:.2f}  |  Recente: {recente:.2f}  |  {seta} {delta:+.2f}")

    # Áreas em alerta
    alertas = por_area[por_area < limiar_humor]
    if len(alertas):
        print(f"\n⚠️  {len(alertas)} área(s) abaixo do limiar ({limiar_humor}).")
        print("   Ação sugerida: conversa individual (humana), não e-mail automático.")
    else:
        print("\n✅ Nenhuma área abaixo do limiar.")

    print("\n🔒 Garantia: nenhum nome real aparece neste dataset.")
    print(f"   IDs anônimos (amostra): {df['id_anon'].unique()[:3].tolist()}")
    return df


if __name__ == "__main__":
    if not DADOS.exists():
        print("Execute antes: python gerar_dados.py")
    else:
        analisar()
