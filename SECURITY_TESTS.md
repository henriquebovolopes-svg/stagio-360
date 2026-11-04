# Testes de autorização obrigatórios — STAGIO 360

**Este checklist deve ser executado no Supabase real antes de importar qualquer resposta sensível.** O arquivo de migração foi analisado, mas sem um projeto conectado os testes de RLS ainda NÃO foram realizados.

| Situação | Resultado exigido |
|---|---|
| Visitante sem sessão lê `stg_students` | Nenhum registro; SELECT bloqueado |
| Visitante sem sessão lê `stg_evidence` | Nenhum registro; SELECT bloqueado |
| Conta autenticada sem registro em `stg_members` | Nenhum registro sensível |
| Conta em `stg_members` com `active=false` | Nenhum registro sensível |
| Conta com `role=admin` e `active=true` | Apenas SELECT permitido |
| Conta com `role=coordenacao` e `active=true` | Apenas SELECT permitido |
| Tentativa de INSERT/UPDATE/DELETE no navegador | Negada para todos os usuários do cliente |
| Tentativa de alterar `stg_members.role` pelo próprio usuário | Negada |
| Tentativa de acessar a URL sem login | Nenhum texto pessoal, nomes de professoras ou estudantes na resposta HTML |
| Logout e recarregamento da página | Dados protegidos não são retornados sem nova autorização |
| Desativação de conta no banco + nova requisição | Dados deixam de ser retornados |
| Conta convidada da Érica | Autorizada somente após inclusão manual de seu UUID |
| Conta com inscrição pública (se houver) | Não consegue acesso; desabilitar cadastro aberto |

Verifique também que `service_role` não aparece em nenhum arquivo estático, log público, commit ou ferramenta de análise do navegador. Teste com contas reais distintas e ambiente sem dados antes de importar os 1.400 textos abertos. Para testes automatizados, siga a documentação de pgTAP/RLS do Supabase: https://supabase.com/docs/guides/database/postgres/row-level-security

Atenção: políticas existentes podem mudar entre versões do banco; testes devem ser repetidos após qualquer migração de segurança.
