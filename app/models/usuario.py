import hashlib
import hmac
import secrets
import sqlite3
import time
from contextlib import closing


DURACAO_SESSAO = 8 * 60 * 60


def _hash_senha(senha, sal):
    return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, 600_000)


def _hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class Usuarios:
    def __init__(self, caminho):
        self.caminho = caminho
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._conectar()) as db, db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    nome TEXT PRIMARY KEY,
                    sal BLOB NOT NULL,
                    senha_hash BLOB NOT NULL
                )
            """)
            db.execute("""
                CREATE TABLE IF NOT EXISTS sessoes (
                    token_hash TEXT PRIMARY KEY,
                    usuario TEXT NOT NULL,
                    expira_em INTEGER NOT NULL
                )
            """)

    def _conectar(self):
        return sqlite3.connect(self.caminho)

    def criar(self, nome, senha):
        sal = secrets.token_bytes(16)
        senha_hash = _hash_senha(senha, sal)
        with closing(self._conectar()) as db, db:
            resultado = db.execute(
                "INSERT INTO usuarios (nome, sal, senha_hash) VALUES (?, ?, ?) "
                "ON CONFLICT (nome) DO NOTHING",
                (nome, sal, senha_hash),
            )
            return resultado.rowcount == 1

    def autenticar(self, nome, senha):
        with closing(self._conectar()) as db:
            linha = db.execute(
                "SELECT sal, senha_hash FROM usuarios WHERE nome = ?", (nome,)
            ).fetchone()

        sal, esperado = linha if linha else (bytes(16), bytes(32))
        confere = hmac.compare_digest(_hash_senha(senha, sal), esperado)
        return linha is not None and confere

    def abrir_sessao(self, nome):
        token = secrets.token_urlsafe(32)
        agora = int(time.time())
        with closing(self._conectar()) as db, db:
            db.execute("DELETE FROM sessoes WHERE expira_em <= ?", (agora,))
            db.execute(
                "INSERT INTO sessoes (token_hash, usuario, expira_em) VALUES (?, ?, ?)",
                (_hash_token(token), nome, agora + DURACAO_SESSAO),
            )
        return token

    def usuario_da_sessao(self, token):
        if not token:
            return None

        with closing(self._conectar()) as db:
            linha = db.execute(
                "SELECT usuario FROM sessoes WHERE token_hash = ? AND expira_em > ?",
                (_hash_token(token), int(time.time())),
            ).fetchone()
        return linha[0] if linha else None

    def encerrar_sessao(self, token):
        if token:
            with closing(self._conectar()) as db, db:
                db.execute("DELETE FROM sessoes WHERE token_hash = ?", (_hash_token(token),))