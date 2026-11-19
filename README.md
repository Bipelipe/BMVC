# Foco Time · BMVC I

O Foco Time reúne um plano semanal para estudantes que querem organizar a revisão da disciplina. A página apresenta cinco atividades de estudo e um cronômetro de 25 minutos.

## Executar localmente

Requer Python 3.10 ou superior. Na raiz do projeto, crie um ambiente virtual.

```sh
python -m venv .venv
```

No Linux ou macOS:

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python route.py
```

No Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe route.py
```

Abra `http://127.0.0.1:8080/foco`. A raiz do site redireciona para essa página. Para encerrar o servidor, pressione `Ctrl+C`.

## Fluxo do BMVC

```text
GET /foco
  → route.py
  → Application.foco() em app/controllers/application.py
  → app/views/html/foco.tpl
  → /static/css/foco.css e /static/js/foco.js
```

O plano de estudos fica no template. O Bottle serve a página e os arquivos estáticos, e o JavaScript controla o cronômetro no navegador.

