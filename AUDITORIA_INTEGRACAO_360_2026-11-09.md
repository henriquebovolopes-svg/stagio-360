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


## Continuação — importação granular dos planejamentos (09/11/2026)
- Os 336 registros de origem foram importados e consultáveis via `stg_planning_entries`. Fonte: Excel original privado, não texto CSV extraído sem validação.
- Os 336 IDs únicos se conciliam com `stg_planning_teacher_summary` sem desvios em nenhum dos 32 pares professor/etapa.
- Campos importados: professor, etapa declarada no formulário, turma, disciplina, data de envio, data da aula quando informada, intencionalidade, habilidades, evidências, reflexão e proveniência.
- No painel `admin/planejamento.html`, o botão `Ver aulas` consulta e apresenta a documentação integral por professor, com expansão individual, escapamento seguro via `textContent` e sem escrever respostas na hospedagem pública.
- **51 de 190 registros classificados na origem como Infantil identificam turma 1º ano**, com flag `first_year_scope_pending`; a direção deve conferir o pertencimento para fins de controle de acesso e análise de etapa. O painel EI explicita essa diferença.
- **Uma data de aula 2016** em registro enviado em 2026 foi preservada com flag `date_requires_review`, sem correção sem fonte.
- A fonte passou a constar como granular anual na tabela `stg_360_source_coverage`, sem inferir equivalência a um ciclo de avaliação M1/M2/M3.
- Testes de RLS feitos em contexto autenticado: Henrique/Giovanna visualizam 336; Érica somente os 119 de FI. Não foram encontradas divergências por professor entre os resumos e os planos individuais.
- Verificação adicional cruzou 20 amostras da extração estruturada com o Excel original (professor/turma); não houve discrepância nessas amostras.
- **Pendente:** homologação de identidades canônicas, atribuição de 1º ano à coordenação correta, reconciliação com o conteúdo dos arquivos `Plano_Oficial_*.docx` e incorporação dos dados efetivos M2/M3 quando existirem. GitHub Pages ao vivo não confirmado nesta rodada.

## Continuação — triagem dos vínculos docentes (09/11/2026)
- Criada `public.stg_360_identity_candidates`: sugestões confidenciais e **não homologadas** de correspondência entre nome abreviado do planejamento e primeiro nome de cadastro docente M1.
- 20 registros de candidatura distribuídos em 19 combinações de etapa/professor, entre 32 combinações totais. Treze combinações permanecem sem correspondência textual; Aline (Infantil) tem duas candidatas distintas, de modo que o primeiro nome não resolve a identidade.
- Das nove combinações de Fundamental I, todas possuem uma candidatura. Seis têm informação de regência FI homologada no cadastro, mas suas associações ao planejamento **continuam pendentes**, até checagem de turma e identidade pela direção.
- Docentes que aparecem em várias etapas ou têm cadastro FI não homologado recebem alerta na fila. Não usar apenas coincidência do primeiro nome para afirmar mesma pessoa; por exemplo, o cadastro M1 `Henrique Cucolo Monteiro` não prova identidade do Henrique do planejamento FII.
- A tela `admin/integracao.html` destaca as sugestões na lista da direção, sem pré-selecionar identidade nem gravar vínculo; a confirmação exige escolha, justificativa e autenticação master/admin.
- RLS confirmada em consultas simuladas: Henrique e Giovanna veem 20 propostas; Érica vê 0. Todas as 32 linhas de `stg_360_planning_crosswalk` continuam sem homologação.
- A verificação externa do GitHub Pages/Actions ainda falhou por indisponibilidade de acesso do ambiente de consulta; portanto não há confirmação de publicação visual.

## Continuação — cadastro canônico pendente (09/11/2026)
- `stg_360_teacher_registry_pending`: criada fila de **13 registros com nome abreviado no planejamento e sem sugestão no cadastro docente M1**: 7 da Educação Infantil, 1 do Fundamental II e 5 do Médio, associados a 143 envios de plano. São registros de origem, **não 13 pessoas de identidade comprovadamente distintas**.
- Campos de conferência: nome completo verificado, situação, origem/fonte da conferência, responsável autenticado e data. O status `ready_for_canonical` exige nome completo e justificativa. Essa etapa **não cria automaticamente professor em `stg_teachers`, não vincula avaliações nem resolve homônimos**.
- `admin/integracao.html` agora permite que direção e administração consultem e registrem a verificação, com turmas do arquivo original. A fila é isolada via RLS: Henrique/Giovanna visualizaram 13 registros e puderam atualizar em transação reversível; Érica visualizou zero e não conseguiu atualizar.
- Verificada sintaxe do JavaScript e ausência de IDs duplicados da página. Não foi estabelecida verificação ponta a ponta do GitHub Pages publicado em navegador autenticado.
- Pendência seguinte: transformar os nomes completos conferidos em identidades canônicas com documentação institucional e ligar ao crosswalk, sem confundir cadastro de planejamento e identidade FI/M1.

