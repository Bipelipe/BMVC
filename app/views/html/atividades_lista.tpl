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
