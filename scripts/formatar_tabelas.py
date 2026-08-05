#!/usr/bin/env python3
"""
Realinha todas as tabelas Markdown de um arquivo (ou pasta) para o formato
"grid alinhado" — cada coluna com a mesma largura visual, como uma planilha.

Isso NÃO muda como o GitHub renderiza a tabela (o Markdown já renderiza como
grid de qualquer forma). O que muda é a aparência do arquivo .md quando aberto
em um editor de texto puro / bloco de notas / Word: em vez de colunas com
tamanhos diferentes, os "|" ficam todos alinhados verticalmente.

Uso:
    python formatar_tabelas.py caminho/para/arquivo.md
    python formatar_tabelas.py caminho/para/pasta   # processa todo *.md recursivamente
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from wcwidth import wcswidth
except ImportError:
    def wcswidth(s: str) -> int:
        return len(s)


def largura_visual(texto: str) -> int:
    w = wcswidth(texto)
    return w if w is not None and w >= 0 else len(texto)


def eh_linha_separadora(linha: str) -> bool:
    celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
    if not celulas:
        return False
    return all(re.fullmatch(r":?-{1,}:?", c) for c in celulas)


def alinhamento_da_celula(sep_celula: str) -> str:
    sep_celula = sep_celula.strip()
    esquerda = sep_celula.startswith(":")
    direita = sep_celula.endswith(":")
    if esquerda and direita:
        return "centro"
    if direita:
        return "direita"
    return "esquerda"


def dividir_celulas(linha: str) -> list[str]:
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    # Divide em '|' que não estejam dentro de crase (`código|assim`) — caso raro,
    # mas tratamos separação simples pois não há tabelas com '|' literal aqui.
    return [c.strip() for c in linha.split("|")]


def formatar_bloco_tabela(linhas: list[str]) -> list[str]:
    cabecalho = dividir_celulas(linhas[0])
    separador = dividir_celulas(linhas[1])
    corpo = [dividir_celulas(l) for l in linhas[2:]]

    n_col = len(cabecalho)
    # normaliza número de colunas (por segurança, caso alguma linha tenha menos células)
    for linha_c in corpo:
        while len(linha_c) < n_col:
            linha_c.append("")

    alinhamentos = [alinhamento_da_celula(separador[i]) if i < len(separador) else "esquerda" for i in range(n_col)]

    larguras = []
    for i in range(n_col):
        maior = largura_visual(cabecalho[i])
        for linha_c in corpo:
            maior = max(maior, largura_visual(linha_c[i]))
        larguras.append(max(maior, 3))  # mínimo 3 para caber "---"

    def preencher(texto: str, largura: int, alinhamento: str) -> str:
        falta = largura - largura_visual(texto)
        if falta <= 0:
            return texto
        if alinhamento == "direita":
            return " " * falta + texto
        if alinhamento == "centro":
            esq = falta // 2
            dire = falta - esq
            return " " * esq + texto + " " * dire
        return texto + " " * falta

    def montar_linha(celulas: list[str]) -> str:
        partes = [preencher(celulas[i], larguras[i], alinhamentos[i]) for i in range(n_col)]
        return "| " + " | ".join(partes) + " |"

    def montar_separador() -> str:
        partes = []
        for i in range(n_col):
            largura = larguras[i]
            a = alinhamentos[i]
            if a == "centro":
                partes.append(":" + "-" * (largura - 2) + ":")
            elif a == "direita":
                partes.append("-" * (largura - 1) + ":")
            else:
                partes.append("-" * largura)
        return "| " + " | ".join(partes) + " |"

    resultado = [montar_linha(cabecalho), montar_separador()]
    for linha_c in corpo:
        resultado.append(montar_linha(linha_c))
    return resultado


def processar_arquivo(caminho: Path) -> bool:
    texto = caminho.read_text(encoding="utf-8")
    linhas = texto.split("\n")
    saida = []
    i = 0
    mudou = False
    while i < len(linhas):
        linha = linhas[i]
        if linha.strip().startswith("|") and i + 1 < len(linhas) and eh_linha_separadora(linhas[i + 1]):
            bloco = [linha, linhas[i + 1]]
            j = i + 2
            while j < len(linhas) and linhas[j].strip().startswith("|"):
                bloco.append(linhas[j])
                j += 1
            novo_bloco = formatar_bloco_tabela(bloco)
            if novo_bloco != bloco:
                mudou = True
            saida.extend(novo_bloco)
            i = j
        else:
            saida.append(linha)
            i += 1

    if mudou:
        caminho.write_text("\n".join(saida), encoding="utf-8")
    return mudou


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python formatar_tabelas.py <arquivo.md|pasta>")
        return 1

    alvo = Path(sys.argv[1])
    arquivos = [alvo] if alvo.is_file() else sorted(alvo.rglob("*.md"))

    total_alterados = 0
    for arquivo in arquivos:
        if processar_arquivo(arquivo):
            print(f"  ✅ realinhado: {arquivo}")
            total_alterados += 1
        else:
            print(f"  · sem tabela ou já alinhado: {arquivo}")

    print(f"\n{total_alterados} arquivo(s) alterado(s) de {len(arquivos)} processado(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
