"""
Capítulo 5 — A Fila que Voou
Processamento paralelo de notas fiscais com ThreadPoolExecutor.
"""

import concurrent.futures
import os
import time
from pathlib import Path

PASTA = Path(__file__).parent / "notas"
PASTA.mkdir(exist_ok=True)


def processar_nota(caminho: str) -> str:
    """Simula leitura (I/O) + validação leve (CPU) + gravação (I/O)."""
    time.sleep(0.05)  # I/O: leitura do arquivo
    _ = sum(i * i for i in range(5_000))  # CPU leve
    time.sleep(0.05)  # I/O: inserção no banco
    return f"OK: {os.path.basename(caminho)}"


def processar_sequencial(notas: list) -> list:
    return [processar_nota(n) for n in notas]


def processar_paralelo(notas: list, max_workers: int = 8) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(processar_nota, notas))


def gerar_notas_fake(qtd: int = 40):
    arquivos = []
    for i in range(qtd):
        path = PASTA / f"nota_{i:04d}.xml"
        path.write_text(f"<nota id='{i}'/>")
        arquivos.append(str(path))
    return arquivos


if __name__ == "__main__":
    notas = gerar_notas_fake(40)

    print("=== Sequencial ===")
    t0 = time.perf_counter()
    processar_sequencial(notas)
    t_seq = time.perf_counter() - t0
    print(f"Tempo: {t_seq:.2f}s")

    print("\n=== Paralelo (ThreadPoolExecutor, 8 workers) ===")
    t0 = time.perf_counter()
    resultados = processar_paralelo(notas, max_workers=8)
    t_par = time.perf_counter() - t0
    print(f"Tempo: {t_par:.2f}s")
    print(f"Speedup: {t_seq / t_par:.1f}x")
    print(f"Notas processadas: {len(resultados)}")
