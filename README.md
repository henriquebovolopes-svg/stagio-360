# STAGIO 360 — Portal institucional de governança e Avaliação 360

Portal do Colégio Stagio com navegação para direção, coordenações e aprofundamentos por etapa. Identidade visual STAGIO 360 oficial aplicada.

**Acesso ao portal:** https://henriquebovolopes-svg.github.io/stagio-360/

## Estrutura atual
- `/` — governança, NPS institucional, históricos 2023–2025 e navegação por segmento.
- `/fundamental-1/` — protótipo validado da Avaliação 360 2026 (2º–5º ano), preservado.
- `/admin/` — área administrativa autenticada, com dados individuais protegidos por Supabase e RLS.
- `/assets/stagio360-historico.json` — indicadores agregados calculados por segmento para 2023–2025.
- `AUDITORIA_PORTAL_2026-11-08.md` — trilha de verificação, problemas encontrados, correções e pendências.

## Situação de homologação
**Entregue no repositório:** portal, navegação, indicadores históricos agregados, séries gráficas por segmento, Fund. I, acesso segmentado por etapa no Supabase.

**Ainda pendente:** importação e homologação da Avaliação 360 pedagógica 2026 do Fundamental II, Médio e Infantil; criação de contas reais para Giovanna e Márcia; teste ponta a ponta em navegador real e confirmação do GitHub Pages. A plataforma não deve ser descrita como 100% homologada antes dessas etapas.

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
