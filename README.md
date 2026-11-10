# STAGIO 360 — Portal institucional de governança e Avaliação 360

Portal do Colégio Stagio com navegação para direção, coordenações e aprofundamentos por etapa. Identidade visual STAGIO 360 oficial aplicada.

**Acesso ao portal:** https://henriquebovolopes-svg.github.io/stagio-360/

## Refinamento visual v11 — branco nos painéis de dados (09/11/2026)

- **Preservado exatamente como na captura aprovada:** os quatro KPIs da home com fundos pastéis azul, verde, pêssego e violeta; as quatro abas da Avaliação 360; o quadro de escolha da etapa de ensino.
- **Todas as demais caixas de gráficos e dados voltaram ao branco**, incluindo os 19 módulos/rotas. Barras, gráficos, legendas e indicadores semânticos continuam coloridos; botões seguem em tons pastéis para manter o padrão já aprovado.
- A nova folha `assets/stagio360-white-panels-v11.css`, carregada por último, diferencia explicitamente superfícies neutras e os três tipos de destaque pastel. Nenhum dado, política de acesso nem consulta do Supabase foi alterado.
- [Relatório de auditoria do padrão v11](AUDITORIA_VISUAL_STAGIO360_V11_PAINÉIS_BRANCOS.md), com limites do teste visual e critérios de aceitação.

## Ajustes visuais v10 — paleta pastel e navegação simplificada (09/11/2026)

- A home, o painel e a Minha área agora exibem **Avaliação 360** como único atalho principal, sem a opção redundante **Governança**. O menu global dos módulos também foi simplificado.
- **Colaboradores · Privado** substitui “Funcionários · privado” na navegação, preservando a mesma área restrita e suas permissões.
- “PLATAFORMA INSTITUCIONAL” e “ANO DE REFERÊNCIA” receberam texto branco no cabeçalho aprovado.
- As **19 rotas** receberam a camada `assets/stagio360-pastel-v10.css`, após a v9: fundos inteiros de cards, KPIs e quadros em tons pastéis, além de botões coloridos legíveis em todas as áreas de interface.
- O quarto KPI da home deixou de destacar somente o Fundamental I: agora apresenta **NPS institucional de famílias e alunos** diretamente da linha agregada de 2026/M1, com **408 respostas e +40,69**. O indicador misto fica indisponível em recortes históricos ou ciclos não importados, para não induzir comparação metodológica incorreta.
- O menu global usa `assets/stagio360-visual-v10.js`; gráficos e dados continuam independentes dessa mudança de aparência. Não foram modificados Supabase, RLS, credenciais ou registros.
- Testes: `scripts/audit_site.py`, `scripts/audit_visual_v9.py` (ampliado para v10), `node --check assets/stagio360-visual-v10.js` e verificação de 19 rotas HTTP.
- [Relatório de auditoria do refinamento pastel v10](AUDITORIA_VISUAL_STAGIO360_V10_2026-11-09.md).

## Design System v9 — padronização integral de interface (09/11/2026)

- **Referência oficial:** captura da home com sidebar marinho, logotipo STAGIO 360 em branco no hero azul/ciano, cards executivos e barras/gráficos multicores.
- **Etapa 1:** design tokens, tipografia, cards, filtros, formulários de login/reset, botões, tabelas e responsividade compartilhados em `assets/stagio360-visual-v9.css`. Mantido `stagio360-unified.css?v=8` como base de compatibilidade.
- **Etapa 2:** as **19 rotas** principais carregam a camada `v9` e o script `assets/stagio360-visual-v9.js`; as páginas com sidebar existente a preservam e os demais módulos recebem menu lateral contextual. Logo oficial presente em todas as telas, inclusive Minha área.
- **Etapa 3:** home/painel com rosca de NPS (promotores, neutros, detratores), barras comparativas das etapas e série histórica colorida. Barras e KPIs dos módulos têm acentos coerentes por série e alerta sem alterar percentuais.
- Os três gráficos dinâmicos do painel público usam somente os arquivos agregados de 2026/histórico e aparecem somente no recorte 2026 M1. Nenhum dado individual é publicado.
- **Auditoria automatizada:** `python scripts/audit_visual_v9.py`, `node --check assets/stagio360-visual-v9.js`, além de `scripts/audit_site.py` e teste HTTP das 19 rotas e do CSS/JS implantados.
- **Segurança preservada:** mudanças de estilo e navegação não modificam Supabase Auth, RLS, perfis nem o conteúdo dos dados; a UI privada do painel administrativo do serviço Supabase é externa ao site e não está sendo tematizada.
- [Relatório técnico e ressalvas da auditoria visual v9](AUDITORIA_VISUAL_STAGIO360_V9_2026-11-09.md).

