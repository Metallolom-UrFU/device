function addSymbol(n) {
    let elem = document.querySelector("#input-code");
    let value = elem.value;
    if (value.length >= 16) return;
    document.querySelector("#input-code").value += n;
}

function removeSymbol() {
    let elem = document.querySelector("#input-code");
    let value = elem.value;
    value = value.slice(0, -1);
    elem.value = value;
}

async function fetchQR() {
    let response = await fetch("/fetch-qr");
    let data = await response.json();

    let code = data["code"];
    if (code === "0") return;

    let elem = document.querySelector("#input-code");
    elem.value = code;
    submitCode();
}

function submitCode() {
    let elem = document.querySelector("#input-code");
    window.location.replace("/pickup?code=" + elem.value);
}

setTimeout(fetchQR, 10000);