## Etapa seguinte — promoção de identidades canônicas após conferência (09/11/2026)

- **Banco:** criada a função transacional `public.stg_360_promote_pending(stage,teacher,year)`, somente para contas ativas com papéis `admin` ou `master`. A operação exige registro `ready_for_canonical`, nome completo verificado, justificativa documental, responsável e data; verifica duplicidade por nome exato, cria uma identidade sem `teacher_id` legado e confirma o vínculo de planejamento com trilha de auditoria.
- **Auditoria:** tabela protegida `stg_360_identity_promotions` registra identidade criada, etapa, nome original, ano, fonte documental, autor e momento da promoção. A função retorna erro quando falta conferência ou existe identidade de mesmo nome, direcionando à conferência de vínculo existente.
- **Perfil 360:** a visão `stg_360_teacher_profile` inclui agora identidades documentais independentes sem inventar ou herdar avaliação M1. Uma identidade nova tem indicadores M1 vazios e apenas os planos da origem homologada.
- **Interface:** `admin/integracao.html` apresenta o botão explícito de promoção somente depois que a conferência foi salva; exige marcar confirmação e distingue cadastro documental de cadastro com avaliação M1. `admin/planejamento.html` indica, por docente, se o vínculo canônico foi homologado.
- **Testes:** promoção de identidade fictícia executada com sucesso em transação revertida; verificados registro de auditoria, vínculo e perfil sem avaliações anteriores. Verificações de RLS: Henrique e Giovanna consultam os 25 perfis e os 13 registros de conferência; Érica não acessa essas estruturas master. Scripts de duas páginas passaram na validação de sintaxe JS e IDs únicos.
- **Situação real ao final:** 25 identidades originais; 13 nomes aguardando conferência; **0 promovidos, 0 vínculos homologados, 0 prontos para promoção**. Não há autorização metodológica para presumir identidade dos docentes com base apenas em primeiro nome.
- **Pendente:** cadastro documental real de cada professor, publicação/verificação no GitHub Pages e integração dos ciclos M2/M3 quando houver dados adequados.

## Continuação — enriquecimento da conferência com Typeform_PROFS (09/11/2026)
- Localizada a fonte `Typeform_PROFS.xlsx` no Drive (`1tX-f-PToiQf6P5jeLS0-yPHjMARXsS4V`), com **36 envios** e **30 nomes completos distintos** (a fonte contém múltiplas respostas de alguns docentes). Não confundir envios com pessoas.
- Extraídos apenas nome completo e segmento autodeclarado para sugestão, **sem importar e-mails, tokens ou respostas dissertativas** para o mapa de integração.
- `stg_360_name_evidence` preserva sete sugestões para registros sem correspondência do cadastro M1: cinco EI (Roseli, Lígia, Ana Paula, Ilci, Daniela) e duas EM (Samantha, Renata). Classificação `self_report_unverified`; todas permanecem dependentes de documento institucional para homologação.
- No painel `admin/integracao.html`, os nomes autodeclarados são mostrados como sugestão e podem ser copiados para rascunho, passando a estado `in_verification` — **não** para `ready_for_canonical` nem para cadastro 360 definitivo.
- Outras seis entradas da fila (Carla, Letícia, Caio, Alessandro, Karina, Rozy) ainda não apresentaram sugestão nessa fonte; isso não prova ausência no quadro de funcionários.
- As avaliações do `Typeform_PROFS` devem ser conciliadas com as pontuações AUTO M1 antes de qualquer importação para evitar respostas contadas duas vezes.
- Controle RLS confirmado: Henrique/Giovanna leem sete sugestões; Érica lê zero. JavaScript da página validado e IDs sem duplicidade. Consulta externa ao GitHub Pages não confirmou acessibilidade devido à limitação do mecanismo de leitura web.

## Conciliação do Typeform_PROFS com a AUTO M1 — 09/11/2026

