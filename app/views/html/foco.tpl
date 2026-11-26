<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Foco Time | Plano de estudos</title>
    <link rel="stylesheet" href="/static/css/foco.css">
    <script src="/static/js/foco.js" defer></script>
</head>
<body>
    <header class="topbar">
        <div class="shell topbar-content">
            <a class="brand" href="/foco">Foco Time</a>
            <nav aria-label="Nesta página">
                <a href="#plano">Plano semanal</a>
                <a href="#cronometro">Cronômetro</a>
            </nav>
            <div class="session-controls">
                <span class="session-user">Conectado como <strong>{{usuario}}</strong></span>
                <form method="post" action="/sair">
                    <input type="hidden" name="csrf" value="{{csrf}}">
                    <button type="submit" class="text-button">Sair</button>
                </form>
            </div>
        </div>
    </header>

    <main class="shell">
        <section class="intro" aria-labelledby="titulo">
            <p class="eyebrow">Orientação a Objetos</p>
            <h1 id="titulo">Sua semana de estudos</h1>
            <p>Escolha uma atividade do plano e reserve 25 minutos para praticar.</p>
        </section>

        <div class="study-layout">
            <section class="plan" id="plano" aria-labelledby="plano-titulo">
                <div class="plan-heading">
                    <h2 id="plano-titulo">Plano semanal</h2>
                    <a class="action-primary" href="/atividades/nova">Nova atividade</a>
                </div>
                % if atividades:
                    <ul class="activities">
                        % for atividade in atividades:
                            <li>
                                <p class="day">{{atividade.dia}}</p>
                                <div class="activity-content">
                                    <h3>{{atividade.titulo}}</h3>
                                    <p>{{atividade.descricao}}</p>
                                    <div class="activity-actions">
                                        <a href="/atividades/{{atividade.id}}/editar" aria-label="Editar {{atividade.titulo}}">Editar</a>
                                        <form class="activity-remove" method="post" action="/atividades/{{atividade.id}}/excluir">
                                            <input type="hidden" name="csrf" value="{{csrf}}">
                                            <button type="submit" aria-label="Excluir {{atividade.titulo}}">Excluir</button>
                                        </form>
                                    </div>
                                </div>
                            </li>
                        % end
                    </ul>
                % else:
                    <p class="empty-plan">Seu plano está vazio. Crie uma atividade para começar.</p>
                % end
            </section>

            <section class="timer" id="cronometro" aria-labelledby="timer-titulo">
                <h2 id="timer-titulo">Cronômetro de foco</h2>
                <p class="timer-display" id="tempo" role="timer" aria-label="Tempo restante">25:00</p>
                <p id="estado" role="status">Pronto para começar</p>
                <div class="timer-actions">
                    <button id="alternar" type="button" disabled>Iniciar</button>
                    <button id="reiniciar" type="button" disabled>Reiniciar</button>
                </div>
                <noscript>Ative o JavaScript para usar o cronômetro.</noscript>
            </section>
        </div>
    </main>
</body>
</html>