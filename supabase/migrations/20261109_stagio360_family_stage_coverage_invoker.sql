-- Conciliacao das familias multietapa 2026
-- A ordem de atribuicao exclusiva foi reconstruida de forma exata a partir
-- dos NPS homologados de 2026, NAO a partir de hipotese de prioridade pedagogica.
-- FII > Medio > Infantil > FI. A leitura inclusiva nao pode ser somada.
CREATE OR REPLACE VIEW public.stg_360_family_stage_membership
 WITH (security_invoker=true) AS
WITH normalized AS(
 SELECT
  source_key,
  nps_value,
  declared_segments,
  (coalesce(declared_segments,'') LIKE '%Infantil%') AS has_infantil,
  (coalesce(declared_segments,'') LIKE '%Iniciais%') AS has_fi,
  (coalesce(declared_segments,'') LIKE '%Finais%') AS has_fii,
  (coalesce(declared_segments,'') LIKE '%Médio%') AS has_medio
 FROM public.stg_360_survey_forms
 WHERE cohort='families' AND school_year=2026
), mapped AS(
 SELECT *, CASE
  WHEN has_fii THEN 'fundamental2'
  WHEN has_medio THEN 'medio'
  WHEN has_infantil THEN 'infantil'
  WHEN has_fi THEN 'fundamental1'
  ELSE NULL
 END AS exclusive_stage
 FROM normalized
)
SELECT m.source_key,m.nps_value,x.stage,m.exclusive_stage,
 (m.exclusive_stage=x.stage) AS exclusive_attribution,
 (m.nps_value IS NOT NULL) AS has_valid_nps
FROM mapped m
CROSS JOIN LATERAL (VALUES
 ('infantil',m.has_infantil),
 ('fundamental1',m.has_fi),
 ('fundamental2',m.has_fii),
 ('medio',m.has_medio)
) AS x(stage,is_mentioned)
WHERE x.is_mentioned;
REVOKE ALL ON public.stg_360_family_stage_membership FROM PUBLIC,anon,authenticated;
GRANT SELECT ON public.stg_360_family_stage_membership TO authenticated;

CREATE OR REPLACE VIEW public.stg_360_family_stage_coverage
 WITH (security_invoker=true) AS
SELECT stage,
 COUNT(*)::integer AS mentions_inclusive,
 COUNT(*) FILTER (WHERE has_valid_nps)::integer AS nps_inclusive,
 COUNT(*) FILTER (WHERE exclusive_attribution)::integer AS assigned_exclusively,
 COUNT(*) FILTER (WHERE exclusive_attribution AND has_valid_nps)::integer AS nps_exclusive,
 COUNT(*) FILTER (WHERE exclusive_attribution AND nps_value>=9)::integer AS promoters_exclusive,
 COUNT(*) FILTER (WHERE exclusive_attribution AND nps_value BETWEEN 7 AND 8)::integer AS passives_exclusive,
 COUNT(*) FILTER (WHERE exclusive_attribution AND nps_value<=6)::integer AS detractors_exclusive,
 ROUND(100.0 * (
 COUNT(*) FILTER (WHERE exclusive_attribution AND nps_value>=9)
 - COUNT(*) FILTER (WHERE exclusive_attribution AND nps_value<=6)
 )/NULLIF(COUNT(*) FILTER (WHERE exclusive_attribution AND has_valid_nps),0),2) AS nps_exclusive_value,
 COUNT(*) FILTER (WHERE has_valid_nps AND nps_value>=9)::integer AS promoters_inclusive,
 COUNT(*) FILTER (WHERE has_valid_nps AND nps_value BETWEEN 7 AND 8)::integer AS passives_inclusive,
 COUNT(*) FILTER (WHERE has_valid_nps AND nps_value<=6)::integer AS detractors_inclusive,
 ROUND(100.0 * (
 COUNT(*) FILTER (WHERE has_valid_nps AND nps_value>=9)
 - COUNT(*) FILTER (WHERE has_valid_nps AND nps_value<=6)
 )/NULLIF(COUNT(*) FILTER (WHERE has_valid_nps),0),2) AS nps_inclusive_value
FROM public.stg_360_family_stage_membership
GROUP BY stage;
REVOKE ALL ON public.stg_360_family_stage_coverage FROM PUBLIC,anon,authenticated;
GRANT SELECT ON public.stg_360_family_stage_coverage TO authenticated;
COMMENT ON VIEW public.stg_360_family_stage_coverage IS
'2026: exclusiva reproduz os quatro NPS por etapa publicados com prioridade FII, EM, EI, FI. Inclusiva conta vinculos e nao e somavel entre etapas. As duas visoes invoker estao sob RLS da fonte.';
