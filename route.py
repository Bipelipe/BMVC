from pathlib import Path

from bottle import Bottle, redirect, static_file

from app.controllers.application import Application
from app.models.atividade import Atividades

BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = BASE_DIR / "app" / "static"

app = Bottle()
controller = Application(Atividades(BASE_DIR / "instance" / "foco.sqlite3"))


@app.get("/")
def index():
    return redirect("/foco")


@app.get("/foco")
def foco():
    return controller.foco()


app.get("/atividades/nova", callback=controller.nova)
app.post("/atividades", callback=controller.criar)
app.get("/atividades/<atividade_id:int>/editar", callback=controller.editar)
app.post("/atividades/<atividade_id:int>/editar", callback=controller.atualizar)
app.post("/atividades/<atividade_id:int>/excluir", callback=controller.excluir)


@app.get("/static/<filepath:path>")
def assets(filepath):
    return static_file(filepath, root=str(STATIC_ROOT))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
