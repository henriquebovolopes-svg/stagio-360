# STAGIO 360 — Auditoria técnica e pedagógica da expansão (08/11/2026)
## Publicação
- Página inicial (`/index.html`) substituída por portal institucional com Governança, Avaliação 360, Séries históricas, Gestão e acessos, Fontes e método.
- Protótipo do Fundamental I integralmente preservado em `/fundamental-1/index.html`; área restrita preexistente em `/admin/index.html`.
- Logotipo institucional disponível em `/assets/stagio360-logo-oficial.svg`.
- Série consolidada NPS 2023–2025 em `/assets/stagio360-historico.json`; quadros e gráficos por etapa no portal.

## NPS (conciliação)
| Segmento | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Colégio Stagio | +48,1 (n=308) | +54,6 (n=240) | +62,8 (n=258) |
| Infantil e 1º | +55,6 (n=63) | +56,3 (n=71) | +82,1 (n=56) |
| Fundamental I | +42,7 (n=110) | +42,3 (n=78) | +61,3 (n=106) |
| Fundamental II | +34,9 (n=126) | +54,3 (n=94) | +54,9 (n=113) |
| Ensino Médio | +69,1 (n=55) | +68,8 (n=32) | +60,7 (n=28) |

Fórmula: NPS = 100 × (promotores − detratores) / respondentes. Validação automatizada de soma das classes e percentuais antes da gravação. Fontes: `2024 - Resultado da Pesquisa de Satisfação NPS - Stagio 2024.xlsx`, aba Comparativo 23-24; `2025 - Resultado da Pesquisa de Satisfação NPS - Stagio 2025.xlsx`, abas Painel e Comparativo 23 a 25.

### Ressalvas
- 2025: linha do Fundamental I no comparativo 23–25 está rotulada “EFAI - 2024”, embora seja a linha do ciclo 2025 (217 contatos, 106 respondentes). Precisa correção na planilha fonte.
- Valores de 2023 arredondados na origem; aqui recalculados pelas contagens.
- O total institucional não pode ser reconstruído somando universos de segmentos, pois as classificações por ciclo podem se sobrepor e variar entre períodos.
- NPS 2026 do Fundamental I (+72,7; n=88) NÃO é diretamente comparável ao total institucional 2025 (+62,8; n=258).
- Dados históricos de famílias ≠ avaliações 360 de professores, estudantes e coordenadores.

## Proteção
- Tabelas existentes em Supabase confirmadas com RLS habilitada.
- Corrigida função `private.stg_authorized()`: consulta de dados preexistentes do Fundamental I exige administração ou coordenação explicitamente autorizada à etapa.
- Criadas `public.stg_scope_access` e `private.stg_scope_authorized(stage)`; mantida autorização do perfil da atual coordenação do Fundamental I.
- Não criadas contas nominais para Giovanna e Márcia sem endereço de acesso e confirmação de vínculo; não há senhas em código-fonte.
- Auditor Supabase reportou somente aviso de proteção contra senhas vazadas desabilitada (configuração do serviço, não do aplicativo). Recomenda-se ativar no console Supabase.

## Testes executados
- Arquivos GitHub: leitura pós-commit do portal, rota FI, área admin, assets e JSON.
- JavaScript: parse sintático de scripts nas três páginas, sem erros.
- Navegação: verificação estática dos IDs de cada área e dos caminhos relativos.
- URLs locais da área administrativa: arquivos de destino confirmados no repositório.
- Ausência de chaves secretas no HTML das três páginas.
- Banco: testes de RLS e consulta sem autenticação retorna falso em `stg_scope_authorized`.
- Não foi possível confirmar abertura do endereço público em browser externo nem teste ponta a ponta do login: ambiente de consulta externa não alcançou GitHub Pages. Não declarar homologação de deploy final.

## Pendências para conclusão plena
1. Importar dados 2026 de Fundamental II, Ensino Médio e Infantil conforme fontes oficiais do ano, após auditoria dos arquivos e homologação de rubricas.
2. Criar contas individuais reais para Giovanna (Fundamental II e Médio) e Márcia (direção geral), associadas às identidades corretas no Auth; testar que cada uma acessa apenas as etapas permitidas.
3. Testar responsividade, publicação GitHub Pages e autenticação em navegador real; verificar informação editorial, atribuição e menores n.
4. Configurar gestão de mudanças e revisão a cada janela de avaliação (março, junho, novembro).

