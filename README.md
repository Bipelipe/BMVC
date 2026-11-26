# Foco Time · BMVC III

Organize uma semana de estudos de Orientação a Objetos. Depois de entrar, você
pode cadastrar, consultar, editar e excluir atividades e usar o cronômetro de
25 minutos. Os usuários cadastrados acessam o mesmo plano semanal.

## Executar localmente

Requer Python 3.10 ou superior. Na raiz do projeto, crie um ambiente virtual.

```sh
python -m venv .venv
```

No Linux ou macOS, instale o Bottle, crie a conta e inicie o servidor.

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python criar_usuario.py estudante
.venv/bin/python route.py
```

No Windows, use estes comandos.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe criar_usuario.py estudante
.\.venv\Scripts\python.exe route.py
```

Escolha uma senha de 12 a 128 caracteres quando o terminal pedir. Crie a conta
uma vez por banco. Abra `http://127.0.0.1:8080/foco` e entre com o usuário e a
senha cadastrados. Use o botão **Sair** para encerrar a sessão.

## Fluxo do BMVC

O Bottle configura as rotas em `route.py`. O controlador `Autenticacao` verifica
a sessão antes de liberar o plano e as rotas do CRUD. A senha é armazenada
como hash com sal e as sessões expiram depois de oito horas.

O controlador `Application` entrega ao template os objetos Python do modelo
`Atividade` e valida os dados do CRUD. O SQLite salva atividades, usuários e
sessões no arquivo local `instance/foco.sqlite3`. O projeto usa o mesmo banco
da fase II, com duas tabelas adicionais para autenticação. O arquivo do banco
fica fora do Git.

## Demonstração

Em uma janela anônima, acesse `/foco` antes do login e veja o redirecionamento.
Entre com a conta de teste e demonstre o CRUD, o CSS e o cronômetro. Depois de
sair, tente abrir `/foco` novamente para confirmar o bloqueio. O vídeo do BMVC III
tem limite de dez minutos.
