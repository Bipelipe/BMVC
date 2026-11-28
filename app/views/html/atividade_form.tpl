% if atividade_id is None:
    % titulo_pagina = "Nova atividade"
    % destino = "/atividades"
% else:
    % titulo_pagina = "Editar atividade"
    % destino = f"/atividades/{atividade_id}/editar"
% end
<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{titulo_pagina}} | Foco Time</title>
    <link rel="stylesheet" href="/static/css/foco.css">
    <script src="/static/js/atividade_form.js" defer></script>
</head>
<body>
    <header class="topbar">
        <div class="shell topbar-content">
            <a class="brand" href="/foco">Foco Time</a>
            <nav aria-label="Navegação">
                <a href="/foco#plano">Plano semanal</a>
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

    <main class="shell form-page">
        <section class="plan form-panel" aria-labelledby="titulo-form">
            <h1 id="titulo-form">{{titulo_pagina}}</h1>
            % if erros:
                <p class="field-error" role="alert">Revise os campos indicados e tente novamente.</p>
            % end

            <form class="activity-form" method="post" action="{{destino}}">
                <input type="hidden" name="csrf" value="{{csrf}}">
                <div class="form-field">
                    <label for="dia">Dia da semana</label>
                    <select id="dia" name="dia" required {{'aria-invalid=true aria-describedby=erro-dia' if 'dia' in erros else ''}}>
                        <option value="">Selecione o dia</option>
                        % for dia in dias:
                            <option value="{{dia}}" {{'selected' if valores['dia'] == dia else ''}}>{{dia}}</option>
                        % end
                    </select>
                    % if 'dia' in erros:
                        <p class="field-error" id="erro-dia">{{erros['dia']}}</p>
                    % end
                </div>

                <div class="form-field">
                    <label for="titulo">Título</label>
                    <input id="titulo" name="titulo" value="{{valores['titulo']}}" required maxlength="80" {{'aria-invalid=true aria-describedby=erro-titulo' if 'titulo' in erros else ''}}>
                    % if 'titulo' in erros:
                        <p class="field-error" id="erro-titulo">{{erros['titulo']}}</p>
                    % end
                </div>

                <div class="form-field">
                    <label for="descricao">Descrição</label>
                    <textarea id="descricao" name="descricao" rows="5" maxlength="300" required aria-describedby="{{'descricao-limite erro-descricao' if 'descricao' in erros else 'descricao-limite'}}" {{'aria-invalid=true' if 'descricao' in erros else ''}}>{{valores['descricao']}}</textarea>
                    <p class="field-hint" id="descricao-limite">Até 300 caracteres</p>
                    % if 'descricao' in erros:
                        <p class="field-error" id="erro-descricao">{{erros['descricao']}}</p>
                    % end
                </div>

                <div class="form-actions">
                    <button class="action-primary" type="submit">Salvar atividade</button>
                    <a href="/foco#plano">Cancelar</a>
                </div>
            </form>
        </section>
    </main>
</body>
</html>