Nota: o portal foi atualizado com evidências verificadas, mas o objetivo de ter a plataforma integralmente pronta ainda depende das fontes 2026 e do provisionamento de acessos.

## Ampliação após a primeira auditoria — dados de 2026
- Fonte principal: planilha particular **Arquitetura do Sistema** e relatórios executivos de famílias, EFAF e Infantil. Dados pessoais e transcrições integrais **não** foram enviados ao repositório público.
- NPS institucional 2026: 408 respostas = 236 famílias + 172 alunos; 219 promotores, 134 neutros, 55 detratores => **+40,20**.
- Famílias 2026: 236; 159 promotores, 59 neutros, 18 detratores => **+59,75**.
- Alunos 2026: 172; 60 promotores, 75 neutros, 37 detratores => **+13,37**.
- Educação Infantil (famílias) 36 respostas, NPS **+75,00**; médias de itens com até 42 respostas, não confundir denominadores.
- Fundamental I (famílias no recorte NPS) 88 respostas, NPS **+72,73**; são diferentes dos 127 registros de famílias do painel FI.
- Fundamental II (famílias) 93 respostas, NPS **+38,71**; 6º–8º (alunos) 94 respostas, NPS **+22,34**; 9º (alunos) 40, NPS **−5,00**.
- Ensino Médio (famílias) 19 respostas, NPS **+73,68**; alunos 38 respostas, NPS **+10,53**. A amostra familiar é pequena.
- Há um registro de família marcado como FII mas com série “Infantil II”, registrado como pendência de categorização na própria fonte.
- Arquivo agregado publicado: `assets/stagio360-2026-agregados.json`; painéis por etapa populados com contagens e médias NPS de 2026. Os recortes do NPS incluem populações diferentes dos registros individuais históricos e do banco de FI.
- A série histórica 2023–2025 é principalmente familiar. **O NPS geral 2026 mistura famílias e alunos**, portanto não deve ser calculada variação anual direta com o NPS histórico geral.

## Dados docentes exclusivos, autenticação e escopo
- Projeto Supabase: stagio-360; todas as tabelas de dados de avaliação com RLS habilitada.
- Migração `stagio360_stage_scoped_access_20261108` cria matriz de autorização de etapas para coordenações, preserva acesso atual da coordenação de FI e permite à administração acesso geral.
- Migração `stagio360_stage_rubric_secure_20261108` cria `public.stg_stage_rubric_aggregates` com **somente médias agregadas dos quatro eixos** da coordenação e políticas SELECT por etapa no servidor.
- FII: Planejamento 3,900 (30 respostas), Condução 3,852 (27), Cultura 4,333 (27), Formação 4,222 (27). Registro apenas de profissionais exclusivamente classificados FII.
- EM: Planejamento 3,889 (9), Condução 2,778 (9), Cultura 3,778 (9), Formação 4,111 (9). Registro apenas de profissionais exclusivamente classificados EM.
- Profissionais com atuação simultânea em FII e EM foram excluídos dos grupos exclusivos para evitar duplicação de média; sem inferência para subgrupos com identificação.
- `/admin/governanca.html` é nova página autenticada com consulta RLS; senha não aparece em código. `/admin/` original FI preservado.
- Giovanna e Márcia ainda necessitam **identidades individuais verificadas e convites/credenciais pessoais** antes de receber acesso. NÃO atribuir permissões por nome textual sem vinculação a autenticação real.
- Auditor Supabase segurança: aviso de "Leaked Password Protection Disabled" exige ativação na configuração de Auth. Documentação: https://supabase.com/docs/guides/auth/password-security#password-strength-and-leaked-password-protection.

