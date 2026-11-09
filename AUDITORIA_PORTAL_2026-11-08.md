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
