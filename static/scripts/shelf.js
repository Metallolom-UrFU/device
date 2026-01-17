async function fetchDoor() {
    let response = await fetch("/fetch-door");
    let data = await response.json();
    let door = data["door"];
    if (door) window.location.replace("/");
}

setInterval(fetchDoor, 1000);
