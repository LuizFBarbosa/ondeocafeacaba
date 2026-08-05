"""
Capítulo 17 — O Condutor Invisível
Orquestração de rotinas (esqueleto Celery-compatible).

PLUS:
  - Schedule legível em Python puro (roda sem Redis)
  - Log de execução com timestamp
  - Demonstração de "maestro" coordenando várias tarefas
"""

from datetime import datetime
from typing import Callable

# ── Tarefas (as "partituras") ──

def gerar_relatorio_diario():
    """Toda manhã às 7h30 — o relatório chega antes do café. (Cap. 1)"""
    print("  📊 Gerando relatório de vendas...")
    print("  ✅ Relatório enviado!")


def verificar_estoque_e_sugerir_compras():
    """Toda segunda às 8h — estoque + previsão de demanda. (Cap. 10)"""
    print("  📦 Verificando estoque crítico...")
    print("  ✅ Sugestões de compra geradas e enviadas para aprovação!")


def rodar_auditoria_dados():
    """Toda madrugada às 2h — o guardião que ninguém vê. (Cap. 6)"""
    print("  🔍 Auditoria noturna iniciada...")
    print("  ✅ Auditoria concluída. Log salvo.")


def rodar_emocionometro():
    """Sexta 16h — clima da equipe. (Cap. 13)"""
    print("  💚 Emocionômetro: coletando feedbacks da semana...")
    print("  ✅ Painel de humor atualizado.")


# ── Agendamento (o "maestro") ──

SCHEDULE = [
    {"nome": "relatorio-diario", "hora": "07:30", "dias": "seg-sex", "task": gerar_relatorio_diario},
    {"nome": "verificar-compras", "hora": "08:00", "dias": "segunda", "task": verificar_estoque_e_sugerir_compras},
    {"nome": "auditoria-noturna", "hora": "02:00", "dias": "todos", "task": rodar_auditoria_dados},
    {"nome": "emocionometro", "hora": "16:00", "dias": "sexta", "task": rodar_emocionometro},
]


def executar_tudo():
    """Simula o Beat disparando todas as tarefas (demo)."""
    print("=" * 55)
    print("  CONDUTOR INVISÍVEL — simulação de orquestra")
    print(f"  Agora: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 55)
    for item in SCHEDULE:
        print(f"\n[{item['hora']}] {item['nome']} ({item['dias']})")
        item["task"]()
    print("\n" + "=" * 55)
    print("  Sinfonia concluída. Nenhum humano precisou lembrar.")
    print("=" * 55)


# Em produção real com Celery:
#   from celery import Celery
#   from celery.schedules import crontab
#   app = Celery("atacado", broker="redis://localhost:6379/0")
#   app.conf.beat_schedule = { ... crontab(hour=7, minute=30) ... }

if __name__ == "__main__":
    executar_tudo()
