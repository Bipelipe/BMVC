const lista = document.querySelector("#lista-atividades");
const estadoConexao = document.querySelector("#tempo-real-estado");

const endereco = new URL("/ws/atividades", window.location.href);
endereco.protocol = window.location.protocol === "https:" ? "wss:" : "ws:";

let conexao;
let demoraParaReconectar = 1000;
let atualizacaoPendente = false;
let atualizando = false;
let ultimoHtml = lista.innerHTML.trim();

function mostrarEstado(mensagem) {
    if (estadoConexao.textContent !== mensagem) {
        estadoConexao.textContent = mensagem;
    }
}

function irParaLogin() {
    window.location.replace("/login");
}

async function consultarLista() {
    const requisicao = new AbortController();
    const prazo = window.setTimeout(() => requisicao.abort(), 10000);

    try {
        const resposta = await fetch("/atividades/lista", {
            cache: "no-store",
            signal: requisicao.signal,
        });

        if (resposta.redirected) {
            irParaLogin();
            return null;
        }

        if (!resposta.ok) {
            throw new Error("Falha ao carregar a lista de atividades.");
        }

        return await resposta.text();
    } finally {
        window.clearTimeout(prazo);
    }
}

function solicitarAtualizacao() {
    atualizacaoPendente = true;
    if (!atualizando) {
        atualizarLista();
    }
}

async function atualizarLista() {
    atualizando = true;
    try {
        while (atualizacaoPendente) {
            atualizacaoPendente = false;
            const html = await consultarLista();

            if (html === null) {
                return;
            }

            const proximoHtml = html.trim();
            if (proximoHtml !== ultimoHtml) {
                lista.innerHTML = html;
                ultimoHtml = proximoHtml;
            }

            if (conexao.readyState === WebSocket.OPEN) {
                mostrarEstado("Atualização em tempo real ativa");
                demoraParaReconectar = 1000;
            } else {
                mostrarEstado("Reconectando ao WebSocket. A lista atualiza por consulta.");
            }
        }
    } catch {
        mostrarEstado("Falha ao consultar o plano. Reconectando…");
        if (conexao.readyState === WebSocket.OPEN) {
            conexao.close();
        }
    } finally {
        atualizando = false;
    }
}

function conectar() {
    conexao = new WebSocket(endereco);
    conexao.addEventListener("open", solicitarAtualizacao);
    conexao.addEventListener("message", (evento) => {
        let mensagem;
        try {
            mensagem = JSON.parse(evento.data);
        } catch {
            return;
        }

        if (mensagem?.tipo === "atividades") {
            solicitarAtualizacao();
        }
    });
    conexao.addEventListener("close", (evento) => {
        if (evento.code === 1008) {
            irParaLogin();
            return;
        }

        mostrarEstado("Conexão interrompida. Reconectando…");
        solicitarAtualizacao();
        window.setTimeout(conectar, demoraParaReconectar);
        demoraParaReconectar = Math.min(demoraParaReconectar * 2, 10000);
    });
}

mostrarEstado("Conectando para receber atualizações…");
conectar();
window.setInterval(() => {
    if (conexao.readyState !== WebSocket.OPEN && !atualizando) {
        solicitarAtualizacao();
    }
}, 2000);
