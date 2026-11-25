"use strict";

const duration = 25 * 60 * 1000;
const display = document.querySelector("#tempo");
const statusMessage = document.querySelector("#estado");
const toggleButton = document.querySelector("#alternar");
const resetButton = document.querySelector("#reiniciar");

let remaining = duration;
let deadline = 0;
let intervalId = null;

function renderTime() {
    const seconds = Math.ceil(remaining / 1000);
    const minutesText = String(Math.floor(seconds / 60)).padStart(2, "0");
    const secondsText = String(seconds % 60).padStart(2, "0");
    display.textContent = `${minutesText}:${secondsText}`;
}

function stopCounting() {
    window.clearInterval(intervalId);
    intervalId = null;
}

function updateTime() {
    remaining = Math.max(0, deadline - performance.now());
    renderTime();

    if (remaining === 0) {
        stopCounting();
        statusMessage.textContent = "Sessão concluída";
        toggleButton.textContent = "Iniciar";
    }
}

toggleButton.addEventListener("click", () => {
    if (intervalId !== null) {
        updateTime();
        if (remaining > 0) {
            stopCounting();
            statusMessage.textContent = "Sessão pausada";
            toggleButton.textContent = "Continuar";
        }
        return;
    }

    if (remaining === 0) {
        remaining = duration;
    }

    deadline = performance.now() + remaining;
    intervalId = window.setInterval(updateTime, 100);
    updateTime();
    statusMessage.textContent = "Sessão em andamento";
    toggleButton.textContent = "Pausar";
});

resetButton.addEventListener("click", () => {
    stopCounting();
    remaining = duration;
    renderTime();
    statusMessage.textContent = "Pronto para começar";
    toggleButton.textContent = "Iniciar";
});

toggleButton.disabled = false;
resetButton.disabled = false;

document.querySelectorAll(".activity-remove").forEach((form) => {
    form.addEventListener("submit", (event) => {
        if (!window.confirm("Excluir esta atividade do plano?")) {
            event.preventDefault();
        }
    });
});