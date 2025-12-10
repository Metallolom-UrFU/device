async function fetchQR() {
    let code = 0;
    // TODO получить расшифрованный код с камеры
    if (code !== 0) submitCode();

}

function submitCode() {
    // TODO отправить код для проверки
}

const intervalId = setInterval(fetchQR, 1000);