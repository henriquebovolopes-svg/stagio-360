# STAGIO 360 — Importação do acervo protegido M1/2026

## Pré-requisitos confirmados

- Duas contas ativas em `stg_members`: um administrador e uma coordenadora.
- Tabelas no Supabase com RLS.
- Importação limitada ao perfil `admin`, inclusive no banco.
- Conta `coordenacao` pode consultar, mas não inserir nem editar.
- Nenhum registro individual nos arquivos públicos do GitHub.

## Procedimento para o administrador

1. Entre em https://henriquebovolopes-svg.github.io/stagio-360/admin/ com o acesso autorizado.
2. Escolha **Importar base M1 com segurança** ou abra diretamente https://henriquebovolopes-svg.github.io/stagio-360/admin/import.html
3. Selecione o arquivo original **STAGIO_360_FI_M1_APROFUNDAMENTO_QUALITATIVO_RESTRITO_v1_6.html** (extraído do ZIP, não o ZIP).
4. Digite a senha de abertura do HTML criptografado.
5. Clique em **Verificar arquivo sem enviar dados**; a senha é utilizada somente no navegador.
6. Confira o total esperado: 25 profissionais, 629 critérios numéricos, 1.400 respostas dissertativas, 159 registros de alunos, 127 famílias.
7. Clique em **Confirmar importação segura** e mantenha a aba aberta até o aviso de conclusão.
8. Volte para /admin/ e confira os perfis, respostas e busca. A coordenadora poderá entrar com sua própria conta.

## Proteções e verificações técnicas

- Dados descriptografados com AES-GCM apenas na memória do navegador do administrador, por Web Crypto.
- Transmissão das linhas via HTTPS diretamente ao Supabase após confirmação.
- Sem chaves de serviço ou senhas no GitHub ou no browser persistente.
- IDs gerados de forma determinística para permitir reexecução em caso de interrupção.
- Segurança testada: inserção de administrador autorizada; inserção de coordenação recusada pela RLS; leitura anônima recusada.
- O total de 2.340 linhas considera os cinco conjuntos de dados. A função administrativa precisa estar em rede durante o upload.
- Há um aviso de segurança complementar no projeto sobre proteção contra senhas vazadas, a ser habilitada em Auth > configurações de segurança.

**Não anexar o HTML criptografado ou seu ZIP ao repositório GitHub.**

**Nota metodológica:** as respostas gerais dos alunos não se convertem em nota individual de professor; M2 e auditoria de participação permanecem pendentes.
