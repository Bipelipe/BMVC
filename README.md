# Foco Time · BMVC IV

O Foco Time reúne um plano semanal de Orientação a Objetos e um cronômetro de
25 minutos. Usuários autenticados podem cadastrar, consultar, editar e excluir
atividades do mesmo plano. Uma mudança aparece nas janelas conectadas sem
recarregar a página.

## Executar localmente

Requer Python 3.10 ou superior. Na raiz do projeto, crie um ambiente virtual.

```sh
python -m venv .venv
```

No Linux ou macOS, use os comandos abaixo.

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python criar_usuario.py estudante
.venv/bin/python criar_usuario.py observador
.venv/bin/python route.py
```

No Windows, use estes comandos.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe criar_usuario.py estudante
.\.venv\Scripts\python.exe criar_usuario.py observador
.\.venv\Scripts\python.exe route.py
```

Crie cada conta uma vez por banco e escolha uma senha de 12 a 128 caracteres
quando o terminal pedir. A segunda conta é útil para demonstrar a
sincronização em outra janela. O banco SQLite fica em `instance/foco.sqlite3`.
As contas e atividades da fase III podem ser usadas no mesmo banco.

Abra `http://127.0.0.1:8080/foco` em uma janela normal e em uma janela anônima
e entre nas duas. Cadastre, edite e exclua uma atividade na primeira janela
e observe a lista mudar na segunda. Pressione `Ctrl+C` para parar o servidor.

## Como funciona

- O Uvicorn serve HTTP e WebSocket na mesma porta. O a2wsgi encaminha as
  requisições HTTP ao Bottle.
- O servidor valida a origem e a sessão ao abrir o WebSocket
  `/ws/atividades`. A sessão também é verificada enquanto a conexão está ativa.
- Após salvar uma alteração no SQLite, o controlador envia um aviso às
  conexões válidas. O JavaScript consulta `/atividades/lista` e troca apenas
  a lista do plano, mantendo a contagem do cronômetro.
- O servidor roda com um processo, que mantém as conexões WebSocket em memória.
  Quando o navegador reconecta, ele busca a lista atual para recuperar
  alterações feitas durante a interrupção.

## Demonstração

Mostre o acesso restrito antes do login e o CRUD em uma janela autenticada.
Mantenha a segunda janela visível para mostrar as alterações chegando sem
recarregar a página. Demonstre os controles do cronômetro, o layout responsivo
e o bloqueio do plano após sair. O vídeo tem limite de 15 minutos.