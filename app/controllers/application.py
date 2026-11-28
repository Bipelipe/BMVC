from pathlib import Path

from bottle import abort, redirect, request, response, template

from app.models.atividade import DIAS, Atividades

VIEWS_ROOT = Path(__file__).resolve().parents[1] / "views" / "html"


class Application:
    def __init__(self, atividades: Atividades, avisar_atualizacao):
        self.atividades = atividades
        self.avisar_atualizacao = avisar_atualizacao

    def foco(self):
        return self._plano("foco.tpl")

    def lista(self):
        return self._plano("atividades_lista.tpl")

    def _plano(self, pagina):
        return template(
            pagina,
            template_lookup=[str(VIEWS_ROOT)],
            atividades=self.atividades.listar(),
            **request.environ["foco.contexto"],
        )

    def nova(self):
        return self._formulario({"dia": "", "titulo": "", "descricao": ""}, {})

    def criar(self):
        valores, erros = self._validar_formulario()
        if erros:
            response.status = 422
            return self._formulario(valores, erros)

        self.atividades.criar(**valores)
        self.avisar_atualizacao()
        return redirect("/foco")

    def editar(self, atividade_id):
        atividade = self.atividades.buscar(atividade_id)
        if atividade is None:
            abort(404, "Atividade não encontrada.")

        valores = {
            "dia": atividade.dia,
            "titulo": atividade.titulo,
            "descricao": atividade.descricao,
        }
        return self._formulario(valores, {}, atividade_id)

    def atualizar(self, atividade_id):
        valores, erros = self._validar_formulario()
        if erros:
            if self.atividades.buscar(atividade_id) is None:
                abort(404, "Atividade não encontrada.")
            response.status = 422
            return self._formulario(valores, erros, atividade_id)

        if not self.atividades.atualizar(atividade_id, **valores):
            abort(404, "Atividade não encontrada.")
        self.avisar_atualizacao()
        return redirect("/foco")

    def excluir(self, atividade_id):
        if not self.atividades.excluir(atividade_id):
            abort(404, "Atividade não encontrada.")
        self.avisar_atualizacao()
        return redirect("/foco")

    def _formulario(self, valores, erros, atividade_id=None):
        return template(
            "atividade_form.tpl",
            template_lookup=[str(VIEWS_ROOT)],
            valores=valores,
            erros=erros,
            dias=DIAS,
            atividade_id=atividade_id,
            **request.environ["foco.contexto"],
        )

    def _validar_formulario(self):
        valores = {
            campo: request.forms.getunicode(campo, "").strip()
            for campo in ("dia", "titulo", "descricao")
        }
        valores["descricao"] = valores["descricao"].replace("\r\n", "\n").replace("\r", "\n")
        erros = {}
        if valores["dia"] not in DIAS:
            erros["dia"] = "Selecione um dia da semana."
        if not 1 <= len(valores["titulo"]) <= 80:
            erros["titulo"] = "Informe um título de 1 a 80 caracteres."
        if not 1 <= len(valores["descricao"]) <= 300:
            erros["descricao"] = "Informe uma descrição de 1 a 300 caracteres."
        return valores, erros