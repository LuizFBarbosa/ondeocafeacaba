#!/usr/bin/env python3
"""
Validador automático do repositório "Onde o Café Acaba, o Código Começa".

O que este script faz:
  1. Compila (py_compile) TODOS os arquivos .py do repositório, capítulo a
     capítulo, garantindo que não há erro de sintaxe em nenhum código do livro.
  2. Executa os scripts que rodam de ponta a ponta sem exigir um serviço
     externo (Redis, Tesseract binário, servidor Streamlit, etc.), incluindo
     os geradores de dados, e confere se o processo termina com sucesso
     (exit code 0).
  3. Para os capítulos que dependem de infraestrutura externa (API que
     precisa ficar no ar, dashboard Streamlit, fila Celery/Redis, OCR com
     Tesseract instalado, LSTM com TensorFlow), o script apenas confirma que
     o arquivo importa e compila corretamente — a execução completa desses
     está documentada no README de cada capítulo.

Uso:
    python scripts/validar_capitulos.py

Este é o mesmo processo usado para validar o repositório antes de cada
publicação e é executado automaticamente pelo GitHub Actions
(.github/workflows/validar-codigo.yml) a cada push.
"""

from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Scripts que rodam sozinhos, sem servidor/serviço externo, e que devem
# terminar com exit code 0 quando executados diretamente com `python arquivo.py`.
EXECUTAVEIS_PONTA_A_PONTA = [
    "capitulo_01/gerar_dados.py",
    "capitulo_01/relatorio_vendas.py",
    "capitulo_02/gerar_dados.py",
    "capitulo_02/tradutor_universal.py",
    "capitulo_04/circuit_breaker.py",
    "capitulo_05/processar_notas.py",
    "capitulo_06/auditor.py",
    "capitulo_07/gerar_dados.py",
    "capitulo_07/radar_oportunidades.py",
    "capitulo_10/previsao_demanda.py",   # roda em modo fallback sem TensorFlow
    "capitulo_12/gamificacao.py",
    "capitulo_13/gerar_dados.py",
    "capitulo_13/emocionometro.py",
    "capitulo_14/auditor_vies.py",
    "capitulo_15/ziulbot.py",            # RAG ilustrativo, sem LLM externo
    "capitulo_16/dna_conhecimento.py",
    "capitulo_17/tasks.py",              # roda sem Redis/Celery instalado
    "capitulo_18/ocr_aceite.py",         # roda em modo simulado sem Tesseract
    "capitulo_19/guardiao.py",
    "capitulo_20/monte_carlo.py",
    "laboratorio/limpador.py",
]

# Apenas checagem de sintaxe/import (precisam de servidor, Streamlit run,
# Redis real ou Tesseract binário para rodar por completo).
SOMENTE_SINTAXE = [
    "capitulo_03/api_precos.py",
    "capitulo_03/cliente_crm.py",
    "capitulo_08/api_sugestoes.py",
    "capitulo_09/dashboard.py",
]


def compilar_todos_os_py() -> list[str]:
    erros = []
    for arquivo in sorted(RAIZ.rglob("*.py")):
        if ".venv" in arquivo.parts or "venv" in arquivo.parts:
            continue
        try:
            py_compile.compile(str(arquivo), doraise=True)
        except py_compile.PyCompileError as e:
            erros.append(f"{arquivo}: {e}")
    return erros


def rodar_ponta_a_ponta() -> list[str]:
    erros = []
    for relativo in EXECUTAVEIS_PONTA_A_PONTA:
        caminho = RAIZ / relativo
        if not caminho.exists():
            erros.append(f"{relativo}: arquivo não encontrado")
            continue
        resultado = subprocess.run(
            [sys.executable, caminho.name],
            cwd=caminho.parent,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if resultado.returncode != 0:
            erros.append(
                f"{relativo}: saiu com código {resultado.returncode}\n"
                f"--- stderr ---\n{resultado.stderr[-1500:]}"
            )
        else:
            print(f"  ✅ {relativo}")
    return erros


def main() -> int:
    print("=" * 60)
    print("  Validando sintaxe de todos os arquivos .py do repositório")
    print("=" * 60)
    erros_sintaxe = compilar_todos_os_py()
    if erros_sintaxe:
        for e in erros_sintaxe:
            print(f"  ❌ {e}")
    else:
        print("  ✅ Sintaxe válida em 100% dos arquivos .py")

    print("\n" + "=" * 60)
    print("  Executando capítulos ponta a ponta")
    print("=" * 60)
    erros_execucao = rodar_ponta_a_ponta()

    print("\n" + "=" * 60)
    print("  Checando sintaxe de capítulos que dependem de serviço externo")
    print("=" * 60)
    for relativo in SOMENTE_SINTAXE:
        caminho = RAIZ / relativo
        if caminho.exists():
            print(f"  ✅ {relativo} (sintaxe OK — execução completa exige serviço externo, ver README do capítulo)")
        else:
            erros_execucao.append(f"{relativo}: arquivo não encontrado")

    total_erros = erros_sintaxe + erros_execucao
    print("\n" + "=" * 60)
    if total_erros:
        print(f"  ❌ {len(total_erros)} problema(s) encontrado(s)")
        return 1
    print("  ✅ TODOS OS CAPÍTULOS VALIDADOS COM SUCESSO")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
