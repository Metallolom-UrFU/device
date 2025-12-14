async function fetchQR() {
    let response = await fetch("/fetch-qr");
    let data = await response.json();

    let code = data["code"];
    if (code !== "0") window.location.replace("/return?code=" + code);
}

setInterval(fetchQR, 1000);