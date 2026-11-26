import hmac
import secrets
from functools import wraps
from pathlib import Path

from bottle import abort, redirect, request, response, template

from app.models.usuario import DURACAO_SESSAO

VIEWS_ROOT = Path(__file__).resolve().parents[1] / "views" / "html"
COOKIE_SESSAO = "foco_sessao"
COOKIE_CSRF = "foco_csrf"


class Autenticacao:
    def __init__(self, usuarios):
        self.usuarios = usuarios

    def _cookie(self, nome, valor, duracao):
        response.set_cookie(
            nome, valor, max_age=duracao, path="/", httponly=True,
            secure=request.urlparts.scheme == "https", samesite="Strict",
        )

    def _novo_csrf(self):
        token = secrets.token_urlsafe(32)
        self._cookie(COOKIE_CSRF, token, DURACAO_SESSAO)
        return token

    def _csrf(self):
        return request.get_cookie(COOKIE_CSRF) or self._novo_csrf()

    def _validar_csrf(self):
        esperado = request.get_cookie(COOKIE_CSRF, "").encode("utf-8")
        enviado = request.forms.get("csrf", "").encode("utf-8")
        if not esperado or not hmac.compare_digest(esperado, enviado):
            abort(403, "Formulário expirado. Recarregue a página e tente novamente.")

    def _formulario(self, usuario="", erro=""):
        return template(
            "login.tpl", template_lookup=[str(VIEWS_ROOT)],
            usuario=usuario, erro=erro, csrf=self._csrf(),
        )

    def login(self):
        response.set_header("Cache-Control", "no-store")
        token = request.get_cookie(COOKIE_SESSAO)
        if self.usuarios.usuario_da_sessao(token):
            return redirect("/foco")

        if request.method == "GET":
            return self._formulario()

        self._validar_csrf()
        usuario = request.forms.getunicode("usuario", "").strip().lower()
        senha = request.forms.getunicode("senha", "")
        if len(usuario) > 32 or len(senha) > 128 or not self.usuarios.autenticar(usuario, senha):
            response.status = 401
            return self._formulario(usuario, "Usuário ou senha inválidos.")

        self.usuarios.encerrar_sessao(token)
        self._cookie(COOKIE_SESSAO, self.usuarios.abrir_sessao(usuario), DURACAO_SESSAO)
        self._novo_csrf()
        return redirect("/foco")

    def proteger(self, acao):
        @wraps(acao)
        def protegida(*args, **kwargs):
            response.set_header("Cache-Control", "no-store")
            usuario = self.usuarios.usuario_da_sessao(request.get_cookie(COOKIE_SESSAO))
            if usuario is None:
                return redirect("/login")

            if request.method == "POST":
                self._validar_csrf()

            request.environ["foco.contexto"] = {"usuario": usuario, "csrf": self._csrf()}
            return acao(*args, **kwargs)

        return protegida

    def sair(self):
        self.usuarios.encerrar_sessao(request.get_cookie(COOKIE_SESSAO))
        response.delete_cookie(COOKIE_SESSAO, path="/")
        response.delete_cookie(COOKIE_CSRF, path="/")
        return redirect("/login")
