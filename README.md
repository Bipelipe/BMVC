# Foco Time · BMVC II

O Foco Time permite organizar uma semana de estudos de Orientação a Objetos.
Você pode cadastrar, consultar, editar e excluir atividades do plano semanal.
A página também tem um cronômetro de 25 minutos para acompanhar uma sessão de foco.

## Executar localmente

Requer Python 3.10 ou superior. Na raiz do projeto, crie um ambiente virtual.

```sh
python -m venv .venv
```

No Linux ou macOS, instale a dependência e inicie o servidor.

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python route.py
```

No Windows, use estes comandos.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe route.py
```

Abra `http://127.0.0.1:8080/foco`. Para encerrar o servidor, pressione `Ctrl+C`.

O SQLite vem com o Python. Na primeira execução, o servidor cria
`instance/foco.sqlite3` e cadastra cinco atividades iniciais. As mudanças
continuam salvas após reiniciar o servidor. O banco local fica fora do Git.

## Fluxo do BMVC

O Bottle recebe as requisições em `route.py`. O controlador, em
`app/controllers/application.py`, valida os dados dos formulários e chama
`Atividades` para consultar ou alterar o banco. As consultas retornam objetos
Python do modelo `Atividade`, definido em `app/models/atividade.py`.
Os templates em `app/views/html/` exibem o plano e os formulários e carregam
o CSS e o JavaScript servidos em `/static/`.

| Método | Rota | Ação |
|---|---|---|
| GET | `/foco` | Listar as atividades |
| GET | `/atividades/nova` | Abrir o formulário de cadastro |
| POST | `/atividades` | Cadastrar a atividade |
| GET | `/atividades/<id>/editar` | Abrir o formulário com os dados atuais |
| POST | `/atividades/<id>/editar` | Salvar as alterações |
| POST | `/atividades/<id>/excluir` | Excluir a atividade |

## Demonstração

Cadastre uma atividade, confirme que ela aparece no plano semanal, edite seus
dados e depois exclua a atividade de teste. Mostre a formatação das páginas e
use o cronômetro para demonstrar o JavaScript. O vídeo do BMVC II tem limite
de seis minutos.
