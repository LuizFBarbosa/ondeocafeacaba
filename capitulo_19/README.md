# Capítulo 19 — O Guardião da Informação

**LGPD • segurança de dados • anonimização • criptografia • auditoria**

---

## O incidente do livro

Às 2h da manhã, o log mostrou: acesso à tabela de salários.  
Usuário: `Ricardo Jr` — estagiário de marketing, filho do diretor.  
Não alterou nada. Só leu. E exportou CSV.

Ziul ligou para Sr. Ricardo às 00h40 sem saber ainda se tinha vazado.  
Quarenta minutos depois: o arquivo nunca saiu da máquina. Susto sem vítima.

Mas a incerteza sozinha já era inaceitável.

> “Construí um edifício magnífico e esqueci do sistema de incêndio.”

---

## Dois pilares da solução

1. **Anonimização real** — sistemas analíticos não recebem nome/CPF  
2. **Permissão por função + trilha de auditoria** — cada acesso registrado  

---

## Como executar

```bash
python guardiao.py
```

O log é gravado em `auditoria_seguranca.log`.

---

## Explicação passo a passo

### 1. Hash para anonimizar

```python
def anonimizar(dado: str) -> str:
    return hashlib.sha256(dado.encode()).hexdigest()[:16]
```

Emocionômetro e DNA do Conhecimento trabalham só com IDs anônimos.

### 2. Menor privilégio por função

```python
PERMISSOES = {
    "rh": ["tabela_funcionarios", "tabela_salarios", ...],
    "marketing": ["clientes", "campanhas", "produtos"],  # sem salários
}
```

Marketing não entra em RH. RH não vê prontuário médico. Cada um no seu quadrado.

### 3. Tudo é logado — permitido ou não

Tentativas bloqueadas geram `WARNING` e podem disparar alerta em produção.

---

## Conceitos-chave

| Conceito             | Tradução                         | Por que importa                        |
| -------------------- | -------------------------------- | -------------------------------------- |
| **LGPD**             | Lei Geral de Proteção de Dados   | Contrato de confiança empresa ↔ pessoa |
| **Anonimização**     | Dado que não identifica a pessoa | Reduz risco jurídico e técnico         |
| **Menor privilégio** | Só o acesso mínimo necessário    | Reduz superfície de ataque             |
| **Auditoria**        | Quem acessou o quê, quando       | Detecta abuso e dá rastreabilidade     |

---

## PLUS deste capítulo

- Middleware `acessar()` (verifica + registra)
- Perfil `medico` isolado
- Demo completa do caso Ricardo Jr.

---

## Frase de ouro

> “Um dado pessoal não é informação — é confiança.  
> E confiança, uma vez quebrada, não se recupera com código.”

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_19/README.md
