# STAGIO 360 — Conciliação adicional de famílias, identidades docentes e histórico acadêmico
**Data de execução:** 09/11/2026

## 1. Famílias que declararam mais de uma etapa

A fonte bruta `Typeform_Famílias.xlsx` tem **248 envios**, dos quais **236 têm nota NPS válida** e **12 não têm**. A consulta `stg_360_family_stage_membership`, com `security_invoker=true`, distingue:
- **Exclusivo (um destino por formulário):** reconstrução exata da regra histórica que reproduz a tabela `stg_360_nps`, prioridade FII > Médio > Infantil > FI.
- **Inclusivo (menção de etapa):** contabiliza cada etapa mencionada, mas o mesmo formulário pode constar em várias etapas. Não somar os recortes inclusivos para obter o número de famílias distintas.

| Etapa | Famílias atribuídas exclusivamente | NPS exclusivo oficial | Menções inclusivas | NPS inclusivo exploratório |
|---|---:|---:|---:|---:|
| Infantil | 36 | +75,00 | 42 | +71,43 |
| Fundamental I | 88 | +72,73 | 127 | +68,50 |
| Fundamental II | 93 | +38,71 | 93 | +38,71 |
| Ensino Médio | 19 | +73,68 | 21 | +71,43 |
| **Total de linhas de etapa** | **236** | **não somar NPS** | **283** | **não somar NPS** |

Validação SQL: 4/4 contagens e 4/4 NPS exclusivos reproduzem exatamente os dados anteriores; a consulta inclusiva retorna 283 menções para 236 famílias com nota. Famílias não são duplicadas no NPS oficial. As novas visões são restritas pela RLS da tabela de formulários, com acesso somente a admin/master. A página `admin/pesquisas-2026.html` exibe os dois resultados com esclarecimento metodológico.

## 2. Vínculos entre docentes e planos do Fundamental I

Inicialmente, havia 32 combinações docente/etapa sem vínculo canônico confirmado. A auditoria cruzou:
- o cadastro institucional `stg_teachers` com função expressa **REGENTE CONFIRMADA**;
- a `stg_360_teacher_identity` com `review_status='verified_existing_id'`;
- o nome de origem dos planejamentos;
- a correspondência da turma do registro `stg_planning_entries.classroom` às turmas homologadas do docente;
- a inexistência de múltiplos candidatos nesse subconjunto.

**Sete vínculos FI** passaram por todas as checagens e receberam `link_status='confirmed'` e `identity_id` no `stg_360_planning_crosswalk`, com justificativa técnica datada e `reviewed_by=NULL` (sem atribuir revisão humana a pessoa que não revisou). Correspondem a **116 envios de planejamento**; os **25 demais pares** continuam pendentes. Nenhum vínculo foi confirmado apenas por coincidência isolada do prenome. A confirmação é do **vínculo identidade–origem do planejamento**, não equivale a avaliar a qualidade pedagógica das 116 aulas.

## 3. Educação Infantil / 1º ano

Dos **190 planejamentos** que o formulário de origem classificou como `infantil`, **51 estão marcados como 1º ano**, envolvendo 3 docentes. Permanecem com `data_quality='first_year_scope_pending'`. Portanto:
- **139 planos** referem-se aos outros recortes da Educação Infantil;
- **51 planos** são do 1º ano no agrupamento da origem, **não foram movidos** ao Fundamental I enquanto a classificação institucional não estiver homologada;
- o painel `admin/infantil.html` exibe separadamente os três números (190, 51, 139).

Os 10 indicadores de satisfação das famílias EI e o NPS EI 2026 continuam a utilizar populações distintas dos planejamentos. O recorte histórico “Infantil e 1º ano” não é comparável diretamente com EI 2026.

## 4. Geekie e ENEM oficial — histórico acadêmico

Origem: planilha-mestra `🧠 ARQUITETURA DO SISTEMA.xlsx`, com 96 abas, encontrada no Drive e conferida em formato Excel. Foram analisadas as abas `TRATADA_GEEKIE` e `TRATADA_ENEM_OFICIAL` (com uso das linhas e cabeçalhos da fonte para proveniência).

| Fonte | Registros válidos integrados | Distribuição |
|---|---:|---|
| Simulados Geekie | **172** | 2021 (52); 2022 (36); 2024 (24); 2025 (60) |
| ENEM oficial | **77** | 2013 a 2022 (7 por ano), e 2024 (7) |
| **Total** | **249** | Todos com identificador e localização de origem distintos |

- A transformação `TRATADA_GEEKIE` contém 183 linhas com conteúdo; **11 linhas deslocadas/sem layout válido de simulado** foram excluídas, não contadas como novos simulados.
- O ENEM oficial contém 77 linhas válidas, com 7 áreas/indicadores por ano. **Não há linha do ano 2023 nesta fonte**, o que não equivale a nota zero ou ausência da avaliação real.
- Os 249 registros foram integrados à tabela `public.stg_360_academic_results`, com colunas de ano, provedor, aplicação, série, área, quantidade informada de alunos quando disponível, média Stagio, média de referência Geekie quando aplicável, diferença e ranking/classificação. Nenhum dado de aluno identificado foi importado.
- A view `stg_360_academic_coverage` tem 15 recortes provedor×ano, e é `security_invoker`.
- Segurança: `public.stg_360_academic_results` tem RLS, papel `anon` sem SELECT, e `authenticated` somente com perfil ativo admin/master. Márcia viu 249 registros; Patrícia viu zero. Integridade: 249 IDs/locais de origem únicos, sem médias obrigatórias vazias.
- Consulta privada: `admin/academico.html`. A página não calcula média indiferenciada entre aplicações, nem mistura notas de simulados com resultado oficial ou com rubrica docente. O inventário `stg_360_source_coverage` contém agora as fontes acadêmicas classificadas como `aggregated`, sem vínculo com docentes.
- A versão limpa do acervo (abas Geekie, ENEM e auditoria) foi salva no Drive como `STAGIO360_Base_Academica_Conciliada_2026.xlsx`. A planilha-fonte original não foi editada.
- Banco versionado em `supabase/migrations/20261109_stagio360_academic_history_secure.sql` e fonte acadêmica privada referenciada no painel.

## 5. O que ainda depende de decisão ou fonte comprobatória
1. **25 vínculos de professor/etapa** sem a mesma certeza documental; aceitar nome abreviado ou código Typeform como identidade canônica exigiria evidência adicional. Permanecem pendentes, não omitidos.
2. **51 planos de 1º ano**: a matrícula curricular exige classificação definitiva da etapa e conferência da natureza pedagógica dos campos de experiência; mantidos separados.
3. **Ciclos M2 e M3**: não foi encontrada fonte inequívoca de Avaliação 360 dessas janelas no inventário consultado; no banco permanecem `not_imported`, sem supor notas inexistentes.
4. **Autenticidade de decisões humanas**: os sete vínculos foram homologados pela verificação documental técnica, não por clique/revisão manual de responsável. A direção pode validar ou contestar a correspondência.
5. **Testes com login real**: validação HTTP/JS/RLS é necessária, mas não substitui a aceitação visual e funcional com conta de direção.
6. **Atualização de novas coletas**: os dados refletem snapshots das fontes disponíveis em 09/11/2026, não integração contínua dos serviços Typeform ou Geekie.

**Resumo:** implementadas as duas leituras de famílias, sete vínculos FI de alta evidência, classificação visível do 1º ano e 249 resultados acadêmicos históricos protegidos. As restrições de identidade, acesso e metodologia permanecem explícitas.
