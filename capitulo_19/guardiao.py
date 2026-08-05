"""
Capítulo 19 — O Guardião da Informação
LGPD: anonimização, permissões por função, trilha de auditoria.

PLUS:
  - Middleware de permissão reutilizável
  - Log de tentativas bloqueadas
  - Demo do caso Ricardo Jr.
"""

from pathlib import Path
import hashlib
import logging

PASTA = Path(__file__).parent
LOG = PASTA / "auditoria_seguranca.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    filename=str(LOG),
    filemode="a",
    force=True,
)

PERMISSOES = {
    "rh": ["tabela_funcionarios", "tabela_salarios", "emocionometro"],
    "financeiro": ["tabela_salarios", "notas_fiscais", "contas"],
    "marketing": ["clientes", "campanhas", "produtos"],
    "ti": ["logs", "configs", "monitoring"],
    "medico": ["fichas_medicas"],
}


def anonimizar(dado: str) -> str:
    """Hash irreversível. Mesmo input = mesmo hash. Não revela a identidade."""
    return hashlib.sha256(dado.encode("utf-8")).hexdigest()[:16]


def verificar_permissao(usuario: str, tabela: str) -> bool:
    """Controle de acesso por função (não por departamento genérico)."""
    perfil = usuario.split("_")[0].lower()
    return tabela in PERMISSOES.get(perfil, [])


def registrar_acesso(usuario: str, acao: str, tabela: str, permitido: bool):
    nivel = logging.INFO if permitido else logging.WARNING
    msg = f"USUARIO={usuario} | ACAO={acao} | TABELA={tabela} | PERMITIDO={permitido}"
    logging.log(nivel, msg)
    if permitido:
        print(f"✅ Acesso OK: {msg}")
    else:
        print(f"🚫 ACESSO BLOQUEADO: {msg}")


def acessar(usuario: str, tabela: str, acao: str = "READ") -> bool:
    """Middleware: verifica + registra em uma chamada."""
    ok = verificar_permissao(usuario, tabela)
    registrar_acesso(usuario, acao, tabela, ok)
    return ok


if __name__ == "__main__":
    print("=== Demo Guardião da Informação ===\n")

    # Acesso legítimo
    acessar("rh_luciana", "tabela_funcionarios")

    # Caso do livro: estagiário de marketing olhando salários
    acessar("marketing_ricardojr", "tabela_salarios")

    # Médico do trabalho — só fichas médicas
    acessar("medico_trabalho", "fichas_medicas")
    acessar("medico_trabalho", "tabela_salarios")

    # TI não vê salários
    acessar("ti_ziul", "tabela_salarios")
    acessar("ti_ziul", "logs")

    print(f"\n🔒 ID anônimo de 'Ana Silva': {anonimizar('Ana Silva')}")
    print(f"   (mesmo input → mesmo hash: {anonimizar('Ana Silva')})")
    print(f"\n📝 Log completo em: {LOG}")
