import argparse
import re
from getpass import getpass
from pathlib import Path

from app.models.usuario import Usuarios

BANCO = Path(__file__).resolve().parent / "instance" / "foco.sqlite3"


def main():
    parser = argparse.ArgumentParser(description="Cria um usuário local do Foco Time.")
    parser.add_argument("usuario", help="Nome usado para entrar no site")
    args = parser.parse_args()
    nome = args.usuario.strip().lower()
    if not re.fullmatch(r"[a-z0-9_.-]{3,32}", nome):
        parser.error("Use de 3 a 32 letras sem acento, números, pontos, hífens ou sublinhados.")

    senha = getpass("Senha (12 a 128 caracteres): ")
    if not 12 <= len(senha) <= 128:
        parser.error("A senha deve ter de 12 a 128 caracteres.")
    if senha != getpass("Confirme a senha: "):
        parser.error("As senhas não coincidem.")

    if not Usuarios(BANCO).criar(nome, senha):
        parser.error("Já existe um usuário com esse nome.")
    print(f"Usuário {nome} criado.")


if __name__ == "__main__":
    main()
