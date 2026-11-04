-- STAGIO 360 | PDI Piloto M1 — migration applied to Supabase 2026-11-04
-- No individual evidence or teacher's personal data is embedded here.
create table if not exists public.stg_pdi_plans (
  id uuid primary key default gen_random_uuid(),
  teacher_id uuid not null references public.stg_teachers(id) on delete restrict,
  module text not null default 'M1' check (module='M1'),
  focus_source text not null default 'ERICA' check (focus_source in ('ERICA','AUTO')),
  focus_axis text not null default '' check (char_length(focus_axis)<=180),
  context_notes text not null default '' check (char_length(context_notes)<=4000),
  objective text not null default '' check (char_length(objective)<=2000),
  actions text not null default '' check (char_length(actions)<=4000),
  support_needed text not null default '' check (char_length(support_needed)<=2500),
  evidence_indicator text not null default '' check (char_length(evidence_indicator)<=2500),
  responsible text not null default '' check (char_length(responsible)<=300),
  next_review date,
  evidence_ids uuid[] not null default '{}'::uuid[] check (cardinality(evidence_ids)<=5),
  status text not null default 'rascunho' check (status in ('rascunho','para_revisao')),
  created_by uuid not null default auth.uid(),
  updated_by uuid not null default auth.uid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint stg_pdi_unique_teacher_module unique (teacher_id,module)
);
alter table public.stg_pdi_plans enable row level security;
revoke all on public.stg_pdi_plans from public, anon;
grant select,insert,update on public.stg_pdi_plans to authenticated;

create or replace function private.stg_pdi_guard()
returns trigger language plpgsql security invoker set search_path=''
as $$
begin
  if not exists(
    select 1 from public.stg_teachers t
    where t.id=new.teacher_id and t.scope='REGENTE CONFIRMADA'
  ) then
    raise exception 'PDI piloto permitido apenas para regentes homologadas.';
  end if;
  if tg_op='UPDATE' and (new.teacher_id<>old.teacher_id or new.module<>old.module or new.created_by<>old.created_by or new.created_at<>old.created_at) then
    raise exception 'Não é permitido transferir o PDI de profissional ou alterar sua autoria.';
  end if;
  if exists(
    select 1 from unnest(new.evidence_ids) as ref(evidence_id)
    left join public.stg_evidence e on e.id=ref.evidence_id
    where e.id is null or e.teacher_id is distinct from new.teacher_id
      or e.scope not in ('ERICA','AUTO') or e.module<>'M1'
  ) then
    raise exception 'Evidência inexistente ou não pertencente à fonte/profissional.';
  end if;
  if new.status='para_revisao' and (
    nullif(btrim(new.focus_axis),'') is null or
    nullif(btrim(new.objective),'') is null or
    nullif(btrim(new.actions),'') is null or
    nullif(btrim(new.evidence_indicator),'') is null or
    new.next_review is null
  ) then
    raise exception 'Para encaminhar à revisão, preencha eixo, objetivo, ação, indicador e data de acompanhamento.';
  end if;
  new.updated_at=now();
  new.updated_by=auth.uid();
  return new;
end;
$$;

drop trigger if exists stg_pdi_guard_trg on public.stg_pdi_plans;
create trigger stg_pdi_guard_trg before insert or update on public.stg_pdi_plans
for each row execute function private.stg_pdi_guard();

drop policy if exists stg_pdi_read_authorized on public.stg_pdi_plans;
create policy stg_pdi_read_authorized on public.stg_pdi_plans
for select to authenticated using ((select private.stg_authorized()));
drop policy if exists stg_pdi_insert_admin on public.stg_pdi_plans;
create policy stg_pdi_insert_admin on public.stg_pdi_plans
for insert to authenticated
with check ((select private.stg_admin_can_import()) and created_by=(select auth.uid()));
drop policy if exists stg_pdi_update_admin on public.stg_pdi_plans;
create policy stg_pdi_update_admin on public.stg_pdi_plans
for update to authenticated
using ((select private.stg_admin_can_import()))
with check ((select private.stg_admin_can_import()) and created_by is not null);
