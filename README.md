# STAGIO 360 — Portal institucional de governança e Avaliação 360

Portal do Colégio Stagio com navegação para direção, coordenações e aprofundamentos por etapa. Identidade visual STAGIO 360 oficial aplicada.

**Acesso ao portal:** https://henriquebovolopes-svg.github.io/stagio-360/

## Estrutura atual
- `/` — governança, NPS institucional, históricos 2023–2025 e navegação por segmento.
- `/fundamental-1/` — protótipo validado da Avaliação 360 2026 (2º–5º ano), preservado.
- `/admin/` — área administrativa autenticada, com dados individuais protegidos por Supabase e RLS.
- `/assets/stagio360-historico.json` — indicadores históricos de satisfação calculados por segmento, 2023–2025.
- `/assets/stagio360-2026-agregados.json` — NPS 2026 de famílias e alunos por etapa, com denominadores e critérios objetivos.
- `/admin/governanca.html` — rubricas agregadas de docentes do Fundamental II e Ensino Médio, autenticadas por etapa no Supabase.
- `AUDITORIA_PORTAL_2026-11-08.md` — trilha de verificação, problemas encontrados, correções e pendências.

## Situação de homologação
**Entregue no repositório:** portal, navegação, NPS agregados de 2023–2026 (distinguidos por público), gráficos por segmento, Fundamental I, rubricas agregadas da coordenação 2026 em rota autenticada e escopo de acesso por etapa no Supabase.

**Ainda pendente:** importação integral das avaliações individuais 360 de alunos, famílias, professores e coordenadores do Fundamental II, Médio e Infantil; contas pessoais de Márcia e Patrícia; testes ponta a ponta de cada perfil e confirmação visual do GitHub Pages. Os NPS agregados de 2026 e os quatro eixos de rubrica docente exclusivos por etapa já foram incorporados. A plataforma não deve ser descrita como 100% homologada antes dessas etapas.

**Privacidade:** não publicar resultados individuais, nomes de estudantes, respostas abertas, planilhas originais com identificadores ou senhas no repositório público.

---

## Histórico do protótipo
Protótipo público do painel de inteligência pedagógica do Colégio Stagio, com indicadores agregados do 1º módulo de 2026.

## Acessar

Após ativar **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root)**:

https://henriquebovolopes-svg.github.io/stagio-360/

## O que esta versão faz

- Painel geral, indicadores de alunos, famílias e docentes
- Nove questões quantitativas dos alunos, com distribuições agregadas
- Quatro eixos docentes (coordenação 1–5 e autoavaliação 1–4), apresentados separadamente
- Explicações metodológicas e limites de interpretação

## Privacidade e limitações

Esta versão pública **não contém respostas individuais, comentários abertos nem perfis de professores ou estudantes**. É uma fotografia estática dos indicadores calculados, sem sincronização automática com a matriz no Google Drive.

Não inserir planilhas originais, exportações Typeform, listas de alunos nem avaliações individuais neste repositório público. Para esses dados, será necessária uma aplicação com autenticação e autorização efetivas.

A taxa definitiva de participação e a evolução para o módulo 2 ainda não estão homologadas.


## Área administrativa (v1.7, aguardando backend)

- Página: https://henriquebovolopes-svg.github.io/stagio-360/admin/
- Login individual preparado para **administração e coordenação**.
- Navegação por profissional, critérios da Érica, autoavaliação, aluno pseudonimizado, família e busca dissertativa.
- **Não há registros individuais no GitHub Pages.** A página permanece bloqueada até a configuração de autenticação e importação em Supabase protegido.
- Migração SQL RLS: [supabase/migrations/20261104_stagio360_secure.sql](supabase/migrations/20261104_stagio360_secure.sql).
- Procedimento de ativação e homologação: [DEPLOY_ADMIN.md](DEPLOY_ADMIN.md).

Atenção: a chave `service_role`, os arquivos com respostas individuais e as senhas **nunca** devem ser enviados a este repositório público.

