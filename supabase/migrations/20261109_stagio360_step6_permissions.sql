-- STAGIO 360 / PASSO 6 / 2026-11-09
-- Configuracao de perfis: administracao, direcao master e coordenacao por etapa.
-- SQL aplicado no projeto stagio-360 pela migracao
-- stagio360_step6_roles_access_hardening_20261109.
-- Nao contem UUIDs, credenciais ou dados individuais.

-- A autorizacao da Escuta dos Funcionarios exige dois vinculos ATIVOS:
-- cadastro institucional (admin/master) e autorizacao especifica privada.
create or replace function private.stg_staff_allowed()
returns boolean language sql stable security definer set search_path = ''
as $$
  select exists (
    select 1 from private.stg_staff_access a
    join public.stg_members m on m.user_id = a.user_id
    where a.user_id = (select auth.uid())
      and a.active is true
      and m.active is true
      and m.role in ('admin', 'master')
      and a.access_label in ('Henrique', 'Giovanna', 'Márcia')
  );
$$;
revoke all on function private.stg_staff_allowed() from public, anon;
grant execute on function private.stg_staff_allowed() to authenticated;

-- Pareceres institucionais de PDIs FI: master tambem pode elaborar parecer,
-- permanecendo sujeito as politicas RLS e a validade do PDI.
alter table public.stg_pdi_institutional_reviews
drop constraint if exists stg_pdi_institutional_reviews_reviewer_role_check;
alter table public.stg_pdi_institutional_reviews
add constraint stg_pdi_institutional_reviews_reviewer_role_check
check (reviewer_role in ('admin', 'master', 'coordenacao'));

create or replace function private.stg_pdi_institutional_review_guard()
returns trigger language plpgsql security definer set search_path = ''
as $$
declare membership record;
begin
  select m.display_name, m.role into membership
  from public.stg_members m
  where m.user_id = (select auth.uid()) and m.active = true
    and m.role in ('admin','master','coordenacao');
  if not found then
    raise exception 'Somente administracao, direcao e coordenacao podem registrar pareceres.';
  end if;
  if not exists (
    select 1 from public.stg_pdi_plans p
    where p.id = new.plan_id and p.status in ('rascunho','para_revisao')
  ) then
    raise exception 'A pre-revisao exige PDI existente ainda nao pactuado.';
  end if;
  new.reviewer_id = (select auth.uid());
  new.reviewer_display_name = membership.display_name;
  new.reviewer_role = membership.role;
  new.created_at = now();
  return new;
end;
$$;

-- Politicas preexistentes preservadas:
-- private.stg_scope_authorized(stage) exige membership ativo,
-- admin/master podem consultar todas as etapas,
-- coordenacao somente com stg_scope_access na etapa.
-- Nenhuma conta adicional e criada por esta migracao.
