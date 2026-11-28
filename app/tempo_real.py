import asyncio
from http.cookies import CookieError, SimpleCookie

from a2wsgi import WSGIMiddleware

from app.controllers.autenticacao import COOKIE_SESSAO


class TempoReal:
    def __init__(self, app_http, usuarios):
        self.http = WSGIMiddleware(app_http)
        self.usuarios = usuarios
        self.loop = None
        self.assinantes = set()

    def avisar(self):
        loop = self.loop
        if loop is not None:
            loop.call_soon_threadsafe(self._notificar)

    def _notificar(self):
        for evento in self.assinantes:
            evento.set()

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            await self.http(scope, receive, send)
        elif scope["type"] == "websocket":
            await self._websocket(scope, receive, send)
        elif scope["type"] == "lifespan":
            await receive()
            self.loop = asyncio.get_running_loop()
            await send({"type": "lifespan.startup.complete"})
            await receive()
            self.loop = None
            await send({"type": "lifespan.shutdown.complete"})

    async def _websocket(self, scope, receive, send):
        conexao = await receive()
        if conexao["type"] != "websocket.connect":
            return

        token = self._token_se_mesma_origem(scope)
        if scope["path"] != "/ws/atividades" or not await self._sessao_valida(token):
            await send({"type": "websocket.close", "code": 1008})
            return

        evento = asyncio.Event()
        self.assinantes.add(evento)
        entrada = asyncio.create_task(receive())
        alteracao = asyncio.create_task(evento.wait())
        try:
            await send({"type": "websocket.accept"})
            while True:
                prontas, _ = await asyncio.wait(
                    (entrada, alteracao), timeout=5,
                    return_when=asyncio.FIRST_COMPLETED,
                )
                if entrada in prontas:
                    if entrada.result()["type"] != "websocket.disconnect":
                        await send({"type": "websocket.close", "code": 1008})
                    return

                if not await self._sessao_valida(token):
                    await send({"type": "websocket.close", "code": 1008})
                    return

                if alteracao in prontas:
                    evento.clear()
                    await send({
                        "type": "websocket.send",
                        "text": '{"tipo":"atividades"}',
                    })
                    alteracao = asyncio.create_task(evento.wait())
        except OSError:
            return
        finally:
            self.assinantes.discard(evento)
            entrada.cancel()
            alteracao.cancel()
            await asyncio.gather(entrada, alteracao, return_exceptions=True)

    async def _sessao_valida(self, token):
        return token and await asyncio.to_thread(self.usuarios.usuario_da_sessao, token)

    def _token_se_mesma_origem(self, scope):
        headers = dict(scope["headers"])
        protocolo = b"https" if scope["scheme"] == "wss" else b"http"
        host = headers.get(b"host")
        if not host or headers.get(b"origin") != protocolo + b"://" + host:
            return None

        cookies = SimpleCookie()
        try:
            cookies.load(headers.get(b"cookie", b"").decode("latin-1"))
        except CookieError:
            return None
        sessao = cookies.get(COOKIE_SESSAO)
        return sessao.value if sessao else None