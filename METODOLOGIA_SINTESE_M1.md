# STAGIO 360 — Protocolo de leitura da Síntese Pedagógica M1/2026

**Situação:** primeira janela importada e auditada; documento de apoio metodológico para direção e coordenação.

## 1. População de análise

A base possui 25 profissionais cadastrados. **A leitura principal usa 7 regentes com vínculo confirmado** (2º a 5º anos). Os outros 18 registros abrangem especialistas, atuação fora do núcleo 2º–5º e vínculos de atuação FI ainda não homologados. Há uma opção explícita para consultar os demais registros **sem misturá-los automaticamente** ao recorte principal.

No recorte das 7 regentes, as duas fontes estão disponíveis para as sete: 84 critérios de coordenação e 147 de autoavaliação. Para toda a base, há 167 avaliações numéricas de coordenação, 462 de autoavaliação, 1.400 textos de várias fontes, 159 registros estudantis e 127 familiares.

## 2. Escalas e critérios

- **Coordenação / Érica:** escala de 1 a 5; quatro eixos (Condução da aula, Cultura profissional, Desenvolvimento profissional, Planejamento).
- **Autoavaliação:** escala de 1 a 4; cinco eixos, incluindo **Condições de trabalho**, que não está representado na avaliação da coordenação.
- As escalas são ordinais e podem ter formulações distintas nos critérios. Não subtrair médias de origens diferentes e **não produzir um índice unificado ou ranking**.
- As barras da visualização são relativas à posição dentro da escala original, usando `(média - 1)/(máximo - 1)`; não são probabilidades nem uma equivalência entre fontes.
- Uma média por eixo é primeiro calculada para cada profissional no eixo; o resumo do grupo é a média entre profissionais com registros naquele eixo (mesmo peso por profissional).

## 3. Evidência qualitativa

A página consulta textos individuais **somente após a seleção e ação explícita** do gestor autorizado, por `teacher_id`, com fontes `ERICA` e `AUTO`. As respostas de alunos e famílias não estão vinculadas diretamente a professoras. Não atribuir opinião de aluno ou família a um docente específico sem desenho avaliativo que sustente esse vínculo.

## 4. Uso formativo

A 'pauta para PDI' é **preparatória**, não um PDI concluído, automático ou homologado. O(s) eixo(s) de menor média **dentro da mesma fonte e ficha** deve(m) funcionar como convite à reflexão, não como diagnóstico ou classificação do profissional.

Antes da decisão pedagógica, a gestão deve discutir evidências observáveis, contexto institucional, práticas e condições de trabalho, metas relevantes e suporte disponível. Os registros qualitativos podem corroborar, tensionar ou contextualizar os resultados numéricos.

## 5. Limitações e evolução

- A análise contém apenas M1/2026. Não mostrar crescimento ou piora sem as janelas seguintes.
- Não inferir causalidade a partir de médias de questionários.
- Resguardar material individual e textos dissertativos sob autenticação + RLS; não publicar registros sensíveis nos arquivos do GitHub.
- Homologar escopos dos 18 registros pendentes ou fora do núcleo antes de qualquer comparação entre grupos.
- Em futuras janelas, manter critérios, origem, versão de rubrica, regras de equivalência e proveniência para comparação longitudinal.

## 6. Implementação

Página: `admin/sintese.html`. Ela lê `stg_members` para autorizar administrador ou coordenação, busca os 25 profissionais e os 629 resultados numéricos já auditados e apenas sob demanda acessa os textos correspondentes à profissional selecionada. Não incorpora conteúdo privado na versão estática.
