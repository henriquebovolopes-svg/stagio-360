# STAGIO 360 — Conciliação dos questionários originais (09/11/2026)

## Resultado confirmado
**423 formulários de origem**, com **19.016 respostas a perguntas**, preservados em tabela individual protegida no Supabase. Dos formulários, **408 possuem nota NPS válida** e **15 não possuem nota NPS**. Nenhuma ausência recebeu nota zero.

| Fonte | Formulários brutos | NPS válido | Sem NPS | Itens brutos preservados |
|---|---:|---:|---:|---:|
| `Typeform_6a8.xlsx` — FII (6º–8º ano) | 96 | 96 | 0 | 7.804 |
| `Typeform_9ANO.xlsx` — 9º ano | 41 | 40 | 1 | 3.360 |
| `Typeform_EM.xlsx` — Ensino Médio | 38 | 36 | 2 | 3.384 |
| `Typeform_Famílias.xlsx` — famílias multietapa | 248 | 236 | 12 | 4.468 |
| **Total** | **423** | **408** | **15** | **19.016** |

**Unidades:** formulário = envio do Typeform; item = resposta a uma pergunta; nota NPS válida = número de 0 a 10 respondido pelo participante. Não somar o número de itens ao número de respondentes. Os dados brutos foram recuperados dos quatro arquivos Typeform originais existentes no Drive. A matriz-mestra `🧠 ARQUITETURA DO SISTEMA.xlsx` é referência de transformação, não a fonte única de validade quando contém células preenchidas artificialmente.

## Reconciliação dos dados tratados (sem perda nem fabricação de respostas)
- A matriz tratada anterior tem 6.828 itens FII 6º–8º, 3.360 itens 9º, 3.384 itens EM e 4.474 itens de famílias = 18.046. Esses itens são um **recorte de transformação** e não equivalem necessariamente à captura bruta integral, nem são uma população nova.
- Os 7.804 itens brutos do FII incluem tipos de perguntas e dois formulários válidos não incorporados ao tratamento antigo. A expansão não é duplicação de respondentes.
- A aba tratada NPS FII utilizava 94 respostas; a fonte bruta confirma 96 NPS válidos, incluindo duas respostas legítimas (turmas 6º A e 8º A) ausentes na base transformada.
- A planilha analítica do Ensino Médio contava 38 notas, porque **dois campos NPS vazios** haviam sido convertidos em `0`. O Typeform original confirma **36 notas NPS válidas**, e os dois envios são preservados como formulários sem NPS.
- A planilha tratada das famílias tinha 4.474 itens, mas a fonte Typeform confirma **4.468 campos de resposta não vazios**. A diferença corresponde a **seis substituições `N/A`** observadas na aba bruta da arquitetura para perguntas que estão vazias no Typeform: uma em “o que incomoda”, três em “expectativa ainda não acontece” e duas em “que mudança faria mais diferença”. A nova base preserva o campo vazio, sem inventar texto. Os 236 NPS válidos das famílias já estavam corretos.
- Famílias com filhos em duas ou mais etapas continuam representadas por apenas **um formulário de origem**. Os segmentos autodeclarados foram mantidos em metadados, mas os itens não são redistribuídos como respostas exclusivas sem regra institucional.
- Nenhuma avaliação de aluno foi atribuída automaticamente a um professor apenas pela posição de perguntas do formulário; o index da coluna preserva proveniência até homologação do mapeamento dos blocos docentes.

## Indicadores públicos corrigidos e publicados
| Recorte NPS | Antes | Agora | Cálculo validado |
|---|---:|---:|---|
| Alunos FII, 6º–8º | +22,34 / 94 | **+21,88 / 96** | 41 promotores, 35 neutros, 20 detratores |
| Alunos Ensino Médio | +10,53 / 38 | **+16,67 / 36** | 13 promotores, 16 neutros, 7 detratores |
| Alunos da escola | +13,37 / 172 | **+14,53 / 172** | 60 promotores, 77 neutros, 35 detratores |
| Institucional misto (famílias e alunos) | +40,20 / 408 | **+40,69 / 408** | 219 promotores, 136 neutros, 53 detratores |

