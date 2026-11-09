# STAGIO 360 — Auditoria visual e padronização v9
**Data:** 09/11/2026  
**Referência de design:** captura aprovada da página inicial, com sidebar azul-marinho, hero institucional em degradê, logotipo Stagio 360 branco, cards claros e gráficos multicores.

## Etapa 1 — Sistema visual global

Arquivos:
- `assets/stagio360-visual-v9.css` — tokens e aparência compartilhada de todas as páginas;
- `assets/stagio360-visual-v9.js` — sidebar contextual nas rotas administrativas antigas, tratamento cromático de barras e visualizações adicionais no painel público.

A v9 **não exclui** `assets/stagio360-unified.css?v=8`; ela o complementa com uma camada final de apresentação que mantém as estruturas e chamadas de backend já existentes.

**Paleta semântica e identidade:**
- marinho profundo `#081e43`, azul `#2f73d9`, ciano `#35c4e8`;
- verde `#27ae60` para promotores, âmbar `#e1a32f` para neutros, vermelho `#dc5959` para detratores;
- violeta `#7c5cfa` para séries comparativas e resultados de autoavaliação, quando aplicável;
- superfície clara, borda `#d4e2f2`, radios de 16px e sombras suaves;
- foco visível, modo de movimento reduzido, impressão e layout responsivo.

**Componentes:** sidebar, cabeçalho/hero, logotipo, breadcrumbs, navegação de contexto, botões, filtros, tabelas, cards KPI coloridos, avisos metodológicos, formulários de entrada e recuperação, estados de carregamento e bloqueio.

## Etapa 2 — Tela a tela (19 rotas)

| Grupo | Rotas integradas |
|---|---|
| Portal público | `index.html`, `painel.html` |
| Fundamental I | `fundamental-1/index.html` |
| Núcleo institucional | `admin/index.html`, `admin/minha-area.html`, `admin/segmento.html`, `admin/governanca.html`, `admin/infantil.html` |
| Trabalho pedagógico | `admin/planejamento.html`, `admin/pdi.html`, `admin/revisao.html`, `admin/sintese.html`, `admin/coord-fii-em.html` |
| Fontes e pesquisa | `admin/pesquisas-2026.html`, `admin/academico.html`, `admin/integracao.html`, `admin/funcionarios.html` |
| Acesso e importação | `admin/import.html`, `admin/reset.html` |

**Critério de layout:** rotas que já tinham sidebar (`.shell` ou `.s360-shell`) a conservam e recebem o novo acabamento visual. As rotas antes sem sidebar recebem o menu institucional pelo script compartilhado, com versão recolhível em telas pequenas. Isto evita inserir uma segunda sidebar no mesmo documento.

**Cabeçalho e logo:** a página Minha área passou a ter a marca da Academy na barra lateral e o logotipo Stagio 360 no hero, seguindo a referência da home. Cabeçalhos independentes passaram a usar o mesmo degradê, anéis decorativos sem imagens externas e linha inferior ciano.

**Login e autenticação:** estilos unificados **nas interfaces do portal** (formulários, login, estados sem acesso e reset de senha). Os serviços de autenticação, permissões por usuário e RLS do Supabase não foram modificados. O painel administrativo interno do provedor Supabase — hospedado fora do portal — não faz parte das 19 rotas e não pode ser tematizado simplesmente por esta stylesheet.

## Etapa 3 — Gráficos e indicadores coloridos

**Home e painel público:**
1. Rosca/donut de composição NPS de famílias do recorte, distinguindo promotores, neutros e detratores pelos totais reais do JSON publicado.
2. Barras horizontais coloridas para comparação de NPS **exclusivo** das famílias de EI, FI, FII e Médio, com nota da escala `−100...+100`.
3. Linha histórica NPS de famílias 2023–2025 para o segmento selecionado, com alerta de não comparabilidade do escopo do Infantil e sem tratar o histórico como M1.

Os gráficos só aparecem no recorte **2026 · M1**. A seleção de 2023–2025 ou de M2/M3 não exibe representações incorretas. São usados apenas os arquivos de agregados de fonte `stagio360-2026-agregados.json` e `stagio360-historico.json`, **sem novos números, sem API privilegiada e sem respostas individuais**.

**Demais módulos:** preenchimentos de barras/progressos passam a usar cores distribuídas por série. Valores baixos com marcação explícita usam laranja, e `auto` permanece violeta; comprimentos/percentuais e vínculos com dados continuam calculados pelos próprios módulos. Cards KPI apresentam acento colorido rotativo, preservando texto e denominador.

## Auditoria e aceitação técnica

Novo script `scripts/audit_visual_v9.py` — validado pelo GitHub Actions:
- exige os 19 HTMLs e referências v9 CSS/JS exatamente uma vez por rota;
- exige marcação de body e checa sidebar única (existente ou nova);
- checa logo oficial e preservação de `v8`;
- verifica existência dos gráficos e seletor de ano/etapa/ciclo;
- verifica tokens de cor, responsividade, estados de autenticação, foco e movimento reduzido;
- confere coerência do NPS e presença da série histórica;
- proíbe lógica de credenciais/autenticação no script visual.

Workflows atualizados:
- `Auditoria STAGIO 360`: `scripts/audit_site.py`, `scripts/audit_visual_v9.py`, `node --check` do JavaScript visual, além dos testes JS anteriores;
- `Publicar STAGIO 360 no GitHub Pages`: mesmas auditorias, empacotamento dos assets e conferência HTTP dos dois novos assets e das 19 rotas após publicação.

**Resultado técnico confirmado:** auditoria e publicação passam na Actions do commit de entrega; todos os 19 HTMLs contêm os links de CSS/JS e a marca visual `s360-v9`.

**Limite da verificação:** testes estáticos de código, sintaxe JS, integridade de dados e acessibilidade HTTP não equivalem a uma inspeção visual humana no navegador autenticado. O aceite final precisa conferir contraste real, quebra de linhas, interação de sidebar mobile, login e leitura de gráficos por perfil com uma sessão de usuário autorizado. Esses testes não foram simulados como se tivessem ocorrido.

## Não alterado

- Não foram editadas as tabelas, view ou políticas RLS do Supabase.
- Não houve importação/recalculo de dados, alteração de permissões ou redefinição de senhas.
- Ficam preservadas as pendências de identidade, ciclos e bases já documentadas na auditoria de dados.

## Links

- Portal: https://henriquebovolopes-svg.github.io/stagio-360/
- Painel: https://henriquebovolopes-svg.github.io/stagio-360/painel.html
- Minha área: https://henriquebovolopes-svg.github.io/stagio-360/admin/minha-area.html
- CSS: `assets/stagio360-visual-v9.css`
- JS: `assets/stagio360-visual-v9.js`
