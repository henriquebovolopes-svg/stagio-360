# STAGIO 360 | Governança do PDI piloto M1

Esta versão adiciona **registro de reunião e histórico de edições** ao PDI existente.

## Etapas de trabalho

- `rascunho`: proposta editável, sem compromisso da docente ou da instituição.
- `para_revisao`: proposta com eixo, objetivo, ações, indicador e prazo de acompanhamento, pronta para ser discutida.
- `pactuacao_registrada`: registro administrativo de reunião já realizada, com participantes, devolutiva da docente, ressalvas, acordos e confirmação de que houve conversa. **Não é uma assinatura digital ou aceite independente da professora.**

O banco proíbe saltar diretamente do rascunho para a última etapa. Ao registrar uma pactuação, a versão é congelada. A tela exige uma confirmação explícita da administração antes dessa ação.

## Histórico protegido

Cada inclusão ou edição produz um instantâneo da ficha em `stg_pdi_revisions`, com versão, data e ator. A primeira ficha preexistente foi marcada como `baseline`: isso não inventa uma alteração histórica. As versões são consultáveis somente por usuários autorizados; não podem ser alteradas ou forjadas por acessos comuns.

## Limites de evidência

Apenas respostas de coordenação e autoavaliação vinculadas à própria profissional podem ser citadas na ficha. Não anexar depoimentos gerais de alunos ou famílias a indivíduos. Rubricas 1–5 e 1–4 não são diretamente comparáveis.

O piloto existente segue em **rascunho**. Testes de transição foram revertidos no banco. A administração precisa realizar a reunião de devolutiva e validar compromissos antes de registrar a pactuação.

## Testes mínimos
- Administrador salva e revisa, deixando rastros de auditoria.
- Coordenação consulta, mas não edita.
- Acesso anônimo ou conta sem autorização não lê.
- Usuário autenticado não consegue inserir ou alterar histórico manualmente.
- Registro de pactuação sem reunião e sem etapa de revisão é negado.
