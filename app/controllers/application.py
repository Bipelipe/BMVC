from pathlib import Path

from bottle import template

VIEWS_ROOT = Path(__file__).resolve().parents[1] / "views" / "html"


class Application:
    def foco(self):
        return template("foco.tpl", template_lookup=[str(VIEWS_ROOT)])