### Procedimento
- Fonte original do Drive: `Typeform_PROFS.xlsx` (`1tX-f-PToiQf6P5jeLS0-yPHjMARXsS4V`), 36 linhas, 30 nomes distintos, 21 critérios pontuados por resposta completa. Extração CSV com interpretação de campos entre aspas e quebras de linha; validação estrutural de 38 colunas.
- As pontuações existentes em `stg_teacher_scores`, fonte AUTO/M1 (462 valores = 22 professores × 21 critérios), foram comparadas **critério a critério**, com normalização de caixa/espaçamento/acentos no nome completo. A seleção de escores foi verificada somente contra campos numéricos válidos da escala 1 a 4.
- **22 respostas completas idênticas:** 462/462 valores coincidiram, sem discrepâncias. Portanto não houve reimportação, alteração nem duplicação em `stg_teacher_scores`.
- **8 respostas completas ainda não presentes** na AUTO M1: Roseli Finessi Silva de Souza, Ligia Tamião Cazetta da Silva, Samantha Sagioro, Ana Paula de Mesquita Pontes, Ilcicleia Bezerra Silva, Daniela Xavier Sabariego Alves, Renata Daniela Silva Miranda e Gabriela Alves Venzol. Total de 168 notas preservadas isoladamente. A correspondência com identidade canônica deve ser homologada antes de incorporá-las ao núcleo longitudinal.
- **6 linhas incompletas** (sem pontuações válidas nos 21 critérios): três de Helen Sisina Dilser, duas de Aline da Silva Manelli e uma de Gabriela Alves Venzol. Excluídas dos indicadores. Os envios válidos dessas docentes não foram descartados nem somados duas vezes.
- Integridade verificada: 36 linhas conciliadas (22 exatas, 8 completas não importadas, 6 incompletas), 168 notas em staging (8×21), 21 critérios distintos, nenhuma resposta pendente com quantidade diferente de 21 itens.

### Implementação
- `stg_360_autoeval_reconciliation`: 36 registros confidenciais com nome de origem, segmento autodeclarado, linha da fonte, status, número de critérios válidos, autor da fonte e UUID do docente **apenas** quando as 21 notas coincidem integralmente.
- `stg_360_autoeval_pending_scores`: 168 notas completas, confidenciais, destinadas à integração futura **depois** da homologação. Não armazena e-mail, token do Typeform nem respostas dissertativas.
- A tabela `stg_360_source_coverage` ganhou dois itens de inventário, com 36 registros de conciliação e 168 notas em staging; esses totais **não são participantes adicionais**.
- `admin/integracao.html` mostra, para admin/master, resumo 22/8/6, 168 notas em staging e lista nominal das oito respostas completas aguardando vínculo. Dados obtidos por consultas ao banco após login e RLS.

### Testes
- `stg_teacher_scores` permaneceu com 462 AUTO + 167 coordenação; nenhuma gravação nesta tabela.
- RLS: Henrique e Giovanna podem ler os 36 registros e 168 notas; Érica lê zero de ambas as tabelas.
- JavaScript sintaticamente válido; nenhum ID HTML duplicado; nenhuma nota ou nome privado inserido no código estático de integração.
- A verificação externa do GitHub Pages não foi possível pelo mecanismo de consulta web. Não afirmar que houve teste ponta a ponta de login no navegador.

## Integração auditável das oito respostas AUTO M1 (09/11/2026)

- **Implementação concluída sem executar integrações reais:** tabelas restritas `stg_360_identity_autoeval_imports` (histórico de operações) e `stg_360_identity_autoeval_scores` (pontuação por identidade canônica, critério e fonte), com RLS master/admin, PK e restrições de unicidade para impedir duplicação de resposta, docente/ano/critério.
- Função transacional `public.stg_360_integrate_autoeval(source_file_id,source_row,identity_id,justification)` disponível apenas para usuários ativos `master` ou `admin`. Exige justificativa mínima, fonte conciliada completa em 2026/M1, 21 critérios, nome completo compatível, vínculo previamente confirmado na etapa declarada, identidade canônica com revisão adequada e ausência de AUTO M1 anterior na identidade legado ou canônica. Impossível integrar resposta idêntica duas vezes.
- A visão `stg_360_teacher_profile` agora lê autoavaliação original e registros canônicos novos, atribuindo `auto_source_m1`: `auto_original_m1`, `typeform_homologado` ou `sem_autoavaliacao`. Nenhum conjunto de escores é atribuído automaticamente pelo nome; a associação exige crosswalk previamente homologado.
- Em `admin/integracao.html`, cada resposta em staging permite integração manual **somente quando há exatamente uma identidade homóloga com nome completo e segmento homologados**; o usuário precisa preencher justificativa e marcar confirmação. Após integração a tabela é consultada novamente e deixa de contabilizar a resposta como pendente.
- **Validação:** simulação real de promoção de Renata e integração das 21 pontuações dentro de transação revertida; verificadas as 21 linhas canônicas, visão do professor com 21 AUTO, 0 coordenação e 5 planejamentos, um log de importação, e tentativa duplicada bloqueada. Não restou alteração desse teste no banco.
- RLS: Henrique/Giovanna acessam 25 perfis e 36 linhas de conciliação; Érica acessa zero e sua tentativa de executar a função foi negada.
- **Status real depois dos testes:** 0 integrações novas, 0 registros em `stg_360_identity_autoeval_scores`, 8 respostas completas preservadas com 168 notas em staging, 462 notas AUTO legadas inalteradas, 25 perfis canônicos existentes, 0 vínculos homologados. Não afirmar que a ampliação de M1 foi realizada antes da conferência documental.
- O site no GitHub Pages ainda não foi validado com login em navegador; testes são de banco, RLS e análise estática de código.

