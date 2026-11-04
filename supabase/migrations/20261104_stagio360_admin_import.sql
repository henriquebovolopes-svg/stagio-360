-- STAGIO 360 · Importação administrada com RLS
-- Requer que a migração inicial e as contas em stg_members já existam.
-- Mantém permissão de leitura para admin/coordenacao, mas escrita apenas para admin.
create or replace function private.stg_admin_can_import()
returns boolean language sql stable security definer set search_path=''
as $$
select exists(select 1 from public.stg_members m where m.user_id=(select auth.uid()) and m.active=true and m.role='admin');
$$;
revoke all on function private.stg_admin_can_import() from public,anon;
grant execute on function private.stg_admin_can_import() to authenticated;
grant insert,update on public.stg_teachers,public.stg_teacher_scores,public.stg_evidence,public.stg_students,public.stg_families to authenticated;

drop policy if exists stg_admin_import_teachers on public.stg_teachers;
create policy stg_admin_import_teachers on public.stg_teachers for insert to authenticated with check ((select private.stg_admin_can_import()));
drop policy if exists stg_admin_update_teachers on public.stg_teachers;
create policy stg_admin_update_teachers on public.stg_teachers for update to authenticated using ((select private.stg_admin_can_import())) with check ((select private.stg_admin_can_import()));

drop policy if exists stg_admin_import_scores on public.stg_teacher_scores;
create policy stg_admin_import_scores on public.stg_teacher_scores for insert to authenticated with check ((select private.stg_admin_can_import()));
drop policy if exists stg_admin_update_scores on public.stg_teacher_scores;
create policy stg_admin_update_scores on public.stg_teacher_scores for update to authenticated using ((select private.stg_admin_can_import())) with check ((select private.stg_admin_can_import()));

drop policy if exists stg_admin_import_evidence on public.stg_evidence;
create policy stg_admin_import_evidence on public.stg_evidence for insert to authenticated with check ((select private.stg_admin_can_import()));
drop policy if exists stg_admin_update_evidence on public.stg_evidence;
create policy stg_admin_update_evidence on public.stg_evidence for update to authenticated using ((select private.stg_admin_can_import())) with check ((select private.stg_admin_can_import()));

drop policy if exists stg_admin_import_students on public.stg_students;
create policy stg_admin_import_students on public.stg_students for insert to authenticated with check ((select private.stg_admin_can_import()));
drop policy if exists stg_admin_update_students on public.stg_students;
create policy stg_admin_update_students on public.stg_students for update to authenticated using ((select private.stg_admin_can_import())) with check ((select private.stg_admin_can_import()));

drop policy if exists stg_admin_import_families on public.stg_families;
create policy stg_admin_import_families on public.stg_families for insert to authenticated with check ((select private.stg_admin_can_import()));
drop policy if exists stg_admin_update_families on public.stg_families;
create policy stg_admin_update_families on public.stg_families for update to authenticated using ((select private.stg_admin_can_import())) with check ((select private.stg_admin_can_import()));
