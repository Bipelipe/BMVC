const lista = document.querySelector("#lista-atividades");
const estadoConexao = document.querySelector("#tempo-real-estado");

const endereco = new URL("/ws/atividades", window.location.href);
endereco.protocol = window.location.protocol === "https:" ? "wss:" : "ws:";

let conexao;
let demoraParaReconectar = 1000;
let atualizacaoPendente = false;
let atualizacaoEmCurso = null;

function irParaLogin() {
    window.location.replace("/login");
}

async function consultarLista() {
    const resposta = await fetch("/atividades/lista", {
        cache: "no-store",
        signal: AbortSignal.timeout(10000),
    });

    if (resposta.redirected) {
        irParaLogin();
        return null;
    }

    if (!resposta.ok) {
        throw new Error("Falha ao carregar a lista de atividades.");
    }

    return resposta.text();
}

function solicitarAtualizacao() {
    atualizacaoPendente = true;
    atualizacaoEmCurso ??= atualizarLista().finally(() => {
        atualizacaoEmCurso = null;
    });
}

async function atualizarLista() {
    try {
        while (atualizacaoPendente) {
            atualizacaoPendente = false;
            const html = await consultarLista();

            if (html === null) {
                return;
            }

            if (!atualizacaoPendente && conexao.readyState === WebSocket.OPEN) {
                if (lista.innerHTML.trim() !== html.trim()) {
                    lista.innerHTML = html;
                }
                if (estadoConexao.textContent !== "Atualização em tempo real ativa") {
                    estadoConexao.textContent = "Atualização em tempo real ativa";
                }
                demoraParaReconectar = 1000;
            }
        }
    } catch {
        conexao.close();
    }
}

async function reconectar() {
    await atualizacaoEmCurso;

    try {
        if ((await consultarLista()) === null) {
            return;
        }
    } catch {
        // A rede pode ainda estar indisponível.
    }

    conectar();
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

        estadoConexao.textContent = "Conexão interrompida. Reconectando…";
        window.setTimeout(reconectar, demoraParaReconectar);
        demoraParaReconectar = Math.min(demoraParaReconectar * 2, 10000);
    });
}

estadoConexao.textContent = "Conectando para receber atualizações…";
conectar();
