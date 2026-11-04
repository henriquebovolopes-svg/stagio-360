# STAGIO 360 — PDI Piloto M1/2026

## Objetivo
Converter a leitura das avaliações 360 em **conversas formativas e ações verificáveis**, sem automatizar julgamento individual. Esta etapa opera somente com sete regentes homologadas do Fundamental I.

## Fluxo de trabalho
1. Acesse `/admin/`, faça login e abra **Síntese pedagógica → PDI piloto**.
2. Escolha uma regente. Leia as médias **em suas escalas originais**: coordenação 1–5, autoavaliação 1–4.
3. Selecione deliberadamente uma fonte e um eixo para a conversa; o sistema não elege "pior" professora ou critério.
4. Examine as respostas textuais da coordenação e da própria profissional. Selecione até cinco evidências, sempre com atenção ao contexto.
5. Registre contexto e hipóteses **a verificar**, objetivo observável, ações combinadas, suporte institucional, evidências de acompanhamento, responsáveis e data.
6. Salve como **rascunho**. O botão **Encaminhar para revisão** exige objetivo, ação, indicador, eixo e data, mas **não significa aprovação**.
7. Imprima para discussão. Combine a devolutiva e os compromissos com a professora antes de qualquer validação formal.

## Proteções
- Página estática no GitHub contém apenas código; fichas e textos ficam no Supabase com RLS.
- `admin`: consulta e grava rascunhos/encaminhamentos. `coordenacao`: consulta; não modifica o banco nesta etapa.
- `anon` não tem privilégio de leitura da tabela de PDIs; outro usuário autenticado sem papel autorizado enxerga zero registros.
- PDI inclui referências a evidências da **mesma professora**, fontes `ERICA` ou `AUTO`, janela M1. O banco valida isso. Respostas de alunos e famílias não são vinculadas automaticamente a docentes.
- Uma ficha por regente e por módulo M1, com campos de autoria e última atualização. O piloto ainda **não tem histórico de revisões imutável** nem aprovação eletrônica.
- Desativar acesso público a cópias exportadas, impressões, arquivos compartilhados ou capturas de tela.

## Limites metodológicos
- Há 7 regentes com ambas as fontes, mas as rubricas têm eixos diferentes. Não calcular um índice único comparando diretamente 1–4 e 1–5.
- "Condições de trabalho" é eixo de autoavaliação e implica **responsabilidade da gestão**; não descreva obstáculo estrutural como falha docente.
- Evidências qualitativas têm contexto e podem contrariar inferências de números; confirmá-las em diálogo.
- O M1 não autoriza inferências de evolução. M2 e M3 só serão comparáveis após homologação de instrumentos, versões e amostras.
- **Plano piloto é preparatório**, não homologado, não devendo ser usado isoladamente para decisões trabalhistas.

## Links
- Painel: https://henriquebovolopes-svg.github.io/stagio-360/admin/
- Síntese: https://henriquebovolopes-svg.github.io/stagio-360/admin/sintese.html
- PDI piloto: https://henriquebovolopes-svg.github.io/stagio-360/admin/pdi.html

## Verificações realizadas
- Inserção temporária como administrador: permitida; transação revertida.
- Inserção como coordenação: bloqueada pela RLS.
- Leitura anônima: bloqueada.
- Leitura autenticada sem autorização: zero linhas.
- Leitura como coordenação: permitida.
- Encaminhamento sem data de revisão: rejeitado pelo banco.