## Continuação — pré-implantação e verificação automatizada (09/11/2026)

- Auditoria do ambiente externo: URLs oficiais `/stagio-360/`, `/admin/integracao.html` e `/admin/planejamento.html` não puderam ser abertas pelo mecanismo externo utilizado. **Isso não prova queda do site** e não equivale a homologação do GitHub Pages.
- Fortalecido `scripts/audit_site.py`: checa existência dos módulos de integração, planejamento e Infantil; exige consulta às tabelas pertinentes; exige carregamento local de `admin/config.js` e rejeita credenciais privilegiadas na configuração. É um preflight estático, não um teste de login.
- Fortalecido `.github/workflows/deploy-pages.yml`: exige presença física dos três módulos e da configuração no artefato. Após publicação, faz HTTP GET das rotas, testa marcadores funcionais esperados e valida a configuração pública de login.
- Verificação de fonte dos arquivos no GitHub: todos os módulos e marcadores esperados presentes; configuração `./config.js` presente nas três páginas. O resultado do GitHub Actions após a alteração ainda precisa ser observado; não foi possível confirmar o job publicado.
- Estado real do Supabase novamente auditado: **25** identidades canônicas existentes; **0** cadastros prontos para promoção; **0** vínculos homologados; **0** autoavaliações novas integradas; **168** notas em staging de oito respostas completas; **462** notas AUTO M1 existentes. Nenhuma aprovação por aproximação de nomes.
- Próxima ação operacional: concluir conferência documental de professor/etapa na fila master e revisar execução de Actions para confirmar publicação (sem confundir status de CI com teste funcional autenticado).

## Painel de prontidão operacional (09/11/2026)

- Criada a view `public.stg_360_operational_readiness` com `security_invoker=true` para compilar dados **ao vivo** dos módulos oficiais: 336 planejamentos, 462 notas AUTO M1 legado, 167 notas de coordenação, 168 notas em staging, 25 identidades canônicas, 32 vínculos de origem e três estados de ciclos (M1 parcial, M2 e M3 não importados).
- Um teste revelou que uma view baseada apenas em contagens poderia devolver uma linha vazia a usuários fora do escopo. **Corrigido** aplicando filtro explícito `private.stg_scope_authorized('institutional')` na view. Resultados comprovados: Henrique/Giovanna visualizam os totais; Érica recebe zero linhas.
- O painel `admin/integracao.html` ganhou seção `Prontidão operacional`, consultada após autenticação master/admin, com dados obtidos do banco no carregamento da página e aviso separado sobre a última fotografia do inventário `stg_360_source_coverage`. Não confunde ausência de dados de M2/M3 com desempenho zero.
- `scripts/audit_site.py` passou a exigir a referência a `stg_360_operational_readiness`, para evitar retirada acidental do módulo no deploy.
- A publicação real via GitHub Pages não foi validada: a ferramenta pública de consulta não acessou os URLs; uma tentativa alternativa falhou por DNS do ambiente. O conector GitHub disponível não lista execuções push do workflow por ID desconhecido. **Não afirmar deploy aprovado ou login testado.**
- A view é dinâmica, mas o inventário `stg_360_source_coverage` continua representando fotografias históricas e não é recalculado automaticamente.

## Auditoria transversal completa — famílias, alunos, professores, coordenação e funcionários (09/11/2026)

