#!/usr/bin/env python3
"""
Confere se cada QR Code em qrcodes/ realmente aponta para a URL esperada
do repositório no GitHub. Usado no CI para evitar que um QR Code impresso
no livro fique "quebrado" (apontando para o repositório errado, branch
errada ou capítulo errado).

Uso:
    pip install pyzbar pillow
    python scripts/checar_qrcodes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from pyzbar.pyzbar import decode

RAIZ = Path(__file__).resolve().parent.parent
PASTA_QR = RAIZ / "qrcodes"
BASE = "https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main"

ESPERADOS = {"00_readme_principal.png": f"{BASE}/README.md"}
for i in range(1, 22):
    ESPERADOS[f"capitulo_{i:02d}.png"] = f"{BASE}/capitulo_{i:02d}/README.md"


def main() -> int:
    problemas = []
    for arquivo, url_esperada in sorted(ESPERADOS.items()):
        caminho = PASTA_QR / arquivo
        if not caminho.exists():
            problemas.append(f"{arquivo}: arquivo não encontrado em qrcodes/")
            continue
        resultado = decode(Image.open(caminho))
        if not resultado:
            problemas.append(f"{arquivo}: não foi possível decodificar o QR Code")
            continue
        url_lida = resultado[0].data.decode()
        if url_lida != url_esperada:
            problemas.append(
                f"{arquivo}: aponta para '{url_lida}', esperado '{url_esperada}'"
            )
        else:
            print(f"  ✅ {arquivo} -> {url_lida}")

    if problemas:
        print("\n❌ Problemas encontrados:")
        for p in problemas:
            print(f"  - {p}")
        return 1
    print("\n✅ Todos os QR Codes apontam para a URL correta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
