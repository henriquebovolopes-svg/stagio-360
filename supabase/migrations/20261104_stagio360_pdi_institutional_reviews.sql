-- STAGIO 360 | Pareceres restritos de viabilidade institucional (M1)
-- Aplicado ao projeto Supabase em 2026-11-04.
-- Pareceres são eventos imutáveis; não equivalem a decisão nem pactuação.
create table if not exists public.stg_pdi_institutional_reviews (
  id uuid primary key default gen_random_uuid(),
  plan_id uuid not null references public.stg_pdi_plans(id) on delete restrict,
  area text not null check (area in (
    'recursos_materiais','processos_solicitacoes','tempo_planejamento',
    'apoio_equipe','acompanhamento'
  )),
  feasibility text not null check (feasibility in (
    'a_verificar','viavel_com_condicoes','precisa_reformulacao','nao_viavel'
  )),
  observations text not null check (char_length(btrim(observations)) between 12 and 4000),
  proposed_adjustment text not null default '' check (char_length(proposed_adjustment)<=2500),
  potential_owner text not null default '' check (char_length(potential_owner)<=300),
  reviewer_id uuid references auth.users(id) on delete set null default auth.uid(),
  reviewer_display_name text not null default '',
  reviewer_role text not null check (reviewer_role in ('admin','coordenacao')),
  created_at timestamptz not null default now()
);
create index if not exists stg_pdi_inst_review_plan_created_idx
  on public.stg_pdi_institutional_reviews(plan_id,created_at desc);
alter table public.stg_pdi_institutional_reviews enable row level security;
revoke all on public.stg_pdi_institutional_reviews from public,anon,authenticated;
grant select,insert on public.stg_pdi_institutional_reviews to authenticated;
create or replace function private.stg_pdi_institutional_review_guard()
returns trigger language plpgsql security invoker set search_path=''
as $$
declare membership record;
begin
  select m.display_name, m.role into membership from public.stg_members m
  where m.user_id=auth.uid() and m.active=true and m.role in ('admin','coordenacao');
  if not found then
    raise exception 'Somente administração e coordenação podem registrar pareceres.';
  end if;
  if not exists(
    select 1 from public.stg_pdi_plans p
    where p.id=new.plan_id and p.status in ('rascunho','para_revisao')
  ) then
    raise exception 'A pré-revisão exige PDI existente ainda não pactuado.';
  end if;
  new.reviewer_id=auth.uid();
  new.reviewer_display_name=membership.display_name;
  new.reviewer_role=membership.role;
  new.created_at=now();
  return new;
end;
$$;
drop trigger if exists stg_pdi_institutional_review_guard_trg
  on public.stg_pdi_institutional_reviews;
create trigger stg_pdi_institutional_review_guard_trg
  before insert on public.stg_pdi_institutional_reviews
  for each row execute function private.stg_pdi_institutional_review_guard();
drop policy if exists stg_pdi_inst_review_select on public.stg_pdi_institutional_reviews;
create policy stg_pdi_inst_review_select on public.stg_pdi_institutional_reviews
  for select to authenticated using ((select private.stg_authorized()));
drop policy if exists stg_pdi_inst_review_insert on public.stg_pdi_institutional_reviews;
create policy stg_pdi_inst_review_insert on public.stg_pdi_institutional_reviews
  for insert to authenticated
  with check ((select private.stg_authorized()) and reviewer_id=(select auth.uid()));
-- Sem privilégios de UPDATE/DELETE para authenticated ou anon.
