from pathlib import Path

from bottle import Bottle, redirect, static_file

from app.controllers.application import Application

STATIC_ROOT = Path(__file__).resolve().parent / "app" / "static"

app = Bottle()
controller = Application()


@app.get("/")
def index():
    return redirect("/foco")


@app.get("/foco")
def foco():
    return controller.foco()


@app.get("/static/<filepath:path>")
def assets(filepath):
    return static_file(filepath, root=str(STATIC_ROOT))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