## Estrutura atual
- `/` — governança, NPS institucional, históricos 2023–2025 e navegação por segmento.
- `/fundamental-1/` — protótipo validado da Avaliação 360 2026 (2º–5º ano), preservado.
- `/admin/minha-area.html` — entrada autenticada por perfil: cada coordenação vê apenas seus segmentos autorizados, e direção/administração vê as etapas e os módulos institucionais permitidos.
- `/admin/` — área administrativa autenticada, com dados individuais protegidos por Supabase e RLS.
- `/assets/stagio360-historico.json` — indicadores históricos de satisfação calculados por segmento, 2023–2025.
- `/assets/stagio360-2026-agregados.json` — NPS 2026 de famílias e alunos por etapa, com denominadores e critérios objetivos.
- `/admin/governanca.html` — rubricas agregadas de docentes do Fundamental II e Ensino Médio, autenticadas por etapa no Supabase.
- `AUDITORIA_PORTAL_2026-11-08.md` — trilha de verificação, problemas encontrados, correções e pendências.

## Conciliação bruta dos questionários e correção NPS — 09/11/2026
- **423 formulários Typeform e 19.016 respostas a questões** de alunos (6º–8º, 9º e Ensino Médio) e famílias, integrados à tabela protegida `stg_360_survey_forms` e à view `stg_360_survey_items` (RLS, somente admin/master). **408 notas NPS válidas e 15 envios sem nota NPS**. A fonte preserva dados em JSONB sem importar nome, e-mail ou token da pessoa.
- Fonte bruta por coorte: FII 6º–8º 96 formulários/7.804 itens, 9º 41/3.360, Médio 38/3.384, famílias 248/4.468. Os 18.046 itens da arquitetura tratada são recorte transformado, não respondentes adicionais.
- Correção de NPS no Supabase e nos JSONs públicos: alunos 6º–8º **+21,88 (n=96)**; EM **+16,67 (n=36)**; alunos escola **+14,53 (n=172)**; institucional misto **+40,69 (n=408)**. NPS sem resposta permanece ausente, nunca zero.
- A origem conserva **38 blocos de docentes** identificados por intervalos validados de 7 questões (15 FII 6º–8º, 11 do 9º e 12 EM). **13.332 itens** possuem código de professor **da fonte**, não identidade canônica homologada; os demais 5.684 não possuem vínculo docente direto. Em FII, a planilha antiga de mapeamento com deslocamento de seis colunas foi reconstruída segundo os cabeçalhos do Typeform (seis questões objetivas e uma qualitativa), com checagem do primeiro/último campo por bloco.
- As escalas categóricas do FII permanecem categorias textuais; **não receberam nota numérica fabricada**. A view `stg_360_survey_items_mapped` permite consulta de referência de origem, não promove automaticamente identidade de docente.
- `/admin/pesquisas-2026.html`: consulta confidencial de formulários, notas, texto, turma, questão, tipo de resposta e docente **na fonte**, acessível em Minha área e Integração 360.
- Validação RLS: direção/administração veem 423 formulários/19.016 itens/38 blocos, coordenação EI/FI e conta desconhecida veem zero. A resposta livre não integra o site estático público.
- Relatório completo: [Reconciliação integral das pesquisas](RECONCILIACAO_INTEGRAL_PESQUISAS_2026_11_09.md).
- **Atualizações posteriores:** famílias multietapa agora possuem leituras exclusiva e inclusiva protegidas (236 formulários válidos / 283 menções); 7 vínculos FI confirmados por regência/turma (116 planos); 249 resultados Geekie/ENEM históricos integrados em fonte acadêmica própria, sem mistura com a Avaliação 360. **Pendem:** 25 outros vínculos docente-etapa, 51 planos classificados na origem como Infantil embora se refiram ao 1º ano, M2/M3 sem fonte comprovada e homologação de login real. Fotografias importadas não significam atualização automática de novas coletas.

