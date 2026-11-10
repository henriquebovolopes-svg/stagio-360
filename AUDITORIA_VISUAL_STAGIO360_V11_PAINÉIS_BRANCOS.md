# STAGIO 360 — Auditoria visual v11: painéis brancos e gráficos coloridos

**Referência:** captura enviada da página inicial em 09/11/2026; revisão aprovada dos quatro KPIs, da navegação em abas e do painel “Escolha uma etapa de ensino”.

## Ajuste solicitado e executado

1. **Exceções com fundo pastel preservado:** apenas os quatro cards principais do recorte de 2026/M1 na home e no painel — Período consultado (azul), NPS de famílias (verde), NPS de alunos (pêssego) e NPS institucional misto (violeta). A barra de quatro abas (“Visão geral”, “Pesquisas”, “Professores”, “PDIs”) permanece em tons pastéis; o painel de escolha de etapa mantém azul suave.
2. **Painéis de dados e gráficos em branco:** cards comuns, quadros de resultados, consultas de pesquisas, histórico acadêmico, avaliações docentes, resultados por público, gráficos NPS, planejamento, integração, formulários de consulta e tabelas voltaram a usar fundo branco e bordas neutras.
3. **Cores preservadas nos dados:** barras de progresso, barras comparativas, linhas de tendência, segmentos de rosca, marcadores, badges e legendas continuam coloridos. Não houve troca de valores, cores semânticas NPS ou denominadores.
4. **Botões:** a decisão anterior de botões em pastel com texto escuro foi preservada, inclusive links de navegação contextual. Sidebar marinho e hero institucional também permanecem.
5. **Segurança:** somente HTML/CSS e scripts de auditoria foram alterados nesta etapa. Não há mudança em tabelas, dados, autenticação ou RLS do Supabase.

## Arquivos e alcance

- Nova camada **`assets/stagio360-white-panels-v11.css`**: é carregada *após* `stagio360-pastel-v10.css`, que por sua vez permanece após o design system v9. Isso explicita, em uma única stylesheet, a regra “dados em branco, quatro destaques pastéis”.
- **19 rotas** passaram a carregar a camada v11, incluindo home, painel, Fundamental I, todas as áreas administrativas e privadas.
- `scripts/audit_visual_v9.py` foi atualizado para exigir presença/ordem da v11 em todas as rotas e a preservação seletiva das quatro exceções e do fundo branco.
- `.github/workflows/deploy-pages.yml` passou a testar existência e download HTTP da nova stylesheet, além de verificar a presença do link v11 nas 19 rotas.
- A funcionalidade e a autenticação dos módulos não foram refatoradas.

## Critérios técnicos de aceitação

- Todos os HTMLs carregam v8, v9, v10 e v11 na ordem correta; o JavaScript v10 de navegação e gráficos mantém sua ordem de execução.
- Os quatro KPIs da home conservam cor explícita de fundo; demais cards e painéis de gráfico recebem `background:#fff!important`.
- A barra de abas e o quadro de escolha de etapa conservam os mesmos tons pastéis da captura.
- A stylesheet v11 **não redefine o preenchimento interno** de donuts nem barras coloridas geradas pelo JavaScript.
- GitHub Actions: auditoria visual, sintaxe do script, verificações de dados e conferência HTTP de 19 páginas.

**Ressalva:** a verificação automática não substitui inspeção visual de navegação com conta autenticada em navegador desktop e mobile. O painel de administração externo do Supabase não é uma rota do site.

Portal: https://henriquebovolopes-svg.github.io/stagio-360/
