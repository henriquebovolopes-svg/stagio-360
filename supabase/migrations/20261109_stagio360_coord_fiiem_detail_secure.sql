-- STAGIO 360 | Reconciliação granular da coordenação FII / EM (M1-2026)
-- Conteúdo de respostas permanece exclusivamente no Supabase (nunca em GitHub).
-- "shared" identifica a atuação declarada FII + Médio, sem rateio ou dupla contagem.
CREATE TABLE IF NOT EXISTS public.stg_360_coord_fiiem_items (
 source_key text PRIMARY KEY,
 school_year integer NOT NULL DEFAULT 2026 CHECK (school_year >= 2023),
 module text NOT NULL DEFAULT 'M1',
 source_file_id text NOT NULL,
 source_row integer NOT NULL CHECK (source_row >= 1),
 source_block integer NOT NULL CHECK (source_block BETWEEN 1 AND 22),
 source_offset integer NOT NULL CHECK (source_offset BETWEEN 0 AND 16),
 source_teacher_id text NOT NULL,
 teacher_label text NOT NULL,
 subject_label text NOT NULL,
 declared_stage text NOT NULL CHECK (declared_stage IN ('fundamental2','medio','shared')),
 assessment_axis text NOT NULL CHECK (assessment_axis IN ('Planejamento','Condução de aula','Cultura profissional','Formação continuada')),
 question_label text NOT NULL,
 response_kind text NOT NULL CHECK (response_kind IN ('objective','qualitative')),
 score integer,
 response_text text,
 identity_status text NOT NULL DEFAULT 'source_only' CHECK (identity_status IN ('source_only','identity_confirmed')),
 imported_at timestamptz NOT NULL DEFAULT now(),
 CONSTRAINT s360_coord_fiiem_response_shape CHECK (
   (response_kind='objective' AND score BETWEEN 1 AND 5 AND response_text IS NULL)
   OR
   (response_kind='qualitative' AND score IS NULL AND nullif(btrim(response_text),'') IS NOT NULL)
 ),
 UNIQUE(source_file_id,source_row,source_block,source_offset)
);
CREATE INDEX IF NOT EXISTS idx_stg_360_coord_fiiem_stage ON public.stg_360_coord_fiiem_items(school_year,module,declared_stage,response_kind);
CREATE INDEX IF NOT EXISTS idx_stg_360_coord_fiiem_teacher ON public.stg_360_coord_fiiem_items(source_teacher_id);
ALTER TABLE public.stg_360_coord_fiiem_items ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.stg_360_coord_fiiem_items FROM anon, authenticated;
GRANT SELECT ON public.stg_360_coord_fiiem_items TO authenticated;
DROP POLICY IF EXISTS stg_360_coord_fiiem_read_master ON public.stg_360_coord_fiiem_items;
CREATE POLICY stg_360_coord_fiiem_read_master
 ON public.stg_360_coord_fiiem_items FOR SELECT TO authenticated
 USING (EXISTS (
   SELECT 1 FROM public.stg_members m
   WHERE m.user_id = (SELECT auth.uid())
     AND m.active
     AND m.role IN ('admin','master')
 ));
COMMENT ON TABLE public.stg_360_coord_fiiem_items IS
'297 respostas M1 da coordenação FII/EM, sendo 212 notas e 85 narrativas. teacher_id é identificador do arquivo CONFIG, não UUID homologado; shared não pertence exclusivamente a nenhuma etapa.';
CREATE OR REPLACE VIEW public.stg_360_coord_fiiem_coverage
 WITH (security_invoker = true)
AS SELECT
 school_year, module, declared_stage, response_kind, assessment_axis,
 COUNT(*)::integer AS answer_count,
 COUNT(DISTINCT source_teacher_id)::integer AS source_teachers,
 ROUND(AVG(score)::numeric,2) AS score_mean
FROM public.stg_360_coord_fiiem_items
GROUP BY school_year,module,declared_stage,response_kind,assessment_axis;
REVOKE ALL ON public.stg_360_coord_fiiem_coverage FROM anon,authenticated;
GRANT SELECT ON public.stg_360_coord_fiiem_coverage TO authenticated;
