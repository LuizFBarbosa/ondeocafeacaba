# Capítulo 11 — A Tabela que Não Tinha Trinta Linhas

**Governança • menor privilégio • peer review • teste de backup**

---

## O incidente

Júnior testou o `DELETE` com filtro (30 linhas).  
Na produção, rodou a versão **sem WHERE** → quase 4 milhões de linhas apagadas.  
3 dias de restauração.

---

## Lições permanentes

1. **Princípio do menor privilégio** — ninguém com SA em produção no dia a dia  
2. **Réplica de leitura** — consultas não tocam a base real  
3. **Peer review** — nenhum comando destrutivo sem segunda pessoa  
4. **Teste de restauração** — backup que nunca foi restaurado é só uma promessa  

> “A diferença entre você continuar aqui e ele continuar aqui não pode depender de sorte. Tem que depender de processo.”  
> — Sr. Ricardo

---

## Arquivos desta pasta

| Arquivo             | Descrição                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| `padrao_seguro.sql` | O padrão que Júnior devia ter seguido: confere antes, apaga, confere depois, só então confirma |
| `README.md`         | Este arquivo                                                                                   |

Este capítulo não tem um `.py` porque a lição é sobre **disciplina de operação em banco de dados**, não sobre uma biblioteca — o "código" da lição é o próprio SQL.

---

## O padrão seguro, passo a passo

```sql
BEGIN;

-- 1. Confere o tamanho do impacto ANTES de apagar
SELECT count(*) FROM debitos
WHERE id_debito IN (2201, 2202, 2203);  -- deveria retornar 30

-- 2. Só executa o DELETE depois de validar o número acima
DELETE FROM debitos
WHERE id_debito IN (2201, 2202, 2203);

-- 3. Confere de novo, depois do DELETE
SELECT count(*) FROM debitos;  -- confirma que a queda bate com o esperado

-- 4. Só agora decide:
COMMIT;    -- se o número bateu
-- ROLLBACK;  -- se algo saiu diferente do esperado, desfaz tudo
```

**Por que funciona:**

1. **`BEGIN` abre uma transação** — nada é gravado de verdade até o `COMMIT`. Isso é a rede de segurança inteira do padrão.
2. **O `SELECT count(*)` antes do `DELETE`** transforma "eu acho que são 30 linhas" em um número que você viu na tela. Se aparecer 4 milhões em vez de 30, você já sabe que o filtro está errado — e ainda não apagou nada.
3. **O `DELETE` só roda depois da conferência humana** olhar o número do passo 1.
4. **O `SELECT count(*)` depois do `DELETE`** confirma que a queda no total bate com o esperado (se antes tinha 500.030 linhas e devia sobrar 500.000, o número tem que fechar).
5. **`COMMIT` ou `ROLLBACK` é a última decisão, não a primeira.** Se algo no passo 3 não bateu, um `ROLLBACK` desfaz tudo como se nada tivesse acontecido — é exatamente o passo que faltou no incidente do Júnior.

---

## Como testar o padrão (sem precisar de um banco de produção)

Você pode ver esse padrão funcionando com SQLite puro, sem instalar nada além do Python:

```bash
python3 - <<'EOF'
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE debitos (id_debito INTEGER, valor REAL)")

# Simula 30 linhas de teste esquecidas na tabela (o cenário do livro)
for i in list(range(2201, 2204)) * 10:
    cur.execute("INSERT INTO debitos (id_debito, valor) VALUES (?, ?)", (i, 10.0))
conn.commit()

# Passo 1: conferir ANTES de apagar
cur.execute("SELECT count(*) FROM debitos WHERE id_debito IN (2201,2202,2203)")
print("Linhas que seriam apagadas:", cur.fetchone()[0])  # deve imprimir 30
EOF
```

Saída esperada:

```
Linhas que seriam apagadas: 30
```

Se o número bater com o que você esperava, seguir para o `DELETE` é seguro. Se não bater, é hora de revisar o `WHERE` — **antes** de qualquer coisa ser apagada de verdade.

---

## Conceitos-chave (linguagem de atacado)

| Conceito                         | Tradução sem tecniquês                                                     | Por que importa                                                       |
| -------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Transação (`BEGIN`/`COMMIT`)** | Um "rascunho" que só vira definitivo quando você confirma                  | Permite desfazer (`ROLLBACK`) se algo sair errado                     |
| **Menor privilégio**             | Cada pessoa só tem acesso ao que precisa para o trabalho dela              | Reduz o estrago possível de um erro de digitação                      |
| **Peer review**                  | Uma segunda pessoa olha antes de um comando destrutivo rodar               | Duas pessoas erram o mesmo `WHERE` com muito menos frequência que uma |
| **Teste de restauração**         | Restaurar o backup de verdade, periodicamente, para confirmar que funciona | Backup nunca testado é uma suposição, não uma garantia                |

---

## Link no GitHub

https://github.com/LuizFBarbosa/ondeocafeacaba/blob/main/capitulo_11/README.md