## Validação contínua e publicação
- `python3 scripts/audit_site.py` valida links locais, IDs, integridade do NPS, logo e presença acidental de credenciais privilegiadas.
- `.github/workflows/audit.yml` executa esses testes e confere a sintaxe JavaScript em pushes e pull requests.
- `.github/workflows/deploy-pages.yml` tenta publicar automaticamente a branch `main` depois da validação.
- Em **Settings > Pages**, a fonte precisa estar configurada como **GitHub Actions**. O estado externo do Pages não foi confirmado pela integração disponível. O workflow sozinho não garante que o site já esteja no ar.

## Escuta dos Funcionários — confidencial
- `/admin/funcionarios.html`: painel autenticado de pesquisa institucional interna, alimentado pelo arquivo privado `Typeform_ADM.xlsx` (2026).
- 17 respondentes, 27 questões objetivas, 6 dimensões. Respostas abertas e endereços de e-mail não foram publicados nem copiados ao novo banco.
- Os itens formulados negativamente (excesso de demandas sem contexto, mudanças de orientação e dependência de pessoas específicas) são recodificados na escala favorável 1–5; médias originais permanecem disponíveis na tabela restrita para auditoria.
- Acesso à tabela `stg_staff_survey_items` e `stg_staff_survey_cycles` definido exclusivamente por `private.stg_staff_access`, **sem privilégio automático para coordenação ou admin genérico**. As contas existentes de Henrique e Giovanna estão vinculadas. Márcia precisa de uma conta pessoal autenticada e conferência de identidade.
- Testes SQL de RLS: Henrique e Giovanna recebem 27 questões; Érica recebe zero; requisições anônimas sem privilégio SELECT.
- Os gráficos do módulo não devem ser interpretados como notas individuais de desempenho.

### Respostas abertas na Escuta dos Funcionários
- 149 respostas originais de nove perguntas dissertativas de `Typeform_ADM.xlsx` foram importadas exclusivamente para `public.stg_staff_survey_comments` com RLS restrita à lista privada de autorização Henrique/Giovanna/Márcia.
- As perguntas são expansíveis (`<details>`) em `/admin/funcionarios.html`, com exibição integral das respostas apenas após autenticação. Campos originais de e-mail, token, área e data não foram importados ao módulo.
- Os textos podem conter situações autodescritivas capazes de identificar participantes; portanto, continuam confidenciais. O código-fonte público não armazena os textos.

## Educação Infantil e acompanhamento docente — 09/11/2026
- `/admin/infantil.html`: painel autenticado para Patrícia e perfis institucionais; inclui NPS das famílias de 2026 (+75,0; 36 respostas), **10 indicadores objetivos confirmados na síntese executiva** (base de 42 respostas, escala 1–4) e três frentes de ação institucional. O 1º ano aparece no agrupamento de planejamento do formulário, mas **não deve ser confundido com a população do NPS de Educação Infantil**.
- `/admin/planejamento.html`: painel reservado com filtros de etapa, professor e turma; fotografia de **336 registros** da base original de planejamento de 2026 e **32 pares professor-etapa** em `stg_planning_teacher_summary`, incluindo contagens por campo e última entrega registrada.
- `stg_planning_reviews`: acompanhamento persistente, com status de análise e notas de devolutiva. Uma coordenação só pode consultar e registrar devolutiva na própria etapa; perfis `admin` e `master` abrangem todas as etapas.
- Henrique mantém `admin`, Giovanna possui `master` ativo e Márcia será `master` após criação e identificação da conta. Patrícia será `coordenacao` com acesso exclusivo à etapa `infantil`. Érica mantém `fundamental1`. A regra é checada no banco, não apenas por elementos da interface.
- A conta de Patrícia **ainda não existe** na autenticação. Depois de criada, um administrador deverá confirmar seu identificador de Auth, associá-la a `stg_members` como `coordenacao` e criar somente o vínculo `stg_scope_access(stage='infantil')`. Para Márcia, associar `stg_members(role='master')` e criar a autorização específica para Escuta dos Funcionários em `private.stg_staff_access`. Não conceder permissões a nomes textuais ou endereços de e-mail não confirmados.
- Fonte de planejamento: arquivo original Excel do formulário, com data de fotografia (não é sincronização automática). A pasta no Drive `PLANOS DE AULA` foi localizada; os documentos na pasta dependem das permissões próprias do Google Drive, e a revisão de conteúdo individual permanece distinta da contagem de envios.
- Segurança testada com transações reversíveis: Henrique e Giovanna podem registrar status EI; Érica é impedida de registrar acompanhamento EI. A publicação do GitHub Pages e testes de login em navegador real ainda exigem confirmação.

