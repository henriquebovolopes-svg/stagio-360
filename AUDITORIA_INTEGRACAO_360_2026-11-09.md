# Auditoria de integração institucional 360 — 09/11/2026

## Veredito
**Ainda não existe integração 360 longitudinal ponta a ponta.** O repositório reúne módulos parcialmente conectados, predominantemente um núcleo FI M1 e recortes agregados das demais etapas.

## Critérios auditados
1. Fonte primária e cobertura de público/etapa.
2. Persistência por ano, módulo e unidade observacional.
3. Identificador único que permita relacionar professor, turma, avaliação, planejamento e PDI.
4. Dependências reais entre páginas e banco de dados (não apenas links de navegação).
5. Atualização automática e sincronização de indicadores executivos.
6. Existência efetiva de registros para histórico de devolutivas e acompanhamento.

## Observações verificadas
- Avaliação FI: 25 docentes, 629 pontuações (AUTO 462 e coordenação ERICA 167), 1.400 evidências, 159 estudantes e 127 respostas de famílias no banco; registros indexados em **M1**.
- Rubrica da coordenação FII+EM: oito linhas agregadas referentes exclusivamente a M1 (FII 111 respostas objetivas e EM 36); não corresponde a avaliações nominais trianguladas de todos os professores.
- Educação Infantil: 10 indicadores objetivos agregados, NPS no portal, e planejamento em tabela separada. Nenhum registro individual cruzado de docentes EI na estrutura de `stg_teacher_scores`.
- Funcionários: 27 indicadores e 149 respostas abertas em módulo protegido, sem vínculo com os ciclos ou com o perfil docente.
- Planejamento: 32 linhas `stg_planning_teacher_summary` (190 EI, 119 FI, 13 FII, 14 EM = 336 envios); tabela `stg_planning_entries` com 0 linhas e `stg_planning_reviews` com 0 linhas. A correspondência simples de nome entre essa tabela e `stg_teachers` encontra 0 linhas; ainda falta chave canônica/homologação.
- PDI: 1 plano, 1 revisão e 0 avaliações institucionais registradas.
- Página `index.html`: não lê `stg_*` nem faz `fetch` de `assets/stagio360-historico.json` ou `assets/stagio360-2026-agregados.json`; mantém valores inseridos no HTML. Os arquivos JSON estão presentes, mas não são fonte viva da página principal.
- `fundamental-1/index.html`: página pública de resultados incorporados na marcação e JS. Os dados restritos do FI são consultados separadamente em `admin/`.
- `admin/governanca.html` lê apenas `stg_stage_rubric_aggregates` (+ membros/escopos), não cruza com NPS, planejamento nem acompanhamento.
- `admin/infantil.html` lê indicadores EI, com NPS fixo na página; linka para planejamento, mas não consulta planejamento internamente.
- `admin/planejamento.html` lê `stg_planning_teacher_summary` e `stg_planning_reviews`, sem cruzar registros com professor canônico ou rubricagem 360.

## Escopo da conclusão
Foram inspecionados **código GitHub e dados/políticas do Supabase**. Não foi executado login de usuário em navegador real nem verificada a publicação final no Pages; funcionamento visual ponta a ponta continua pendente de homologação.

## Plano recomendado de conclusão
P0. Definir `school_year`, `cycle_id` (M1/M2/M3), `stage_id`, `teacher_id`, `class_id` e `respondent_role` canônicos; resolver exceções de nomes e distribuição de professores sem atribuição automática.
P1. Importar todas as fontes da matriz original com rastreabilidade (`source_file`, `source_row`, `import_batch`, `source_timestamp`) e separação por privacidade. Registrar lacunas de coleta ao invés de fabricar M2/M3.
P2. Conectar as perspectivas (auto, coordenação, famílias, estudantes, pares/direção, quando existentes) às mesmas unidades e ciclos usando rubrica com escala e critério homologados.
P3. Integrar planejamento por aula e entrega no perfil docente e no PDI, com status de devolutiva separado de notas de qualidade; vincular Drive de modo autorizado.
P4. Substituir dados fixos em `index.html`/EI por consultas a uma camada única de indicadores agregados, com denominadores e metodologia explícitos.
P5. Implantar validação automática de reconciliação por etapa, fonte, ciclo e professor; testes de segregação de acesso RLS e testes de interface para Henrique, Giovanna, Márcia, Patrícia e Érica.

## Implementação subsequente — camada canônica (09/11/2026)

### Estruturas adicionadas
- `stg_360_cycles`: cadastro de ciclos por ano (2026 M1 parcial, M2/M3 não importados).
- `stg_360_source_coverage`: inventário das 14 fontes de 2026 por etapa, período M1/ANUAL, granularidade, quantidade e condição do vínculo docente. Quantidades de itens, respostas e envios são heterogêneas e não podem ser somadas como pessoas.
- `stg_360_teacher_identity`: 25 identidades originadas do identificador UUID da base docente FI (sem criar identidade de docente fictícia).
- `stg_360_planning_crosswalk`: 32 pares professor/etapa/ano aguardando homologação. Nenhum vínculo confirmado automaticamente. Aprovação manual auditável exige conta master/admin, identidade selecionada e justificativa.
- `stg_360_nps`: 25 registros históricos de 2023 a 2026 com ano, etapa, público, universo e denominador. Fórmulas do NPS conferidas (zero divergências acima de 0,08 ponto); Infantil histórico inclui 1º ano, diferentemente da amostra exclusiva EI 2026.
- `stg_360_teacher_profile`: visão `security_invoker` que combina por UUID de origem autoavaliação, coordenação, evidências diretamente atribuídas, PDI e planejamentos **somente após homologação**. Não fabrica escore combinado e não atribui o planejamento anual ao ciclo M1.

### Interface
- `admin/integracao.html`: painel autenticado com filtros de etapa, período, público de NPS, coberturas, estado dos ciclos, fila de homologação e perfis de docentes master.
- Portal institucional `index.html`: incluída navegação para integração e aviso explícito de M1 parcial/M2-M3 não importados.
- Nenhum número individual do banco foi inserido no código público; as consultas da nova interface usam Supabase autenticado.

### Verificações
- A visão de 25 docentes soma 462 respostas AUTO e 167 respostas de coordenação em M1, 288 evidências efetivamente atribuíveis por `teacher_id`, 1 PDI e 0 planos cujo vínculo de identidade foi homologado.
- A base de 1.400 evidências inclui registros não vinculados diretamente a `teacher_id`: não atribuir esses registros automaticamente.
- Tests com impersonação de role autenticado e transações revertidas: Henrique/Giovanna leem 14 fontes, 25 identidades, 32 vínculos e 3 ciclos; Érica lê apenas as 6 fontes e 9 vínculos relativos a FI, sem acesso ao cadastro institucional de identidades/ciclos. A nova view retorna 25 linhas a Henrique/Giovanna e zero a Érica.
- Atualização do crosswalk permitida para Henrique/Giovanna e negada a Érica (transações revertidas).
- JS do painel validado em análise sintática, nenhum ID HTML duplicado e nenhum token secreto detectado nos arquivos inspecionados.
- Supabase security advisor: aviso já existente de proteção contra senhas vazadas desativada e um informe sobre RLS sem política.
- **Ainda não é integração 360 completa**: faltam matrizes M2/M3, demais perspectivas individuais das etapas e importação dos 336 planos por linha. Não verificado GitHub Pages ao vivo; somente arquivos e operações do backend foram confirmados.
