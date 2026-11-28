"use strict";

const description = document.querySelector("#descricao");
const descriptionHint = document.querySelector("#descricao-limite");

function updateCharacterCount() {
    descriptionHint.textContent = `${description.value.length}/${description.maxLength} caracteres`;
}

description.addEventListener("input", updateCharacterCount);
updateCharacterCount();
