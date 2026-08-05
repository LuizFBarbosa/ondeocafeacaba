"""
Capítulo 4 — O Freio de Mão do Desconto
Circuit breaker + validação de desconto para proteger campanhas.
"""

from typing import Dict, Tuple

# Cada campanha válida entra ANTES de ir ao ar
CAMPANHAS_REGISTRADAS: Dict[Tuple[str, str], dict] = {
    ("linha_giro_lento", "Salvador"): {
        "desconto_min": 0.0,
        "desconto_max": 0.05,
        "pedidos_hora_max": 400,
    },
    ("cerveja", "São Paulo"): {
        "desconto_min": 0.0,
        "desconto_max": 0.20,
        "pedidos_hora_max": 800,
    },
}

# Estado do circuito por (produto, praça)
circuito: Dict[Tuple[str, str], str] = {}


def validar_desconto(desconto_proposto: float, desconto_maximo_usual: float = 0.05) -> float:
    """
    Bloqueia qualquer desconto fora do razoável sem confirmação explícita.
    Em produção, a confirmação viria de uma tela; aqui simulamos.
    """
    if desconto_proposto > desconto_maximo_usual:
        percentual = desconto_proposto * 100
        print(
            f"⚠️  Você está aplicando {percentual:.1f}% de desconto — "
            f"acima do usual de {desconto_maximo_usual*100:.0f}%."
        )
        # Em ambiente interativo: input("digite CONFIRMO: ")
        # Aqui aceitamos para demonstração se <= 0.25
        if desconto_proposto > 0.25:
            raise ValueError("Desconto fora do padrão não confirmado. Operação cancelada.")
        print("   (confirmação simulada: OK)")
    return desconto_proposto


def alertar_time_comercial(chave, desconto, pedidos):
    print(f"🚨 ALERTA COMERCIAL: {chave} | desconto={desconto:.1%} | pedidos/h={pedidos}")


def registrar_pedido(produto: str, praca: str, desconto_aplicado: float, pedidos_na_ultima_hora: int) -> str:
    """
    Protege o que acontece depois, pedido por pedido.
    Nunca cancela o que já foi vendido — só impede o próximo erro.
    """
    chave = (produto, praca)

    if circuito.get(chave) == "aberto":
        return "BLOQUEADO: regra em revisão. Aguarde atualização."

    campanha = CAMPANHAS_REGISTRADAS.get(chave)
    if campanha is None:
        return "LIBERADO: sem campanha registrada (passe livre)."

    dentro_do_desconto = campanha["desconto_min"] <= desconto_aplicado <= campanha["desconto_max"]
    dentro_do_volume = pedidos_na_ultima_hora <= campanha["pedidos_hora_max"]

    if not dentro_do_desconto or not dentro_do_volume:
        circuito[chave] = "aberto"
        alertar_time_comercial(chave, desconto_aplicado, pedidos_na_ultima_hora)
        return "BLOQUEADO: regra pausada automaticamente a partir de agora."

    return "LIBERADO: dentro do esperado para a campanha registrada."


def fechar_circuito(produto: str, praca: str):
    """Reabre a regra após correção manual."""
    chave = (produto, praca)
    circuito.pop(chave, None)
    print(f"✅ Circuito fechado para {chave}")


if __name__ == "__main__":
    print("=== Demo Circuit Breaker ===\n")

    # 1. Desconto normal
    print(registrar_pedido("linha_giro_lento", "Salvador", 0.02, 50))

    # 2. Desconto 20% (erro clássico do 0,2 em vez de 0,02) + volume alto
    print(registrar_pedido("linha_giro_lento", "Salvador", 0.20, 500))

    # 3. Tentativa após abertura do circuito
    print(registrar_pedido("linha_giro_lento", "Salvador", 0.02, 10))

    # 4. Correção e reabertura
    fechar_circuito("linha_giro_lento", "Salvador")
    print(registrar_pedido("linha_giro_lento", "Salvador", 0.02, 10))
