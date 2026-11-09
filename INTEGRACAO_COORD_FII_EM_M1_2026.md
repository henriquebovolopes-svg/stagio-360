# STAGIO 360 — Conciliação da rubrica de coordenação FII/EM (M1/2026)
**Data:** 09/11/2026
**Estado:** camada detalhada importada e reconciliada; vínculo com identidades canônicas ainda não homologado.

## Fontes conferidas
- Planilha institucional original privada `🧠 ARQUITETURA DO SISTEMA.xlsx`, abas `RAW_COORD_FII_EM`, `CONFIG_COORD_FII_EM`, `LONGA_COORD_FII_EM`, `ANALITICA_COORD_FII_EM` e `AUDITORIA_COORD_FII_EM`.
- Fonte Typeform original privada `Typeform_COORD_FIIEM.xlsx`. O arquivo contém um envio, com 22 blocos de avaliação por professor e itens de autoavaliação institucional da coordenação em colunas adicionais. A configuração possui 21 docentes ativos; 19 possuem respostas aproveitáveis.
- Os blocos usam nomes abreviados e identificadores de origem `P###`; **não são UUIDs de identidade docente homologada**.

## Reconciliação exata
| Atuação declarada na configuração do formulário | Notas 1–5 | Comentários | Total | Docentes com respostas |
|---|---:|---:|---:|---:|
| Fundamental II exclusivo | 111 | 46 | 157 | 10 |
| Ensino Médio exclusivo | 36 | 14 | 50 | 3 |
| Fundamental II + Médio, compartilhado | 65 | 25 | 90 | 6 |
| **Total** | **212** | **85** | **297** | **19** |

- Os **212 itens numéricos e 85 qualitativos** da aba `LONGA_COORD_FII_EM` foram reproduzidos em `public.stg_360_coord_fiiem_items`, sem valor faltante, com chave única de fonte/bloco/questão. A contagem de 297 itens bate com a aba `AUDITORIA_COORD_FII_EM`; identificadores distintos 297/297.
- As **65 notas e 25 comentários compartilhados** ficam classificados como `declared_stage='shared'`. Não são divididos, duplicados ou atribuídos arbitrariamente entre Fundamental II e Ensino Médio.
- As 111 notas exclusivas FII e 36 exclusivas Médio já estavam agregadas em `stg_stage_rubric_aggregates`; a importação **não alterou** essa tabela. Confrontação por eixo: 8/8 contagens iguais e 8/8 médias iguais dentro do arredondamento.
- O número de `21` da CONFIG é a quantidade de ativos, não a quantidade de professores com avaliações preenchidas (`19`). Não criar notas zero para os demais.
- Os itens da autoavaliação da coordenação e perguntas institucionais no final do formulário **não fazem parte das 297 linhas da rubrica docente** e exigem trilha própria. Não declarar a fonte integralmente concluída em todas as perspectivas.

## Segurança e acesso
- Migração versionada em `supabase/migrations/20261109_stagio360_coord_fiiem_detail_secure.sql`.
- A tabela confidencial `public.stg_360_coord_fiiem_items` tem RLS habilitada; `anon` sem permissão SELECT; `authenticated` só com perfil ativo `admin` ou `master`; sem INSERT/UPDATE/DELETE do frontend.
- A visão agregada `public.stg_360_coord_fiiem_coverage` é `security_invoker`, preservando as mesmas permissões.
- Testes de sessão simulada: Márcia/Direção Master viu 297 itens; Patrícia/EI viu 0; `anon` recebeu erro de permissão (esperado).
- O código estático e o relatório público não incluem os textos das avaliações, nomes completos, e-mails pessoais, tokens do Typeform, senhas ou UUIDs.
- As leituras das respostas devem usar apenas a UI protegida e o Supabase, não o GitHub Pages em modo público.

## Interface para consulta
- `/admin/coord-fii-em.html`: acesso com login admin/master, leitura de 297 linhas do Supabase e filtros por etapa declarada, eixo, tipo e docente na fonte. Comentários abrem sob demanda.
- `/admin/minha-area.html`: novo atalho em Ferramentas da direção e administração.
- `/admin/integracao.html`: atalho da área institucional, acessível somente após autenticação.
- A interface não soma os 90 itens compartilhados aos 157 exclusivos de FII nem aos 50 exclusivos de EM; apresenta as três populações separadas.

## Pendências para integração 360 plena
1. Homologar a correspondência entre `P###` de origem, cadastro institucional do professor e identidades da avaliação FI, **sem aceitar coincidência de prenome como prova**.
2. Definir metodologia para contextualizar docentes que lecionam tanto no Fundamental II quanto no Médio (não atribuir automaticamente uma resposta a ambos os segmentos).
3. Incluir a autoavaliação da coordenação e questões institucionais adicionais da mesma fonte em uma trilha própria.
4. Conciliar alunos/famílias qualitativos destas etapas e respectivos denominadores com as bases originais, sem romper anonimização.
5. Importar M2/M3 apenas quando houver documentação real de coleta e fontes adequadas.
6. Validar acesso e legibilidade com login real de Henrique, Giovanna ou Márcia no navegador; SQL/RLS e CI não substituem essa homologação.

**Importante:** Esta etapa resolve a lacuna de registro e consulta da rubrica detalhada FII/EM, não a totalidade das pendências pedagógicas do STAGIO 360.
