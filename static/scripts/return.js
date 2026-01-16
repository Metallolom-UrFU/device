function addSymbol(n) {
    let elem = document.querySelector("#input-code");
    if (elem.value.length >= 16) return;
    elem.value += n;
}

function removeSymbol() {
    let elem = document.querySelector("#input-code");
    elem.value = elem.value.slice(0, -1);
}

function submitCode() {
    let elem = document.querySelector("#input-code");
    let code = elem.value.trim();
    if (!code) return;

    window.location.replace("/return?code=" + encodeURIComponent(code));
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("#input-code");

    input.focus();
    document.addEventListener("click", () => input.focus());
    setInterval(() => input.focus(), 500);

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            submitCode();
        }
    });
});