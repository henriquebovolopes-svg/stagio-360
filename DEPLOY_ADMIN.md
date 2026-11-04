# Implantação da área administrativa — STAGIO 360

## Situação atual

O site público em GitHub Pages funciona com indicadores agregados. A rota `/admin/` está publicada, mas **fica bloqueada até a configuração do backend privado**. Nenhum registro sensível está no repositório.

**Não use o GitHub como banco de avaliações individuais, exportações Typeform ou comentários de crianças.**

## O que já existe no repositório

- `index.html` — painel institucional com indicadores agregados.
- `admin/index.html` — interface com login, perfis docentes, avaliações por critério, respostas dissertativas, estudantes por código e famílias.
- `admin/config.js` — placeholder para URL e chave pública, sem segredos.
- `supabase/migrations/20261104_stagio360_secure.sql` — tabelas e políticas RLS com negação por padrão.

## Ativar o backend em ordem segura

1. Criar um projeto **privado** em https://supabase.com/dashboard, com credenciais sob controle do Colégio e responsável definido pela proteção de dados.
2. No **SQL Editor**, executar a migração em `supabase/migrations/20261104_stagio360_secure.sql`.
3. Em Authentication, **desabilitar cadastro aberto ao público**. Criar apenas contas individuais convidadas (administração e coordenação). Usar senha forte e, quando possível, MFA.
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

7. Em `Project Settings → API Keys`, obter **Project URL** e **Publishable key** (ou legacy anon key, quando aplicável). Após a homologação das políticas, preencher apenas esses dois valores em `admin/config.js`:

   ```js
   window.STAGIO_AUTH = {
     url: "https://SEU-PROJETO.supabase.co",
     publishableKey: "SUA-CHAVE-PUBLICAVEL"
   };
   ```

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

**Status:** código e política disponíveis; criação do projeto, implantação SQL, homologação da segurança, importação e contas reais **pendentes**.
