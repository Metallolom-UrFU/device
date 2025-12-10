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
    let code = 0;
    // TODO получить расшифрованный код с камеры
    if (code === 0) return;

    let elem = document.querySelector("#input-code");
    elem.value = code;
    submitCode();
}

function submitCode() {
    let elem = document.querySelector("#input-code");
    let value = elem.value;
    // TODO отправить код для проверки
}

const intervalId = setInterval(fetchQR, 1000);