As 40 notas NPS do 9º ano e as 236 das famílias permaneceram intactas. O NPS histórico 2023–2025 também não foi alterado. A expressão “NPS institucional misto” permanece metodologicamente distinta do NPS exclusivamente familiar.

Os arquivos agregados, sem dados pessoais, foram atualizados:
- `assets/stagio360-2026-agregados.json`;
- `assets/stagio360-nps-publico-2023-2026.json`.

O banco `public.stg_360_nps` também foi corrigido apenas nos quatro recortes acima, com registro da metodologia na nota da fonte.

## Estrutura criada
- `public.stg_360_survey_forms`: **423 formulários** anonimizados em metadados, cada um contendo as respostas completas às perguntas em JSONB protegido, com referências estáveis a arquivo/linha/coluna; nomes, e-mails e tokens de identificação **não importados**.
- `public.stg_360_survey_items`: view `security_invoker` que mostra **19.016 itens** a partir dos formulários, mantendo a mesma RLS.
- `public.stg_360_survey_coverage`: view `security_invoker` com contagem de formulários brutos, itens, notas NPS válidas, ausentes e classes NPS por fonte. Quatro linhas novas foram adicionadas ao inventário `stg_360_source_coverage`, **não** a um novo total de pessoas.
- Migração versionada: `supabase/migrations/20261109_stagio360_survey_forms_2026_secure.sql`.
- UI de direção/admin: `admin/pesquisas-2026.html`, vinculada a `admin/minha-area.html` e `admin/integracao.html`. Possui filtros por fonte, tipo, turma/segmento e questão. O conteúdo livre é revelado sob demanda.

## Segurança e testes
- RLS: administração (Henrique) e Direção Master (Márcia) visualizam 423 formulários e 19.016 itens; coordenadoras FI e EI visualizam 0; identidade autenticada sem vínculo visualiza 0.
- O GitHub Pages contém somente código-fonte, CSS, NPS agregados e autenticação cliente. Não guarda respostas abertas, nomes de alunos, e-mails ou tokens dos formulários.
- Integridade do banco: 423 formulários, 19.016 itens expandidos, 408 NPS não nulos e 15 NPS `NULL`.
- Auditoria `scripts/audit_site.py` valida o recálculo NPS público, vínculos para a nova tela, tema e ausência de referências privilegiadas. O workflow do GitHub Pages verifica por HTTP 18 páginas.
- A homologação interativa com sessão real em navegador da direção ainda é distinta dos testes estáticos/HTTP e do isolamento RLS.

## O que ainda não pode ser considerado concluído
1. Homologação canônica de identidades docentes, turmas e blocos de questionários; os itens de alunos **não foram somados a notas nominais** de professores.
2. Respostas de famílias multietapa não podem ser duplicadas por segmento sem decisão explícita sobre o denominador e a regra de atribuição.
3. Ciclos M2 e M3 não foram captados/importados com evidência documental suficiente; estão sinalizados como ausentes.
4. Base individual da Educação Infantil: indicadores e planejamentos estão presentes; vínculos docentes e parte do 1º ano ainda aguardam conferência.
5. O módulo de resultados acadêmicos Geekie/ENEM (fontes históricas disponíveis na planilha-mestra) ainda não foi importado ao painel de pesquisas: requer preservação de data, aplicação, série e escala distinta da Avaliação 360.
6. O dashboard **não recebe automaticamente novas respostas do Typeform**. A fotografia auditada reflete os arquivos de origem acessíveis em 09/11/2026 e deve ser atualizada por novo ciclo de importação/reconciliação.

**Leitura correta:** concluída a integração e reconciliação das quatro pesquisas originais em âmbito confidencial e das correções NPS; não concluída a triangulação docente longitudinal, nem integração acadêmica histórica.
