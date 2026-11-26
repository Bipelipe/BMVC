"use strict";

const senha = document.querySelector("#senha");
const alternarSenha = document.querySelector("#alternar-senha");

alternarSenha.addEventListener("click", () => {
    const senhaOculta = senha.type === "password";
    senha.type = senhaOculta ? "text" : "password";
    alternarSenha.textContent = senhaOculta ? "Ocultar senha" : "Mostrar senha";
});

alternarSenha.hidden = false;