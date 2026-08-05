"""
Capítulo 12 — O Jogo das Ideias
Gamificação de visitas de RCA com validação GPS + ranking em SQLite.

PLUS deste capítulo:
  - Validação de proximidade GPS (haversine)
  - Anti-fraude: não conta ponto se a distância for absurda
  - Ranking e histórico por RCA
"""

import math
import sqlite3
from datetime import datetime
from pathlib import Path

DB = Path(__file__).parent / "pontos.db"

CLIENTES_GPS = {
    "Mercado Bom Preço": (-23.5505, -46.6333),
    "Padaria Central": (-23.5489, -46.6388),
    "Minimercado São José": (-23.5610, -46.6550),
    "Atacarejo Norte": (-23.5200, -46.6100),
    "Empório da Vila": (-23.5700, -46.6400),
}


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Distância em km entre dois pontos GPS (fórmula de Haversine)."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


def init_db():
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS pontos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rca TEXT NOT NULL,
            data TEXT NOT NULL,
            pontos INTEGER NOT NULL,
            motivo TEXT,
            cliente TEXT,
            distancia_km REAL,
            valido INTEGER DEFAULT 1
        )
    """)
    con.commit()
    con.close()


def registrar_visita(
    rca: str,
    cliente: str,
    lat_rca: float,
    lon_rca: float,
    pontos_base: int = 10,
    raio_max_km: float = 0.5,
) -> dict:
    """
    Registra visita com validação GPS.
    Se o RCA estiver a mais de raio_max_km do cliente → visita inválida (anti-fraude).
    """
    if cliente not in CLIENTES_GPS:
        return {"ok": False, "msg": f"Cliente '{cliente}' não cadastrado no GPS."}

    lat_cli, lon_cli = CLIENTES_GPS[cliente]
    dist = haversine_km(lat_rca, lon_rca, lat_cli, lon_cli)
    valido = dist <= raio_max_km
    pontos = pontos_base if valido else 0
    motivo = "visita validada GPS" if valido else f"GPS fora do raio ({dist:.2f} km)"

    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO pontos (rca, data, pontos, motivo, cliente, distancia_km, valido) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            rca,
            datetime.now().isoformat(timespec="seconds"),
            pontos,
            motivo,
            cliente,
            round(dist, 3),
            int(valido),
        ),
    )
    con.commit()
    con.close()

    return {
        "ok": valido,
        "rca": rca,
        "cliente": cliente,
        "distancia_km": round(dist, 3),
        "pontos": pontos,
        "motivo": motivo,
    }


def ranking(top: int = 10) -> list:
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT rca, SUM(pontos) as total, COUNT(*) as visitas, "
        "SUM(CASE WHEN valido=1 THEN 1 ELSE 0 END) as validas "
        "FROM pontos GROUP BY rca ORDER BY total DESC LIMIT ?",
        (top,),
    ).fetchall()
    con.close()
    return rows


def historico_rca(rca: str) -> list:
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT data, cliente, pontos, motivo, distancia_km FROM pontos "
        "WHERE rca=? ORDER BY data DESC LIMIT 20",
        (rca,),
    ).fetchall()
    con.close()
    return rows


if __name__ == "__main__":
    # Limpa DB de demos anteriores para resultado previsível
    if DB.exists():
        DB.unlink()
    init_db()

    print("=== Simulação de visitas com GPS ===\n")

    r1 = registrar_visita("Ana", "Mercado Bom Preço", -23.5506, -46.6334)
    print(f"Ana @ Mercado Bom Preço → {r1}")

    r2 = registrar_visita("Bruno", "Padaria Central", -23.50, -46.60)
    print(f"Bruno @ Padaria Central → {r2}")

    r3 = registrar_visita("Ana", "Empório da Vila", -23.5701, -46.6402)
    print(f"Ana @ Empório da Vila → {r3}")

    r4 = registrar_visita("Carla", "Atacarejo Norte", -23.5201, -46.6102)
    print(f"Carla @ Atacarejo Norte → {r4}")

    print("\n=== Ranking ===")
    for rca, total, visitas, validas in ranking():
        print(f"  {rca:10s}  {total:3d} pts  ({validas}/{visitas} visitas válidas)")

    print("\n=== Histórico da Ana ===")
    for row in historico_rca("Ana"):
        print(f"  {row}")
