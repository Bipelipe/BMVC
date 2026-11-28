from pathlib import Path

import uvicorn
from bottle import Bottle, redirect, static_file

from app.controllers.application import Application
from app.controllers.autenticacao import Autenticacao
from app.models.atividade import Atividades
from app.models.usuario import Usuarios
from app.tempo_real import TempoReal

BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = BASE_DIR / "app" / "static"
BANCO = BASE_DIR / "instance" / "foco.sqlite3"

app = Bottle()
usuarios = Usuarios(BANCO)
tempo_real = TempoReal(app, usuarios)
controller = Application(Atividades(BANCO), tempo_real.avisar)
auth = Autenticacao(usuarios)


@app.get("/")
def index():
    return redirect("/foco")


app.get("/login", callback=auth.login)
app.post("/login", callback=auth.login)
app.post("/sair", callback=auth.proteger(auth.sair))

app.get("/foco", callback=auth.proteger(controller.foco))
app.get("/atividades/lista", callback=auth.proteger(controller.lista))
app.get("/atividades/nova", callback=auth.proteger(controller.nova))
app.post("/atividades", callback=auth.proteger(controller.criar))
app.get("/atividades/<atividade_id:int>/editar", callback=auth.proteger(controller.editar))
app.post("/atividades/<atividade_id:int>/editar", callback=auth.proteger(controller.atualizar))
app.post("/atividades/<atividade_id:int>/excluir", callback=auth.proteger(controller.excluir))


@app.get("/static/<filepath:path>")
def assets(filepath):
    return static_file(filepath, root=str(STATIC_ROOT))


if __name__ == "__main__":
    uvicorn.run(tempo_real, host="127.0.0.1", port=8080, ws_max_size=4096, workers=1)