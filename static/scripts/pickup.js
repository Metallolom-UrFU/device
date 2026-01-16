function addSymbol(n) {
    const elem = document.querySelector("#input-code");
    if (elem.value.length >= 16) return;
    elem.value += n;
}

function removeSymbol() {
    const elem = document.querySelector("#input-code");
    elem.value = elem.value.slice(0, -1);
}

function submitCode() {
    const input = document.querySelector("#input-code");
    const code = input.value.trim();
    if (!code) return;


    if (window.submittedPickup) return;
    window.submittedPickup = true;

    window.location.replace("/pickup?code=" + encodeURIComponent(code));
}


document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("#input-code");
    const form = document.querySelector("#pickup-form");

    input.focus();
    document.addEventListener("click", () => input.focus());
    setInterval(() => input.focus(), 500);

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault(); 
            submitCode();
        }
    });

    if (form) {
        form.addEventListener("submit", (e) => e.preventDefault());
    }
});

