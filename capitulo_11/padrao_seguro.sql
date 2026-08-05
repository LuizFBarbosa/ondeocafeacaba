-- Capítulo 11 — A Régua que Protege Contra Pressa
-- Padrão seguro para qualquer DELETE ou UPDATE em produção

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
