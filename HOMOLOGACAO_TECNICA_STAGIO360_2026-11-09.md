# STAGIO 360 — Homologação técnica do passo 9
**Data de referência:** 09/11/2026
**Escopo:** validar implantação dos nove passos, execução das rotas, navegação, perfis, RLS e integridade dos dados públicos. Sem acesso a senhas pessoais ou testes com identidade simulada no navegador.

## 1. Publicação e execução
- Portal: https://henriquebovolopes-svg.github.io/stagio-360/
- Área pessoal: https://henriquebovolopes-svg.github.io/stagio-360/admin/minha-area.html
- Repositório: https://github.com/henriquebovolopes-svg/stagio-360
- Evidência de base: execução de GitHub Actions de 09/11/2026, revisão `dda8d9d52812fe92cbdb031e9a508a5e06c05169`:
  - Auditoria: https://github.com/henriquebovolopes-svg/stagio-360/actions/runs/42680903446 — **success** (16 páginas, zero erros, sintaxe JavaScript aprovada)
  - Publicação: https://github.com/henriquebovolopes-svg/stagio-360/actions/runs/42680903081 — **success** (implantação GitHub Pages e etapa de confirmação HTTP executadas com sucesso, inclusive CSS, dataset e módulos protegidos)
- Melhorias finais do passo 9: workflow `.github/workflows/deploy-pages.yml` agora consulta as **16 páginas estáticas por HTTP**, exige conteúdo de STAGIO 360 e uso do CSS unificado em cada rota. `scripts/audit_site.py` transforma ausência de logo em erro e impede repetição da classe de tema.
- **Critério de encerramento técnico:** auditar o último commit `main` e confirmar que tanto os workflows `Auditoria STAGIO 360` quanto `Publicar STAGIO 360 no GitHub Pages` concluíram com `success`.

## 2. Correções realizadas na validação
- Eliminada a repetição de `s360-harmonized` nos arquivos `index.html`, `painel.html`, `admin/index.html` e `admin/sintese.html`.
- Incluído o logotipo oficial (SVG branco com `360` e arcos orbitais) nos cabeçalhos `admin/import.html` e `admin/reset.html`, sem alterar os formulários.
- Conservar o visual azul/branco/ciano aprovado, links por etapa e funcionalidades existentes; nenhuma fonte de dados foi alterada.

## 3. Matriz de acesso testada em Supabase
Os testes executaram consultas sob `authenticated`, com `request.jwt.claim.sub` associado a cada UUID real, dentro de transações revertidas. A RLS permaneceu ativa e não houve escrita em registros pedagógicos.

| Perfil | Institucional | Infantil | Fundamental I | Fundamental II | Médio | Escuta dos funcionários |
|---|---|---|---|---|---|---|
| Henrique · administração | Sim | Sim | Sim | Sim | Sim | Sim |
| Giovanna · master | Sim | Sim | Sim | Sim | Sim | Sim |
| Márcia · master | Sim | Sim | Sim | Sim | Sim | Sim |
| Érica · coordenação FI | Não | Não | Sim | Não | Não | Não |
| Patrícia · coordenação EI | Não | Sim | Não | Não | Não | Não |
| Sem vínculo autorizado | Não | Não | Não | Não | Não | Não |

Validações adicionais:
- Márcia recupera indicadores EI, planejamentos de EI e FI e os 27 itens da Escuta.
- Patrícia recupera 10 indicadores EI e 190 entradas de planejamento EI; vê **zero** linhas das entradas FI, docentes FI e itens da Escuta.
- Érica continua restrita ao Fundamental I e sem acesso à pesquisa confidencial de funcionários.
- Sessão autenticada sem membro: zero membros, docentes FI e itens de Escuta recuperados.

## 4. Links, integridade de dados e confidencialidade
- `scripts/audit_site.py` percorre as referências locais de HTML e valida presença dos destinos no repositório; confere IDs duplicados e ausência de chaves privilegiadas.
- O JS de todos os arquivos HTML é validado por `node --check` no workflow `audit.yml`.
- O GitHub Pages disponibiliza apenas HTML, CSS, JS público com chave *publishable* e indicadores agregados. Dados individuais são lidos mediante autenticação e RLS do Supabase.
- Os NPS históricos e atuais mantêm denominadores e populações não intercambiáveis; o Ensino Médio tem amostra de famílias pequena (n=19), com aviso de interpretação mantido.
- Testes com URL de segmento invalidado, conta sem permissão e conta desativada dependem das regras RLS que já foram auditadas no servidor. Nenhuma senha, e-mail ou UUID da equipe foi incorporado ao código deste relatório.

## 5. Riscos residuais e aceitação humana necessária
- **Teste de navegador com contas reais:** cada usuária deve entrar em `Minha área`, conferir menus, carregar dados, usar links e sair. Os testes por JWT simulado não equivalem à execução de login com senha, sessão real e clique.
- **Responsividade visual:** comparar desktop e celular em páginas principais, com dados reais após o login. A auditoria sintática e HTTP não identifica todos os defeitos visuais ou de interação.
- **Auth/Supabase:** o auditor mantém aviso de proteção contra senhas vazadas desabilitada; ativar no painel Auth conforme disponibilidade. Duas RPC `SECURITY DEFINER` chamáveis pelo papel `authenticated` devem continuar sob revisão; possuem checagem ativa de vínculo/admin/master. A tabela privada de autorização da Escuta mantém RLS sem política pública, intencionalmente.
- **Conteúdo pedagógico:** importação e homologação individual de outras etapas/ciclos permanecem diferentes de validação técnica do site. Não afirmar que bases M2/M3 ou avaliações individuais ausentes estejam concluídas.
- **Limite da certificação:** publicação confirmada pelo ambiente GitHub Actions, não por um navegador com acesso privilegiado. A aprovação técnica não é homologação funcional assistida pela direção/coordenações.

## 6. Rotas de aceitação sugeridas
- **Direção:** `/admin/minha-area.html` → Infantil / FI / FII / Médio → integração, planejamento e Escuta (quando concedida).
- **Coordenação FI:** `/admin/minha-area.html` → Fundamental I → professores → pesquisas → PDI.
- **Coordenação EI:** `/admin/minha-area.html` → Educação Infantil → indicadores → planejamento; verificar que FI, FII, Médio e Escuta não aparecem.
- **Portal aberto:** `/` → etapa e ciclo → resultados agregados → acesso protegido → voltar à visão geral.

**Status pretendido:** publicação e auditoria automatizadas comprovadas; pendências de homologação humana e recomendações de segurança claramente discriminadas.
