-- STAGIO 360 | Serie academica historica independente da Avaliacao 360 docente.
-- Origem: TRATADA_GEEKIE (172 linhas validas) e TRATADA_ENEM_OFICIAL (77).
-- As 11 linhas deslocadas na TRATADA_GEEKIE sao excluidas do conjunto de simulados.
CREATE TABLE IF NOT EXISTS public.stg_360_academic_results(
 source_key text PRIMARY KEY,
 source_file_id text NOT NULL,
 source_sheet text NOT NULL,
 source_row integer NOT NULL CHECK(source_row>=2),
 provider text NOT NULL CHECK(provider IN ('geekie','enem_oficial')),
 school_year integer NOT NULL CHECK(school_year BETWEEN 2000 AND 2100),
 application text NOT NULL,
 grade_label text NOT NULL,
 academic_area text NOT NULL,
 students_count integer CHECK(students_count IS NULL OR students_count>=0),
 stagio_mean numeric NOT NULL CHECK(stagio_mean BETWEEN 0 AND 1000),
 reference_mean numeric CHECK(reference_mean IS NULL OR reference_mean BETWEEN 0 AND 1000),
 difference_from_reference numeric,
 ranking_text text,
 rank_position integer CHECK(rank_position IS NULL OR rank_position>0),
 rank_total integer CHECK(rank_total IS NULL OR rank_total>0),
 rank_city integer CHECK(rank_city IS NULL OR rank_city>0),
 category text,
 imported_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(source_file_id,source_sheet,source_row),
 CONSTRAINT academic_provider_shape CHECK(
  (provider='geekie' AND reference_mean IS NOT NULL AND students_count IS NOT NULL)
  OR (provider='enem_oficial' AND reference_mean IS NULL)
 )
);
ALTER TABLE public.stg_360_academic_results ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.stg_360_academic_results FROM anon,authenticated;
GRANT SELECT ON public.stg_360_academic_results TO authenticated;
DROP POLICY IF EXISTS stg_360_academic_results_management_read ON public.stg_360_academic_results;
CREATE POLICY stg_360_academic_results_management_read
 ON public.stg_360_academic_results FOR SELECT TO authenticated
 USING (EXISTS(SELECT 1 FROM public.stg_members m WHERE m.user_id=(SELECT auth.uid()) AND m.active AND m.role IN ('admin','master')));
CREATE INDEX IF NOT EXISTS idx_360_academic_year ON public.stg_360_academic_results(provider,school_year,grade_label,academic_area);
CREATE OR REPLACE VIEW public.stg_360_academic_coverage WITH(security_invoker=true) AS
SELECT provider,school_year,COUNT(*)::integer AS result_rows,
 COUNT(DISTINCT academic_area)::integer AS areas,
 COUNT(DISTINCT application)::integer AS applications,
 COUNT(DISTINCT grade_label)::integer AS grades
 FROM public.stg_360_academic_results
 GROUP BY provider,school_year;
REVOKE ALL ON public.stg_360_academic_coverage FROM PUBLIC,anon,authenticated;
GRANT SELECT ON public.stg_360_academic_coverage TO authenticated;
COMMENT ON TABLE public.stg_360_academic_results IS
'Registros por ano, aplicacao, serie e area. Nao equivalem a estudantes distintos. Geekie (simulado) NAO e ENEM oficial. Acesso exclusivo admin/master; nao misturar com notas docentes/NPS.';
