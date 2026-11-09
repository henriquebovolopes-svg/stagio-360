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

**Ainda pendente:** importação integral das avaliações individuais 360 de alunos, famílias, professores e coordenadores do Fundamental II, Médio e Infantil; contas reais de Giovanna e Márcia; testes ponta a ponta de cada perfil e confirmação visual do GitHub Pages. Os NPS agregados de 2026 e os quatro eixos de rubrica docente exclusivos por etapa já foram incorporados. A plataforma não deve ser descrita como 100% homologada antes dessas etapas.

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
- Acesso à tabela `stg_staff_survey_items` e `stg_staff_survey_cycles` definido exclusivamente por `private.stg_staff_access`, **sem privilégio automático para coordenação ou admin genérico**. Somente a conta confirmada de Henrique foi vinculada. A conta de Márcia ainda precisa ser criada e vinculada após verificação de sua identidade.
- Testes SQL de RLS: Henrique recebe 27 questões; Érica e Giovanna recebem zero; requisições anônimas sem privilégio SELECT.
- Os gráficos do módulo não devem ser interpretados como notas individuais de desempenho.

### Respostas abertas na Escuta dos Funcionários
- 149 respostas originais de nove perguntas dissertativas de `Typeform_ADM.xlsx` foram importadas exclusivamente para `public.stg_staff_survey_comments` com RLS restrita à allowlist privada Henrique/Márcia.
- As perguntas são expansíveis (`<details>`) em `/admin/funcionarios.html`, com exibição integral das respostas apenas após autenticação. Campos originais de e-mail, token, área e data não foram importados ao módulo.
- Os textos podem conter situações autodescritivas capazes de identificar participantes; portanto, continuam confidenciais. O código-fonte público não armazena os textos.