## Integração complementar — famílias, identidades e resultados acadêmicos (09/11/2026)
- A página protegida `/admin/pesquisas-2026.html` passou a mostrar **NPS por etapa exclusivo** (36 EI, 88 FI, 93 FII e 19 Médio; 236 famílias distintas) **e inclusivo** (42 EI, 127 FI, 93 FII e 21 Médio; 283 menções não somáveis). O critério exclusivo conserva os NPS homologados de 2026, com ordem de atribuição FII → Médio → EI → FI, reconstruída pela conciliação de notas da fonte original.
- Dos 32 pares docente-etapa em planejamento, **7 vínculos FI** passaram por checagem de nome único, identidade existente, regência confirmada e turma compatível: **116 planejamentos** agora associados corretamente. Os outros 25 continuam sem vínculo confirmado.
- O painel `/admin/infantil.html` diferencia **190 planos classificados Infantil pela fonte**, sendo **51 do 1º ano ainda pendentes de etapa** e **139 dos outros agrupamentos EI**; não migra automaticamente esses 51 planos para FI.
- História acadêmica individualizada por aplicação/área (não por aluno): **172 resultados Geekie** e **77 ENEM oficial** importados à tabela `stg_360_academic_results`, com RLS admin/master e consulta em `/admin/academico.html`. Onze linhas desalinhadas da origem Geekie foram excluídas. Os dados são resultados escolares agregados por área, distintos do NPS e da avaliação docente.
- Arquivo de reconciliação limpa: [Base acadêmica no Drive](https://docs.google.com/spreadsheets/d/1TZzyw8EsqyGykn9T7b9OzTLe-sy1S6Ct/edit) (XLSX). A matriz original de 96 abas não foi alterada.
- Registro de critérios, discrepâncias, validações e itens ainda pendentes: [Auditoria complementar](RECONCILIACAO_FAMILIAS_DOCENTES_ACADEMICO_2026_11_09.md).

## Passo 7 — Navegação contextual por perfil (09/11/2026)
- Página de acesso: https://henriquebovolopes-svg.github.io/stagio-360/admin/minha-area.html
- O login consulta `stg_members` e, para coordenação, `stg_scope_access`. Contas inativas ou sem etapa autorizada são bloqueadas.
- Coordenação vê exclusivamente as etapas autorizadas e links para módulos compatíveis: Infantil (indicadores e planejamento), Fundamental I (acervo docente, pesquisas, PDI e planejamento), Fundamental II e Médio (rubricas agregadas e planejamento).
- Direção `master` e administração `admin` visualizam todas as etapas, além da integração institucional. A Escuta de Funcionários só é oferecida depois de leitura autorizada no Supabase com RLS específica.
- A tela `admin/segmento.html` passa a permitir voltar a Minha área, inclusive quando uma etapa não está autorizada; os portais públicos incluem um acesso permanente no quadro de cada etapa.
- PDI piloto e Pré-revisão reconhecem a Direção Master; edição do plano continua exclusiva à administração e pareceres mantêm validação no servidor.
- A página somente organiza links: **a autorização real continua sendo aplicada pelo Supabase**, não pela exibição ou ocultação de botões.
- Contas de Márcia e Patrícia ativadas no Supabase em 09/11/2026, com e-mails de Auth confirmados e políticas RLS testadas. Testes reais de entrada no navegador e confirmação do deploy externo ainda são necessários.


## Conciliação da avaliação da coordenação FII/EM — M1/2026

Fonte institucional privada `Typeform_COORD_FIIEM.xlsx` conciliada contra `LONGA_COORD_FII_EM` e `AUDITORIA_COORD_FII_EM` da arquitetura original: **297 registros válidos** (212 notas objetivas, 85 comentários), vinculados a 19 identificadores de docente presentes na fonte. Os 21 docentes ativos na CONFIG não equivalem a 21 respondentes com registros preenchidos.

- FII exclusivo: 111 notas e 46 comentários; Médio exclusivo: 36 notas e 14 comentários; atuação FII+EM: 65 notas e 25 comentários.
- Os 147 itens objetivos de atuação exclusiva já estavam representados nos quatro agregados por eixo de cada etapa. A comparação entre o detalhe importado e os agregados pré-existentes confirmou **8/8 contagens e médias corretas**; nenhuma tabela histórica foi sobrescrita.
- As 90 respostas de docentes de atuação compartilhada ficaram em categoria própria e **não foram somadas a ambas as etapas**.
- Banco: `public.stg_360_coord_fiiem_items` (RLS, SELECT somente `admin/master`) e `public.stg_360_coord_fiiem_coverage` (`security_invoker`). Dados pessoais e textos qualitativos não constam do repositório.
- UI privada: `/admin/coord-fii-em.html`, acessível pelos atalhos de `Minha área` e `Integração 360`. Exibe notas/comentários por origem, etapa declarada, eixo e docente, com textos protegidos e filtros.
- **Limite:** o identificador `P###` é do formulário, não o UUID canônico do perfil 360. A autoavaliação do próprio coordenador e outras questões institucionais da mesma fonte não são parte das 297 respostas docentes, tampouco foram importadas neste lote. Homologação de nomes, compartilhamento por etapa e outros públicos seguem pendentes.
- Detalhes, critérios e testes: [Conciliação da Coordenação FII e EM — M1/2026](INTEGRACAO_COORD_FII_EM_M1_2026.md).

## Passo 8 — Padronização de painéis e experiência visual (09/11/2026)
- **Tema comum:** `assets/stagio360-unified.css`, aplicado em 16 páginas por `body.s360-harmonized`. A folha contém apenas estilo: não altera autenticação, consultas, armazenamento, resultados nem permissões.
- **Identidade preservada:** cores azuis do design aprovado, contraste branco/ciano, tipografia consistente, cantos e bordas de cartões, hierarquia de títulos, KPIs numéricos e logotipo oficial `stagio360-logo-oficial.svg`.
- **Abrangência:** `index.html`, `painel.html`, `fundamental-1/index.html`, `admin/index.html`, `admin/minha-area.html`, `admin/segmento.html`, `admin/infantil.html`, `admin/planejamento.html`, `admin/governanca.html`, `admin/integracao.html`, `admin/funcionarios.html`, `admin/sintese.html`, `admin/pdi.html`, `admin/revisao.html`, `admin/import.html` e `admin/reset.html`.
- **Navegação consistente:** links Minha área e Visão institucional no topo dos cinco módulos de cabeçalho próprio; link Minha área nos menus dos módulos auxiliares FI e do protótipo público FI.
- **Marca oficial:** os cabeçalhos de Síntese Pedagógica, PDI e Pré-revisão agora apresentam o logotipo oficial em vez de somente texto digitado; `h1` permanece presente para acessibilidade.
- **Responsividade/acessibilidade:** controles de foco visível, quebra de texto em cards, contagem tabular, tabelas roláveis e respeito a `prefers-reduced-motion`.
- **Validação contínua:** `scripts/audit_site.py` verifica referência ao tema, classes de ativação, marca e navegação; o workflow de publicação testa o download da nova folha e seu carregamento nas páginas.
- **Homologação visual pendente:** comparar as telas publicadas em desktop/mobile e os estados autenticado, negado e carregando. A publicação do GitHub Pages ainda não foi comprovada externamente nesta sessão.

## Ativação de Márcia e Patrícia — 09/11/2026
- **Márcia:** identidade confirmada no Supabase Auth; papel `master` ativo, acesso a Infantil, Fundamental I, Fundamental II, Médio, integração e planejamento, além da Escuta dos Funcionários mediante autorização privada.
- **Patrícia:** identidade confirmada no Supabase Auth; papel `coordenacao` ativo, somente `infantil`; acesso aos 10 indicadores disponíveis e aos registros de planejamento da etapa, sem acesso a outras etapas nem à Escuta dos Funcionários.
- Validação por sessões SQL simuladas com `authenticated`: Márcia acessa indicadores EI e as 27 questões da Escuta; Patrícia acessa indicadores e planejamento EI, mas não FI, FII, Médio, institucional nem pesquisa interna.
- A página `/admin/minha-area.html` é dinâmica: não precisou de cadastro de usuários por nome no HTML. Perfil e etapas são obtidos via Supabase.
- As duas contas ainda não têm login de navegador confirmado pelo teste de ponta a ponta; senha pessoal, MFA e funcionamento do deploy devem ser verificados com cada usuária.
- **Não armazenar** emails pessoais, senhas, UUIDs de Auth ou listas privadas de autorização no código-fonte público.

## Situação de homologação
**Entregue no repositório:** portal, navegação, NPS agregados de 2023–2026 (distinguidos por público), gráficos por segmento, Fundamental I, rubricas agregadas da coordenação 2026 em rota autenticada e escopo de acesso por etapa no Supabase.

**Ainda pendente:** importação integral das avaliações individuais 360 de alunos, famílias, professores e coordenadores do Fundamental II, Médio e Infantil; testes ponta a ponta de cada perfil e confirmação visual do GitHub Pages. Os NPS agregados de 2026 e os quatro eixos de rubrica docente exclusivos por etapa já foram incorporados. A plataforma não deve ser descrita como 100% homologada antes dessas etapas.

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
- Acesso à tabela `stg_staff_survey_items` e `stg_staff_survey_cycles` definido exclusivamente por `private.stg_staff_access`, **sem privilégio automático para coordenação ou admin genérico**. As contas de Henrique, Giovanna e Márcia estão vinculadas à autorização privada específica. Patrícia e Érica não recebem acesso à Escuta dos Funcionários.
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
- Henrique mantém `admin`; Giovanna e Márcia possuem `master` ativos. Patrícia possui `coordenacao` com acesso exclusivo a `infantil`, e Érica mantém somente `fundamental1`. A regra é checada no banco, não apenas por elementos da interface.
- **Ativação nominal concluída em 09/11/2026:** os dois UUIDs foram confirmados contra as contas verificadas no Supabase Auth e associados a `stg_members`. Patrícia recebeu apenas `stg_scope_access(stage='infantil')`; Márcia, `master` e autorização explícita em `private.stg_staff_access`. Nenhuma senha ou UUID pessoal é armazenado neste repositório público.
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

### Promoção canônica protegida
A página `admin/integracao.html` permite, depois de conferir nome completo e origem documental, promover o registro a identidade canônica independente. A operação auditável é executada por função Supabase para `master/admin`, sem herdar notas M1 e sem inventar correspondência com cadastro antigo; a coluna “Vínculo 360” em `admin/planejamento.html` informa o estado de homologação. Nenhum registro real foi promovido antes da conferência.

### Sugestões de identidade por fonte de autoavaliação
O cadastro pendente oferece sete sugestões de nome completo autodeclarado no `Typeform_PROFS.xlsx`. As sugestões são guardadas em `stg_360_name_evidence`, acessível só à administração/master, sem e-mail ou token. Elas não substituem a validação documental nem associam avaliações automaticamente.

### Conciliação Typeform_PROFS com AUTO M1
Auditadas as 36 respostas da fonte docente contra os 21 critérios AUTO M1: 22 respostas já presentes (462 notas integralmente iguais), oito respostas completas pendentes (168 notas em staging privado) e seis incompletas excluídas dos indicadores. `stg_360_autoeval_reconciliation` e `stg_360_autoeval_pending_scores` têm RLS institucional master/admin; `admin/integracao.html` apresenta os resultados somente após login. Nenhum registro foi reimportado para `stg_teacher_scores`.

### Integração auditável de autoavaliações M1 pendentes
O fluxo `stg_360_integrate_autoeval` integra exatamente 21 notas de uma fonte do Typeform PROFS após a homologação de identidade e etapa, com confirmação e justificativa explícitas de `master/admin`, ledger e restrições contra dupla importação. As novas notas são separadas em `stg_360_identity_autoeval_scores` e entram na view `stg_360_teacher_profile` com origem declarada. Nenhuma das oito fontes pendentes foi efetivamente integrada antes da validação humana.

### Prontidão operacional ao vivo
A seção master/admin em `admin/integracao.html` consulta `stg_360_operational_readiness`, view `security_invoker` com filtro institucional explícito. Mostra planos, pontuações, respostas pendentes, vínculos homologados e estado real M1/M2/M3; preserva distinção entre dados vivos e fotografias do inventário. Os testes de RLS garantiram ausência de linhas para a coordenação limitada ao Fundamental I.

### Matriz transversal homologável por público, etapa e unidade de análise
`admin/integracao.html` conecta em uma matriz institucional as cinco perspectivas — famílias, alunos, professores, coordenação e funcionários — e explicita 23 leituras dinâmicas de 2026. `stg_360_audience_coverage`, `stg_360_fi_class_context` e `stg_360_fi_grade_context` operam em RLS master/admin, com 8 turmas FI e quatro séries de contexto seguro. São proibidas imputação de resposta de aluno/família ao docente por regência, comparação de NPS com questionários heterogêneos, atribuição de clima institucional anônimo a funcionário e mistura de etapas/ciclos não importados.

### Acessos oficiais · 2026
- **Painel geral para compartilhar (sem login, somente agregados):** https://henriquebovolopes-svg.github.io/stagio-360/painel.html
- **Visão histórica ampliada:** https://henriquebovolopes-svg.github.io/stagio-360/
- **Gestão por etapa (login de equipe e restrição por perfil):** https://henriquebovolopes-svg.github.io/stagio-360/admin/governanca.html
- **Governança e homologação (master/admin):** https://henriquebovolopes-svg.github.io/stagio-360/admin/integracao.html
O painel público não disponibiliza escuta de funcionários, textos, PDI, dados individuais nem avaliação nominal. Resultados inexistentes em M2/M3 são identificados como não importados. A publicação real e o login autenticado requerem confirmação externa.

### Identidade visual oficial do acesso geral — 09/11/2026
O painel compartilhável `/painel.html` reutiliza a identidade visual aprovada da página inicial `/index.html`: menu lateral azul-marinho, logo oficial branco, hero azul em degradê com círculo, cartões de indicadores e leitura adaptada a celular. Mantém consulta agregada por etapa/ano/ciclo sem login, enquanto os módulos de gestão continuam autenticados. O preflight testa a presença dos elementos de marca e do arquivo no pacote do GitHub Pages.
