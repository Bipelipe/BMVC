<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Entrar | Foco Time</title>
    <link rel="stylesheet" href="/static/css/foco.css">
    <script src="/static/js/login.js" defer></script>
</head>
<body>
    <header class="topbar">
        <div class="shell topbar-content">
            <a class="brand" href="/">Foco Time</a>
        </div>
    </header>

    <main class="shell form-page">
        <section class="plan form-panel" aria-labelledby="titulo-login">
            <h1 id="titulo-login">Entrar</h1>
            <p class="login-intro">Entre para acessar o plano de estudos.</p>
            % if erro:
                <p class="field-error" role="alert">{{erro}}</p>
            % end

            <form class="login-form" method="post" action="/login">
                <input type="hidden" name="csrf" value="{{csrf}}">
                <div class="form-field">
                    <label for="usuario">Usuário</label>
                    <input id="usuario" name="usuario" value="{{usuario}}" autocomplete="username" required>
                </div>

                <div class="form-field">
                    <label for="senha">Senha</label>
                    <input id="senha" name="senha" type="password" autocomplete="current-password" required>
                    <button id="alternar-senha" class="text-button" type="button" aria-controls="senha" hidden>Mostrar senha</button>
                </div>

                <div class="form-actions">
                    <button class="action-primary" type="submit">Entrar</button>
                </div>
            </form>
        </section>
    </main>
</body>
</html>