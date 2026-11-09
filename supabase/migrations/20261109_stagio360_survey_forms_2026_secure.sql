-- STAGIO 360 — Questionários 2026, fonte bruta sanitizada, sem PII de identificação
-- Importação por formulário, respostas em JSONB; leitura do detalhamento só a admin/master.
-- Respostas ausentes (especialmente NPS) permanecem NULL; nunca imputar zero.
CREATE TABLE IF NOT EXISTS public.stg_360_survey_forms (
  source_key text PRIMARY KEY,
  source_file_id text NOT NULL,
  source_name text NOT NULL,
  source_row integer NOT NULL CHECK(source_row>=2),
  school_year integer NOT NULL DEFAULT 2026,
  module text NOT NULL DEFAULT 'M1',
  audience text NOT NULL CHECK(audience IN ('students','families')),
  stage text NOT NULL CHECK(stage IN ('fundamental2','medio','institutional')),
  cohort text NOT NULL CHECK(cohort IN ('fii_6a8','fii_9ano','em','families')),
  class_or_series text,
  declared_segments text,
  source_submitted_at text,
  nps_value integer CHECK(nps_value IS NULL OR nps_value BETWEEN 0 AND 10),
  answers jsonb NOT NULL DEFAULT '[]'::jsonb CHECK(jsonb_typeof(answers)='array'),
  answers_count integer NOT NULL DEFAULT 0 CHECK(answers_count >= 0),
  import_snapshot date NOT NULL DEFAULT CURRENT_DATE,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(source_file_id,source_row),
  CONSTRAINT stg_360_answers_len CHECK(answers_count=jsonb_array_length(answers))
);
ALTER TABLE public.stg_360_survey_forms ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.stg_360_survey_forms FROM anon,authenticated;
GRANT SELECT ON public.stg_360_survey_forms TO authenticated;
DROP POLICY IF EXISTS stg_360_survey_forms_read_management ON public.stg_360_survey_forms;
CREATE POLICY stg_360_survey_forms_read_management
ON public.stg_360_survey_forms FOR SELECT TO authenticated
USING(EXISTS(SELECT 1 FROM public.stg_members m WHERE m.user_id=(SELECT auth.uid()) AND m.active AND m.role IN ('admin','master')));
CREATE INDEX IF NOT EXISTS idx_stg_360_survey_forms_stage ON public.stg_360_survey_forms(school_year,stage,cohort);
CREATE INDEX IF NOT EXISTS idx_stg_360_survey_forms_nps ON public.stg_360_survey_forms(school_year,cohort,nps_value);

CREATE OR REPLACE VIEW public.stg_360_survey_items WITH(security_invoker=true) AS
SELECT f.source_key,f.source_file_id,f.source_row,f.school_year,f.module,
       f.audience,f.stage,f.cohort,f.class_or_series,f.declared_segments,
       f.nps_value,
       (a.x->>'column')::integer AS source_column,
       a.x->>'question' AS question,
       a.x->>'kind' AS response_kind,
       a.x->>'value' AS response_text,
       CASE WHEN a.x->>'kind' IN ('rating_1to5','nps') THEN (a.x->>'value')::numeric ELSE NULL END AS score
FROM public.stg_360_survey_forms f
CROSS JOIN LATERAL jsonb_array_elements(f.answers) a(x);
REVOKE ALL ON public.stg_360_survey_items FROM anon,authenticated;
GRANT SELECT ON public.stg_360_survey_items TO authenticated;

CREATE OR REPLACE VIEW public.stg_360_survey_coverage WITH(security_invoker=true) AS
SELECT school_year,audience,stage,cohort,
 COUNT(*)::integer AS raw_forms,
 COUNT(*) FILTER(WHERE nps_value IS NOT NULL)::integer AS valid_nps,
 COUNT(*) FILTER(WHERE nps_value IS NULL)::integer AS no_nps,
 SUM(answers_count)::integer AS items_captured,
 COUNT(*) FILTER(WHERE nps_value BETWEEN 9 AND 10)::integer AS promoters,
 COUNT(*) FILTER(WHERE nps_value BETWEEN 7 AND 8)::integer AS passives,
 COUNT(*) FILTER(WHERE nps_value BETWEEN 0 AND 6)::integer AS detractors,
 ROUND(100.0*(COUNT(*) FILTER(WHERE nps_value BETWEEN 9 AND 10)-COUNT(*) FILTER(WHERE nps_value BETWEEN 0 AND 6))/NULLIF(COUNT(nps_value),0),2) AS nps_valid_only
FROM public.stg_360_survey_forms
GROUP BY school_year,audience,stage,cohort;
REVOKE ALL ON public.stg_360_survey_coverage FROM anon,authenticated;
GRANT SELECT ON public.stg_360_survey_coverage TO authenticated;
COMMENT ON TABLE public.stg_360_survey_forms IS 'Typeform 2026: 6º-8º, 9º, Médio e famílias. Sem nome, e-mail nem token do respondente. Dados brutos confidenciais, multi-etapas preservadas. Notas ausentes permanecem NULL.';