## Auditoria pós-expansão
- Interface revisada para substituir etiquetas “fontes em validação” incorretas nas etapas cujo NPS 2026 já está publicado.
- Revisão estática do código, integridade de JSON e existência dos arquivos GitHub. Ainda falta teste E2E do ambiente publicado, inclusive de sessões reais de cada perfil.
- **Status correto: entrega de portal funcional em código, com relatórios NPS e rubricas agregadas; plataforma de avaliação individual 360 multietapa ainda NÃO integralmente homologada.** Não divulgar o portal como pronto para acesso a informações individuais de todas as etapas.

## Continuação 09/11/2026 — roteamento, CI e publicação
- Ajustado o portal para URLs diretas `#etapa/infantil`, `#etapa/fundamental2`, `#etapa/medio`, com suporte a voltar/avançar no navegador.
- Adicionado `scripts/audit_site.py` para detectar referências internas inexistentes, IDs HTML duplicados, padrões de segredos, NPS inconsistentes e ausência do logo oficial.
- Adicionado `.github/workflows/audit.yml` para executar auditoria e validação de sintaxe JavaScript a cada push/PR em `main`.
- Adicionado `.github/workflows/deploy-pages.yml` para validar e publicar o portal via GitHub Pages.
- Confirmados no repositório os arquivos de todas as rotas principais, logo e configuração do cliente; os nove HTML inspecionados não tinham IDs duplicados.
- No Supabase, perfil da coordenação atual aparece com autorização **apenas Fundamental I**. Rubricas FII e Médio seguem restritas. O administrador tem privilégio institucional previsto pela política.
- **Verificação externa ainda pendente:** o ambiente de consulta web não conseguiu abrir os endereços do GitHub Pages e a integração GitHub disponível não retornou o estado efetivo do Pages. O workflow pode precisar de `Settings > Pages > Build and deployment > GitHub Actions` para entrar em operação. Não alegar sucesso de deploy sem execução confirmada.

## 09/11/2026 — continuidade e controle de qualidade
- Revisadas as nove páginas HTML do portal, Fundamental I e administração: nenhum `id` duplicado nos arquivos inspecionados.
- Confirmada a existência dos arquivos usados pelas rotas internas (logotipo, CSS, scripts de configuração e páginas protegidas).
- Correção do histórico de navegação: seções e etapas passam a ter links diretos (`#etapa/...`) com suporte ao botão Voltar do navegador.
- Corrigida a área `admin/governanca.html` para obter as etapas concedidas em `stg_scope_access`, desabilitar opções não autorizadas na interface e manter fiscalização definitiva no RLS do Supabase. Não cria permissões automaticamente.
- Workflow de validação e publicação configurados no GitHub, mas **execução/estado do Pages não confirmados**: o provedor conectado retorna código e commits, não lista os resultados de execução de workflows de push.
- O repositório é público: nenhuma resposta aberta identificável, senha individual ou chave de serviço deve ser publicada.
- Conclusão correta: navegação, código, indicadores e proteção por etapa continuam avançando; o fechamento da versão oficial depende de login real, validação do Pages e carga integral das avaliações dos demais segmentos.

## 09/11/2026 — reforço de entrega e QA
- Adicionada conciliação cruzada ao `scripts/audit_site.py`: valores de famílias + alunos devem igualar o total institucional, e as quatro etapas das famílias e os três subgrupos de alunos devem coincidir com os totais e com as classes NPS.
- Tabela indicativa de NPS de **famílias** 2023–2026 implantada no painel histórico para instituição, Fundamental II e Ensino Médio. Infantil e Fundamental I excluídos desse comparativo conjunto por divergência de abrangência das séries.
- Pipeline do GitHub Pages agora empacota somente `index.html`, `assets/`, `admin/`, `fundamental-1/` em `_site/`, evitando publicar scripts e arquivos internos de auditoria como artefato do Pages.
- Após o deploy, o workflow deverá testar HTTP das rotas inicial, Fundamental I e governança restrita com `curl`. Sua efetiva execução precisa ser conferida em GitHub Actions.
- **Atenção:** a execução do workflow não foi observada e o site ao vivo não pôde ser alcançado pelos acessos externos disponíveis nesta sessão. Implementação do teste automatizado não é confirmação de sucesso.
