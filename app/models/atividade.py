import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path


DIAS = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta")

ATIVIDADES_INICIAIS = (
    ("Segunda", "Classes e objetos", "Crie uma classe Livro e instancie dois livros com títulos diferentes."),
    ("Terça", "Encapsulamento", "Defina como uma conta bancária valida depósitos e saques."),
    ("Quarta", "Herança", "Crie classes Bicicleta e Carro que herdem de Veiculo."),
    ("Quinta", "Polimorfismo", "Implemente o método area() em um retângulo e em um círculo."),
    ("Sexta", "Revisão prática", "Releia os exercícios e explique a decisão de design de cada um."),
)


@dataclass(frozen=True)
class Atividade:
    id: int
    dia: str
    titulo: str
    descricao: str


class Atividades:
    def __init__(self, caminho: Path):
        self.caminho = caminho
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with closing(self._conectar()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            versao = db.execute("PRAGMA user_version").fetchone()[0]
            if versao == 0:
                db.execute("""
                    CREATE TABLE atividades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dia TEXT NOT NULL,
                        titulo TEXT NOT NULL,
                        descricao TEXT NOT NULL
                    )
                """)
                db.executemany(
                    "INSERT INTO atividades (dia, titulo, descricao) VALUES (?, ?, ?)",
                    ATIVIDADES_INICIAIS,
                )
                db.execute("PRAGMA user_version = 1")

    def _conectar(self):
        return sqlite3.connect(self.caminho)

    def listar(self):
        with closing(self._conectar()) as db:
            linhas = db.execute(
                "SELECT id, dia, titulo, descricao FROM atividades ORDER BY id"
            ).fetchall()

        atividades = [Atividade(*linha) for linha in linhas]
        return sorted(atividades, key=lambda atividade: DIAS.index(atividade.dia))

    def buscar(self, atividade_id):
        with closing(self._conectar()) as db:
            linha = db.execute(
                "SELECT id, dia, titulo, descricao FROM atividades WHERE id = ?",
                (atividade_id,),
            ).fetchone()

        return Atividade(*linha) if linha else None

    def criar(self, dia, titulo, descricao):
        with closing(self._conectar()) as db, db:
            db.execute(
                "INSERT INTO atividades (dia, titulo, descricao) VALUES (?, ?, ?)",
                (dia, titulo, descricao),
            )

    def atualizar(self, atividade_id, dia, titulo, descricao):
        with closing(self._conectar()) as db, db:
            resultado = db.execute(
                "UPDATE atividades SET dia = ?, titulo = ?, descricao = ? WHERE id = ?",
                (dia, titulo, descricao, atividade_id),
            )
            return resultado.rowcount == 1

    def excluir(self, atividade_id):
        with closing(self._conectar()) as db, db:
            resultado = db.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
            return resultado.rowcount == 1
