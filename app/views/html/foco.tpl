<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Foco OO | Plano de estudos</title>
    <link rel="stylesheet" href="/static/css/foco.css">
    <script src="/static/js/foco.js" defer></script>
</head>
<body>
    <header class="topbar">
        <div class="shell topbar-content">
            <a class="brand" href="/foco">Foco OO</a>
            <nav aria-label="Nesta página">
                <a href="#plano">Plano semanal</a>
                <a href="#cronometro">Cronômetro</a>
            </nav>
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
                <h2 id="plano-titulo">Plano semanal</h2>
                <ul class="activities">
                    <li>
                        <p class="day">Segunda</p>
                        <div>
                            <h3>Classes e objetos</h3>
                            <p>Crie uma classe <code>Livro</code> e instancie dois livros com títulos diferentes.</p>
                        </div>
                    </li>
                    <li>
                        <p class="day">Terça</p>
                        <div>
                            <h3>Encapsulamento</h3>
                            <p>Defina como uma conta bancária valida depósitos e saques.</p>
                        </div>
                    </li>
                    <li>
                        <p class="day">Quarta</p>
                        <div>
                            <h3>Herança</h3>
                            <p>Crie classes <code>Bicicleta</code> e <code>Carro</code> que herdem de <code>Veiculo</code>.</p>
                        </div>
                    </li>
                    <li>
                        <p class="day">Quinta</p>
                        <div>
                            <h3>Polimorfismo</h3>
                            <p>Implemente o método <code>area()</code> em um retângulo e em um círculo.</p>
                        </div>
                    </li>
                    <li>
                        <p class="day">Sexta</p>
                        <div>
                            <h3>Revisão prática</h3>
                            <p>Releia os exercícios e explique a decisão de design de cada um.</p>
                        </div>
                    </li>
                </ul>
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