## Integração 360 canônica — novembro de 2026
- Governança integrada restrita: `/admin/integracao.html` (por login Supabase e RLS).
- Registros de origem por ano/ciclo/etapa: `stg_360_cycles` e `stg_360_source_coverage`; levantamentos anuais são classificados como `YEAR`, sem falsamente pertencer a M1.
- Histórico NPS agora também normalizado em `stg_360_nps`, com amostra, público e abrangência explícitos. Séries de populações diferentes não são mescladas.
- Identidades antigas da base docente FI preservadas em `stg_360_teacher_identity`; vínculos com `stg_planning_teacher_summary` são homologados manualmente em `stg_360_planning_crosswalk`. Nenhum matching aproximado ganha status confirmado sem validação humana.
- `stg_360_teacher_profile` é uma visão invoker que cruza indicadores FI M1, PDI e planejamento **somente quando identidade estiver homologada**; acesso reservado a `admin` e `master`.
- O mapa de integração ainda não é uma análise longitudinal completa: M2/M3 não foram importados, avaliações por múltiplos públicos de todos os segmentos ainda não compartilham chaves canônicas e o painel inicial ainda contém números estáticos de agregados previamente auditados.


### Planejamento 2026 — importação individual concluída
- Foram importados **336 planos individuais** da planilha original `PLANO DE AULA | Colégio Stagio (respostas).xlsx` para `public.stg_planning_entries`. Identificadores estáveis `sheet2026_2` a `sheet2026_337` permitem importação idempotente.
- Os campos de intencionalidade, habilidade/campo da BNCC, evidências e reflexão ficam **somente no Supabase com RLS por etapa**; nenhum texto pedagógico foi enviado ao repositório público.
- Em `/admin/planejamento.html`, a coordenação pode clicar em **Ver aulas** para recuperar os planos integrais enviados pelo professor. Há status/devolutiva separados no acompanhamento por docente.
- Conciliação da base: 190 registros classificados no formulário como Infantil, 119 FI, 13 FII, 14 EM = 336, distribuídos entre 32 pares professor/etapa. Os registros conferem com a base-resumo existente.
- **Ressalvas:** 51 envios classificados pelo formulário como Infantil têm turma `1º ano`, marcados com `first_year_scope_pending` até homologação; um registro de Ensino Médio informa aula em 2016, marcado `date_requires_review`. Não modificar silenciosamente a data de origem nem transferir os registros para outra etapa.
- `stg_360_source_coverage` passou a incluir quatro fontes de planos individuais (ano, não M1/M2/M3), que se somam às fontes-resumo. Não somar fontes individuais com seus próprios resumos como se fossem respondentes diferentes.
- Verificações: 336 IDs únicos; zero divergências por professor entre resumo e registros importados; acesso completo a Henrique e Giovanna, somente FI a Érica; ausência de acesso EI para Érica.

### Conferência de cadastro docente (09/11/2026)
- Direção/master encontra em `/admin/integracao.html` uma fila de 13 registros de docentes ainda sem correspondência no cadastro M1. Pode informar nome completo, situação, referência documental e salvar a conferência, com atribuição de usuário.
- Esses 13 registros são identificadores de origem por etapa, não equivalem necessariamente a 13 pessoas únicas. Nenhum foi unido automaticamente a avaliações ou a outro registro de planejamento.
- Novos campos são armazenados em `stg_360_teacher_registry_pending` sob RLS de direção/admin. Confirmação do nome **não** promove automaticamente a identidade global nem homologa a relação com avaliação.
