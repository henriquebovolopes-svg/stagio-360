-- STAGIO 360 | Fund. I | M1/2026
-- Execute somente em projeto Supabase privado, no SQL Editor (dono do projeto).
-- Nenhum dado real deve ser gravado antes dos testes de RLS.
create extension if not exists pgcrypto;
create schema if not exists private;

create table if not exists public.stg_members (
  user_id uuid primary key references auth.users(id) on delete cascade,
  display_name text not null,
  role text not null check (role in ('admin','coordenacao')),
  active boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists public.stg_teachers (
  id uuid primary key,
  name text not null,
  classes text[] not null default '{}'::text[],
  scope text not null default 'A confirmar',
  role_label text not null default 'Docente',
  source_module text not null default 'M1',
  unique(name,source_module)
);

create table if not exists public.stg_teacher_scores (
  id uuid primary key,
  teacher_id uuid not null references public.stg_teachers(id) on delete cascade,
  source text not null check (source in ('ERICA','AUTO')),
  axis text not null,
  criterion text not null,
  score numeric(6,2) not null,
  scale_max integer not null check(scale_max in (4,5)),
  module text not null default 'M1',
  source_id text,
  check(score between 1 and scale_max)
);

create table if not exists public.stg_evidence (
  id uuid primary key,
  scope text not null check (scope in ('ERICA','AUTO','ALUNO','FAMILIA')),
  teacher_id uuid references public.stg_teachers(id) on delete set null,
  class_code text,
  respondent_code text,
  axis text,
  question text not null,
  answer text not null,
  origin text,
  module text not null default 'M1'
);

create table if not exists public.stg_students (
  respondent_code text primary key,
  class_code text not null,
  answers jsonb not null default '[]'::jsonb,
  module text not null default 'M1'
);

create table if not exists public.stg_families (
  respondent_code text primary key,
  scope text not null,
  grade_names text,
  answers jsonb not null default '[]'::jsonb,
  module text not null default 'M1'
);

create index if not exists stg_scores_teacher_idx on public.stg_teacher_scores(teacher_id, source);
create index if not exists stg_evidence_teacher_idx on public.stg_evidence(teacher_id, scope);
create index if not exists stg_evidence_scope_idx on public.stg_evidence(scope);
create index if not exists stg_students_class_idx on public.stg_students(class_code);

-- Acesso explicitamente negado para visitantes, e apenas SELECT para usuários autenticados.
alter table public.stg_members enable row level security;
alter table public.stg_teachers enable row level security;
alter table public.stg_teacher_scores enable row level security;
alter table public.stg_evidence enable row level security;
alter table public.stg_students enable row level security;
alter table public.stg_families enable row level security;

revoke all on public.stg_members,public.stg_teachers,public.stg_teacher_scores,public.stg_evidence,public.stg_students,public.stg_families from public,anon,authenticated;
grant select on public.stg_members,public.stg_teachers,public.stg_teacher_scores,public.stg_evidence,public.stg_students,public.stg_families to authenticated;

-- Não usar metadata editável pelo usuário para autorizar acesso.
create or replace function private.stg_authorized()
returns boolean language sql stable security definer set search_path = ''
as $$
  select exists (
    select 1 from public.stg_members m
    where m.user_id = (select auth.uid())
      and m.active = true
      and m.role in ('admin','coordenacao')
  );
$$;
revoke all on function private.stg_authorized() from public,anon;
grant usage on schema private to authenticated;
grant execute on function private.stg_authorized() to authenticated;

drop policy if exists stg_member_self on public.stg_members;
create policy stg_member_self on public.stg_members
for select to authenticated
using (user_id = (select auth.uid()));

drop policy if exists stg_private_read_teachers on public.stg_teachers;
create policy stg_private_read_teachers on public.stg_teachers
for select to authenticated using ((select private.stg_authorized()));

drop policy if exists stg_private_read_scores on public.stg_teacher_scores;
create policy stg_private_read_scores on public.stg_teacher_scores
for select to authenticated using ((select private.stg_authorized()));

drop policy if exists stg_private_read_evidence on public.stg_evidence;
create policy stg_private_read_evidence on public.stg_evidence
for select to authenticated using ((select private.stg_authorized()));

drop policy if exists stg_private_read_students on public.stg_students;
create policy stg_private_read_students on public.stg_students
for select to authenticated using ((select private.stg_authorized()));

drop policy if exists stg_private_read_families on public.stg_families;
create policy stg_private_read_families on public.stg_families
for select to authenticated using ((select private.stg_authorized()));

-- ATENÇÃO: criar usuários manualmente em Authentication > Users, com cadastro público desativado.
-- Em seguida autorizar apenas contas convidadas, por exemplo:
-- insert into public.stg_members (user_id,display_name,role,active)
-- values ('<UUID-DA-CONTA>'::uuid,'Coordenação','coordenacao',true);
-- IMPORTANTE: apenas o administrador SQL/service_role pode alterar stg_members.
