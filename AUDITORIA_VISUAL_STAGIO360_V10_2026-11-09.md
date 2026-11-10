# STAGIO 360 — Auditoria de refinamento visual v10
**Data:** 09/11/2026  
**Escopo:** 19 rotas do portal. Sem mudanças de dados, autenticação, RLS ou políticas do Supabase.

## Pedido incorporado

1. **Menu único de Avaliação 360.** A navegação da home, do painel e da Minha área deixou de apresentar o atalho redundante “Governança”. O script da sidebar padronizada também eliminou esse item e mantém “Avaliação 360”. A rota histórica pública `painel.html` e a rota administrativa `admin/governanca.html` foram preservadas para manter compatibilidade com links e permissões — remover o item visual não significa apagar arquivos do sistema.
2. **Colaboradores · Privado.** Novo nome no menu da home, painel, Minha área e sidebar global, preservando o endereço e os dados confidenciais de `admin/funcionarios.html`.
3. **Cabeçalho.** Os rótulos “PLATAFORMA INSTITUCIONAL” e “ANO DE REFERÊNCIA” da home receberam cor `#ffffff`, explicitamente reforçada após o CSS antigo.
4. **Preenchimento de cartões e quadros.** Não apenas a borda ou faixa superior: os fundos inteiros dos KPIs, cards, painéis, blocos de dados, filtros, cards de gráfico e formulários assumiram superfícies sólidas pastéis azul, ciano, verde, violeta, pêssego e rosa. Contrastes de texto e estados importantes foram preservados.
5. **Botões.** Ações principais, secundárias, links com aspecto de botão e navegação contextual utilizam fundos pastéis com texto escuro; a sidebar continua marinho com seleção contrastante, por ser navegação em fundo escuro. Inputs mantêm distinção visual para edição.
6. **Quarto KPI da home.** O bloco antes fixo `NPS das famílias · Fundamental I (+72,73, 88)` foi substituído por **“NPS institucional · famílias e alunos”** com valor apurado da linha `2026 / institutional / misto` do JSON público oficial. O resultado esperado é **+40,69 em 408 notas válidas**, exclusivamente no recorte `2026 · M1`. Em outros anos/ciclos, o card mostra que o indicador não está disponível, sem inventar dados ou tomar valores históricos como equivalentes.

## Implementação
- Novo CSS `assets/stagio360-pastel-v10.css` aplica tons pastéis ao conteúdo das 19 páginas, carregado **depois** do design system v9.
- Novo JS `assets/stagio360-visual-v10.js` preserva os gráficos da v9 e elimina a duplicação na sidebar global.
- Atualizados `index.html`, `painel.html`, `admin/minha-area.html` e os outros 16 HTMLs para carregar a v10.
- Atualizados `scripts/audit_site.py` e `scripts/audit_visual_v9.py` para verificar 4 acessos principais na home, nomenclatura, cores, KPI institucional, CSS pastel e sidebar v10.
- Atualizadas `.github/workflows/audit.yml` e `.github/workflows/deploy-pages.yml` para validar sintaxe do JS v10, links aos novos assets e 19 rotas HTTP.
- Preservado o logotipo oficial Stagio 360 e a fonte histórica dos demais KPIs.

## Limites de aceitação
As verificações automáticas confirmam estrutura, sintaxe, fontes, enlaces e acessibilidade HTTP, **não substituem** avaliação visual em navegador autenticado com diferentes larguras de tela. O console administrativo do serviço Supabase é externo ao site e não recebe o tema do portal; as páginas internas conectadas ao banco recebem o tema.

## Endereços
- Portal: https://henriquebovolopes-svg.github.io/stagio-360/
- Painel: https://henriquebovolopes-svg.github.io/stagio-360/painel.html
- Minha área: https://henriquebovolopes-svg.github.io/stagio-360/admin/minha-area.html
