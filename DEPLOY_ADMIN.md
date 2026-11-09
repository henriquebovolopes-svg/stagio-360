# Implantação da área administrativa — STAGIO 360

## Atualização operacional — 09/11/2026

O status datado de 04/11/2026 abaixo foi mantido como histórico da implantação inicial. **A situação atual é diferente:**
- Administração, Érica, Giovanna, Márcia e Patrícia possuem perfis institucionais ativos no Supabase.
- Márcia: `master` com autorização específica à Escuta dos Funcionários; Patrícia: `coordenacao` apenas para `infantil`.
- A entrada orientada por perfil é `/admin/minha-area.html`, que lê os perfis no Supabase após autenticação.
- As contas de Márcia e Patrícia estão com e-mails confirmados e senha cadastrada; nenhuma das duas realizou login registrado no momento da auditoria.
- Testes de RLS por simulação de sessão autenticada passaram. Falta validação real de login no navegador e confirmação da publicação do GitHub Pages.
- **Não compartilhar senhas ou credenciais administrativas no repositório.**


## Situação atual (04/11/2026)

- ✅ Projeto Supabase **stagio-360** criado na organização Stagio Academy (região São Paulo; plano gratuito).
- ✅ Migração SQL aplicada, seis tabelas com RLS ativo e políticas de leitura restrita.
- ✅ Auditoria Supabase sem avisos de segurança; papel `anon` não consegue ler `stg_evidence`; papel `authenticated` sem usuário autorizado recebe zero linhas.
- ✅ `admin/config.js` aponta para o projeto, usando **somente chave publishable**.
- ⏳ Contas individuais de administração e Érica ainda não criadas nem autorizadas.
- ⏳ Arquivo de respostas individuais **não importado** ao Supabase.
- ⏳ Implantação no GitHub Pages pode ainda estar em fila; o código está no repositório.

O site público continua exibindo somente indicadores agregados. A rota `/admin/` exige sessão e permissão explícita. Nenhum registro sensível foi publicado no GitHub.

**Não use o GitHub como banco de avaliações individuais, exportações Typeform ou comentários de crianças.**

## O que já existe no repositório

- `index.html` — painel institucional com indicadores agregados.
- `admin/index.html` — interface com login, perfis docentes, avaliações por critério, respostas dissertativas, estudantes por código e famílias.
- `admin/config.js` — placeholder para URL e chave pública, sem segredos.
- `supabase/migrations/20261104_stagio360_secure.sql` — tabelas e políticas RLS com negação por padrão.

## Ativar o backend em ordem segura

1. **Já concluído:** projeto Supabase em https://supabase.com/dashboard/project/imwmkftrtljdokmkwicj; banco e RLS aplicados.
2. **Já concluído:** regras e permissões testadas, sem alertas de segurança.
3. **Ação humana necessária:** em Authentication → Providers (ou configurações de Auth), restringir cadastro aberto. Em Authentication → Users, criar contas individuais convidadas (administração e coordenação); usar senhas fortes e MFA quando disponível.
4. Em `Authentication → Users`, copiar o UUID de cada conta. Autorizar apenas as pessoas desejadas no SQL Editor:

   ```sql
   insert into public.stg_members (user_id, display_name, role, active)
   values ('COLE_AQUI_O_UUID'::uuid, 'Administração', 'admin', true);
   -- Para a coordenadora: role='coordenacao', display_name='Érica'
   ```

5. **Testar RLS antes de importar dados.** Verificar: visitante anônimo não consegue ler nada; conta autenticada não incluída em `stg_members` não consegue ler dados; conta autorizada pode fazer SELECT; nenhuma dessas contas pode escrever dados. Executar os testes no ambiente do projeto com `supabase test db` ou consultas autenticadas que exercitem as políticas. O script SQL é preparado, **não foi executado nem homologado remotamente**.
6. Somente após esses testes, carregar o acervo confidencial usando o utilitário `importar_dados_restritos.py`, fornecido à parte para execução local. Ele lê o arquivo **HTML criptografado v1.6** e usa uma chave `service_role` apenas no computador do responsável. A chave `service_role` **NUNCA** deve ser enviada ao GitHub, ao navegador ou ao chat.

   Exemplo de validação local:

   ```bash
   python importar_dados_restritos.py --file "STAGIO_360_FI_M1_APROFUNDAMENTO_QUALITATIVO_RESTRITO_v1_6.html"
   ```

   Execução controlada, após definir `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` **somente no ambiente local** e senha solicitada no terminal:

   ```bash
   python importar_dados_restritos.py --file "STAGIO_360_FI_M1_APROFUNDAMENTO_QUALITATIVO_RESTRITO_v1_6.html" --apply --confirm
   ```

7. **Já concluído:** `admin/config.js` contém apenas o Project URL e a Publishable key. Nunca substituir por chave administrativa.

   São informações públicas de conexão, não privilégios administrativos. **Nunca** colocar `service_role` em `config.js`.

8. Abrir `https://henriquebovolopes-svg.github.io/stagio-360/admin/` e testar login autorizado, conta sem autorização, logout, leitura de critérios, busca e consulta das dissertativas.

## Perfis de acesso iniciais

- `admin`: leitura de dados privados do segmento e governança.
- `coordenacao`: leitura dos mesmos dados do Fundamental I para acompanhamento pedagógico. O acesso é individual; não há senha compartilhada.
- Visitante, usuário sem convite e usuário desativado: **sem permissão**.

**Não confundir a exibição nominal da coordenação com permissão de acesso:** a identidade da Érica só estará autorizada quando sua conta e seu UUID forem registrados.

## Privacidade e limites metodológicos

- A pesquisa dos alunos não indica necessariamente um professor responsável por cada resposta. Revezamentos entre turmas não autorizam atribuição indevida.
- Respostas abertas podem identificar terceiros mesmo quando o respondente usa um código pseudonimizado.
- O banco deste protótipo atende apenas ao M1/2026. M2 e a revisão definitiva das taxas de participação permanecem pendentes.
- A exportação/consulta administrativa deve ser regida por finalidade pedagógica, necessidade de acesso, período de retenção e medidas exigidas pela escola e pela LGPD.

## Fontes de segurança

- Supabase Auth: https://supabase.com/docs/guides/auth
- Supabase RLS: https://supabase.com/docs/guides/database/postgres/row-level-security

**Status:** projeto e regras de segurança criados e testados; faltam contas reais, importação dos dados privados e teste final do login autorizado. O deploy recente ainda precisava de confirmação na última consulta.
