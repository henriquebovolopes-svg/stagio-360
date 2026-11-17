# STAGIO 360 — Auditoria técnica de fechamento do M1 (16/11/2026)

> **Estado: M1 NÃO integralmente homologado.** Este documento público descreve somente métricas técnicas e critérios de controle. Respostas individuais, nomes completos, documentos funcionais, e-mails, tokens e registros de homologação permanecem no Supabase com RLS ou nas fontes autorizadas do Drive.

## Integridade verificada

- Fontes protegidas de alunos e famílias: 423 formulários distintos, 19.016 itens; sem colisão de `source_key`.
  - Alunos 6º–8º: 96 formulários e 7.804 itens (96 NPS válidos).
  - Alunos 9º: 41 formulários e 3.360 itens (40 NPS válidos).
  - Alunos EM: 38 formulários e 3.384 itens (36 NPS válidos).
  - Famílias: 248 formulários e 4.468 itens (236 NPS válidos).
  - Total: 408 notas NPS válidas; 15 formulários sem nota. Não transformar ausência em zero.
- Coordenação FII/EM: 297 itens de origem distintos, sendo 212 notas e 85 textos; segmentação exclusiva FII (111+46), exclusiva EM (36+14), compartilhada (65+25). Não duplicar a faixa compartilhada.
- Acervo legado 360 de origem FI: 1.400 evidências qualitativas originais e 629 notas por critério (462 AUTO de docentes que podem atuar em mais de uma etapa, 167 de coordenação FI); não interpretar todos os 462 itens como docentes exclusivamente do FI.
- Planejamento 2026: 336 registros individuais; 32 combinações professor/etapa.
- Autoavaliação Typeform_PROFS: 36 envios conciliados, 22 integrações legadas exatamente verificadas (462 itens), 8 novas respostas completas retidas em staging seguro (168 itens) e 6 respostas incompletas excluídas do cálculo, mas preservadas.

## Correções executadas no Supabase

1. Migração `stagio360_m1_quality_gate_curricular_stage_normalization_20261116`:
   - `stg_360_curricular_stage_2026` calcula a etapa curricular de 51 registros de **1º ano** que a fonte marcou como Infantil. Etapa declarada original permanece imutável; 139 demais registros classificados como Infantil são preservados.
   - `stg_360_m1_gate` expõe à administração/direção, com `security_invoker` e controle de escopo, indicadores operacionais de fechamento antes do M2.
   - `stg_360_operational_readiness` deixou de comparar status com a opção inexistente `complete`; verifica `validated`, permitido pela restrição real de `stg_360_cycles`.
2. Migração `stagio360_m1_fk_indexes_pre_m2_20261116`: índices nos 10 relacionamentos apontados pelo auditor de desempenho; diagnóstico de chaves estrangeiras sem índice não apresenta novas ocorrências.
3. Conciliação documental preservada no banco: um vínculo adicional de planejamento do Médio validado com a identidade já canônica mediante autoavaliação, disciplina e dois planos de aula independentes; nenhuma nota nem resposta pessoal foi reatribuída por aproximação.
4. Observações da auditoria documental registradas **somente no banco privado** para cinco candidaturas do Médio, incluindo nomes funcionais ampliados e divergências entre disciplina/identificador. Nenhuma revisão humana foi artificialmente atribuída.

## Controle de acesso verificado

- Teste simulado `authenticated` com identidades de direção `master`: a view do fechamento retorna os indicadores esperados.
- Teste simulado com perfil `coordenacao`: não retorna linhas do controle de fechamento.
- Papel `anon`: acesso à view do fechamento negado.
- Código do painel de Integração atualizado para ler o gate protegido e informar as diferenças entre dados de origem e associação canônica.
- O teste acima é de política SQL simulada, **não** substitui ensaio no navegador publicado com as credenciais de direção.

## Pendências documentadas após esta rodada

| Verificação | Confirmado | Pendente |
| --- | ---: | ---: |
| Vínculos de planejamento/identidade | 16 | 16 |
| Novas autoavaliações completas integradas | 0 de 8 | 8 |
| Blocos de docente nas pesquisas FII/EM homologados com identidade canônica | 0 de 38 | 38 |
| Reclassificação curricular derivada dos planos de 1º ano | 51 | 0 casos do 1º ano sem classificação derivada |

**Atenção: identificadores Typeform NÃO são a identidade canônica.** Há códigos repetidos entre origens com rótulos divergentes (por exemplo, `P058`) e variações ortográficas (`P056`), assim como docentes representados por códigos distintos em formulários diferentes. Nunca aplicar um mapeamento global de código sem prova por formulário, pergunta, turma e identidade.

As oito novas autoavaliações completas não devem ser transferidas para indicadores nominais sem evidência de nome, papel, etapa e autorização institucional. As seis incompletas não devem receber notas presumidas. As 51 aulas devem ser tratadas como turma de 1º ano do Fundamental I em relatórios curriculares, sem alterar o valor da etapa originalmente preenchida.

## Regras de importação do M2

1. Manter M1 como fotografia versionada: preservar fontes brutas, `source_file_id`, `source_row`, `module`, ano, etapa declarada e horário original.
2. Importar novos envios em staging separado, com `module='M2'` e identificadores idempotentes. Não sobrescrever registros `M1` e não lançar dados parciais nos totais homologados.
3. Comparar as fontes e a população de cada módulo antes de fazer série temporal. A pesquisa anual de colaboradores e o histórico acadêmico não se tornam `M1`/`M2` automaticamente.
4. Validar no servidor (RLS): direção `admin/master` tem visão institucional; cada coordenação consulta apenas etapa autorizada; visitantes não consultam respostas protegidas.
5. Para liberação institucional do M2, registrar por escrito as decisões de identificação pendentes, exceções metodológicas e o resultado dos testes de navegação com usuário real. Não marcar `stg_360_cycles.data_status='validated'` sem evidência de testes.
6. Reexecutar as verificações de duplicidade, contagens, médias, denominadores NPS, associação professor/turma e integridade de permissões após importação do M2.

## Limites de homologação

O portal não pode afirmar que toda resposta de aluno/família pertence a determinado professor quando a fonte não guarda essa associação de forma verificável. A disponibilidade de uma resposta confidencial para a direção **não exige** que ela possua correspondência nominal validada. O fechamento do M1 exige decisões institucionais sobre casos ambíguos; a auditoria técnica não substitui essa decisão.
