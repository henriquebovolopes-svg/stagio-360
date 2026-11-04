-- STAGIO 360 — teste de permissões (somente leitura)
-- Executar no SQL Editor após migração, ou via Supabase.execute_sql.
-- Não usa dados pessoais e não altera registros.
select
 c.relname as tabela,
 c.relrowsecurity as rls_ativo,
 has_table_privilege('anon', c.oid, 'select') as anon_pode_ler,
 has_table_privilege('authenticated', c.oid, 'select') as autenticado_pode_ler,
 has_table_privilege('authenticated', c.oid, 'insert') as autenticado_pode_inserir,
 has_table_privilege('authenticated', c.oid, 'update') as autenticado_pode_editar,
 has_table_privilege('authenticated', c.oid, 'delete') as autenticado_pode_excluir,
 (select count(*) from pg_policies p where p.schemaname='public' and p.tablename=c.relname) as politicas
from pg_class c
join pg_namespace n on n.oid=c.relnamespace
where n.nspname='public' and c.relkind='r' and c.relname like 'stg_%'
order by c.relname;
-- Resultado esperado para seis tabelas:
-- rls_ativo=true, anon_pode_ler=false, autenticado_pode_ler=true,
-- autenticado_pode_inserir=false, autenticado_pode_editar=false,
-- autenticado_pode_excluir=false, politicas>=1.
-- Autorização RLS NÃO deve ser inferida de 'autenticado_pode_ler=true':
-- apenas membros ativos autorizados passam pelas políticas.
