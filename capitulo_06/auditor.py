"""
Capítulo 6 — O Guardião da Base
Auditoria com logging + throttle de alertas (evita os 47 e-mails).
"""

from datetime import datetime, timedelta
import logging
from pathlib import Path

PASTA = Path(__file__).parent
LOG_FILE = PASTA / "auditoria.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    force=True,
)

_ULTIMO_ALERTA: dict[str, datetime] = {}
JANELA_DE_COOLDOWN = timedelta(hours=2)


def deve_alertar(tipo_erro: str) -> bool:
    agora = datetime.now()
    ultimo = _ULTIMO_ALERTA.get(tipo_erro)
    if ultimo is None or (agora - ultimo) > JANELA_DE_COOLDOWN:
        _ULTIMO_ALERTA[tipo_erro] = agora
        return True
    return False


def enviar_alerta_com_throttle(tipo_erro: str, mensagem: str):
    logging.warning(mensagem)  # log sempre registra tudo
    if deve_alertar(tipo_erro):
        # Em produção: enviar_email(...)
        logging.info(f"E-mail enviado para: {tipo_erro}")
        print(f"📧 E-MAIL: {mensagem}")
    else:
        logging.info(f"Alerta agrupado (cooldown): {tipo_erro}")
        print(f"⏳ Agrupado (cooldown): {tipo_erro}")


def detectar_duplicados(pedidos: list[dict]) -> list:
    vistos = set()
    duplicados = []
    for p in pedidos:
        chave = (p["cliente"], p["produto"], p["horario"])
        if chave in vistos:
            duplicados.append(p)
        else:
            vistos.add(chave)
    return duplicados


if __name__ == "__main__":
    pedidos = [
        {"cliente": "A", "produto": "X", "horario": "10:00", "id": 1},
        {"cliente": "A", "produto": "X", "horario": "10:00", "id": 2},  # duplicado
        {"cliente": "B", "produto": "Y", "horario": "11:00", "id": 3},
        {"cliente": "A", "produto": "X", "horario": "10:00", "id": 4},  # duplicado
    ]

    dups = detectar_duplicados(pedidos)
    print(f"Duplicados encontrados: {len(dups)}")

    for _ in range(5):
        enviar_alerta_com_throttle(
            "pedido_duplicado",
            f"Detectados {len(dups)} pedidos duplicados",
        )
