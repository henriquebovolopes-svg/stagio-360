-- Blocos de 7 perguntas de cada docente, reconciliação de fonte (não identidade canônica)
CREATE TABLE IF NOT EXISTS public.stg_360_survey_teacher_blocks (
  cohort text NOT NULL CHECK(cohort IN ('fii_6a8','fii_9ano','em')),
  block_number integer NOT NULL CHECK(block_number BETWEEN 1 AND 20),
  first_source_column integer NOT NULL CHECK(first_source_column >= 1),
  last_source_column integer NOT NULL CHECK(last_source_column = first_source_column + 6),
  source_teacher_id text NOT NULL,
  teacher_source_label text NOT NULL,
  mapping_reference text NOT NULL,
  identity_status text NOT NULL DEFAULT 'source_only' CHECK(identity_status='source_only'),
  PRIMARY KEY(cohort,block_number),
  UNIQUE(cohort,first_source_column),
  UNIQUE(cohort,last_source_column)
);
ALTER TABLE public.stg_360_survey_teacher_blocks ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.stg_360_survey_teacher_blocks FROM anon,authenticated;
GRANT SELECT ON public.stg_360_survey_teacher_blocks TO authenticated;
DROP POLICY IF EXISTS stg_360_survey_blocks_master ON public.stg_360_survey_teacher_blocks;
CREATE POLICY stg_360_survey_blocks_master ON public.stg_360_survey_teacher_blocks
 FOR SELECT TO authenticated USING (
 EXISTS(SELECT 1 FROM public.stg_members m WHERE m.user_id=(SELECT auth.uid()) AND m.active AND m.role IN ('admin','master'))
);
CREATE OR REPLACE VIEW public.stg_360_survey_items_mapped WITH(security_invoker=true) AS
SELECT i.*,b.block_number,b.source_teacher_id,b.teacher_source_label,b.mapping_reference
FROM public.stg_360_survey_items i
LEFT JOIN public.stg_360_survey_teacher_blocks b
ON i.cohort=b.cohort AND i.source_column BETWEEN b.first_source_column AND b.last_source_column;
REVOKE ALL ON public.stg_360_survey_items_mapped FROM anon,authenticated;
GRANT SELECT ON public.stg_360_survey_items_mapped TO authenticated;
COMMENT ON TABLE public.stg_360_survey_teacher_blocks IS 'Vínculos apenas de bloco de origem validado por 7 perguntas; códigos P/B podem variar entre formulários. Não liga automaticamente a UUID docente.';