### Inventário verificado e semântica dos cruzamentos
- **Famílias FI M1:** 127 respondentes únicos em `stg_families`; 88 identificados com escopo FI e 39 FI+outras etapas. No recorte estrito de *série única do 2º–5º ano*, 66 casos (2º 19, 3º 15, 4º 14, 5º 18). Os outros 61 formulários **não** foram alocados arbitrariamente a uma série ou docente. Importante: os 88 de escopo FI não são necessariamente os mesmos 88 respondentes NPS FI 2026 — são pesquisas diferentes.
- **Alunos FI M1:** 159 respondentes únicos em oito turmas do 2º ao 5º ano; 477 respostas textuais (três por aluno). Série: 2º 46, 3º 39, 4º 27, 5º 47. Ligações por classe/turma são **contextuais**, não identidade do professor avaliado; turma compartilhada não admite imputação de nota ao docente.
- **Professores AUTO M1:** 462 notas, 22 docentes cadastrados (21 itens cada), transversais a segmentos. 168 itens de oito respostas completas em staging, ainda sem vínculo homologado; 220 evidências dissertativas AUTO com teacher_id.
- **Coordenação FI M1:** 167 itens ligados a 14 docentes por teacher_id, mais 68 evidências textuais ligadas. FII e EM: 111 e 36 respostas objetivas, respectivamente, em agregados de quatro eixos; sem chave individual de avaliador–docente para cruzamento nominal.
- **Escuta de funcionários 2026:** 17 respondentes, 27 indicadores objetivos de seis eixos e 149 comentários codificados, sem identificação individual; **não** constitui avaliação de desempenho pessoal de colaboradores ou professores.
- **NPS 2026:** famílias EI 36, FI 88, FII 93, EM 19; alunos FII 134 (6º–8º 94, 9º 40), EM 38. NPS escolar de famílias e alunos é inventariado em linhas separadas e sem equivalência a survey FI M1. NPS de anos anteriores mantém escopo histórico EI+1º ano.
- **Educação Infantil:** dez indicadores agregados do instrumento baseado em 42 respostas; arquivo de planejamento contém 190 planos na origem EI, sendo 51 registros identificados com 1º ano e ainda sob revisão de escopo. Não foi inventado vínculo nominal dessas famílias com crianças ou professoras.
- **Planejamento:** 336 envios: 190 EI (inclui 1º ano), 119 FI, 13 FII e 14 EM. 32 nomes abreviados por etapa, nenhum vínculo homologado professor–planejamento.

### Correção da cobertura
- Em `stg_360_source_coverage`, AUTO M1 (462 itens) agora tem `stage='institutional'` — a antiga classificação FI exclusiva era incorreta.
- As 1.400 evidências também foram reclassificadas como institucionais com `linked_to_teacher=false` por não serem todas identificáveis: 477 textos alunos, 635 famílias, 220 AUTO e 68 coordenação. Apenas 288 destes 1.400 textos estão diretamente vinculados a docente. A origem específica continua consultável nas tabelas.
- **Não** se criou nenhuma associação por coincidência de turma, primeiro nome, sequência de resposta ou soma de NPS.

### Objetos novos de integração
- `stg_360_audience_coverage`: visão institucional master/admin, `security_invoker=true`, com 23 indicadores dinâmicos por etapa, público, unidade, fonte, nível de associação e ressalva metodológica, cobrindo cinco perspectivas (*familias, alunos, professores, coordenacao, funcionarios*).
- `stg_360_fi_class_context`: oito turmas FI com 159 formulários de alunos, 477 textos e regentes de referência já confirmados. Ligação contextual por turma, sem nota atribuída automaticamente e reconhecendo regência compartilhada.
- `stg_360_fi_grade_context`: quatro séries com respostas de estudantes e recorte das 66 famílias de única série, excluindo registros multietapa e 1º ano.
- `admin/integracao.html`: nova Matriz Transversal com filtros por etapa e público, tabela com ressalvas visíveis, quadros de série e turma; consultas após login somente admin/master.
- `scripts/audit_site.py`: reforçado para exigir as três consultas desta integração no preflight.

### Validação
- Simulações RLS: Henrique e Giovanna veem 23 leituras, cinco públicos, quatro séries e oito turmas; Érica não tem acesso à matriz institucional. Totais das 8 turmas: 159 alunos / 477 textos; quatro séries: 159 alunos / 66 formulários de família exclusiva.
- Sintaxe JavaScript do módulo verificada, IDs HTML únicos e nenhuma resposta textual ou nome confidencial inserido estaticamente na página.
- **Pendências reais:** respostas de alunos/famílias não têm chave validada de docente; FII/EM coordenação permanece agregada; funcionários são anônimos; identidade e planejamento têm 0/32 homologações; M2/M3 não importados. Nenhum desses fatos pode ser descrito como homologação integral ou comparação longitudinal completa.
- As URLs do GitHub Pages não foram acessíveis pelo mecanismo de verificação web desta sessão. Isso não prova indisponibilidade do site; **publicação e login não testados externamente**.
