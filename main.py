from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from requests import post

app = FastAPI(title="ShelfLocal")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

URL_BASE = "http://158.160.198.52:8000/"
URL_PICKUP = f"{URL_BASE}/reservations/pickup"
URL_RETURN = f"{URL_BASE}/reservations/return"

SHELF_ID = "57a5fe24-f280-4897-ba9d-4177a6174748"


@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/download", response_class=HTMLResponse)
async def render_download(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})


@app.get("/pickup", response_class=HTMLResponse)
async def render_pickup(request: Request, code: str | None = None):
    if not code:
        return templates.TemplateResponse("pickup.html", {"request": request})

    result = post(f"{URL_PICKUP}?pickup_code={code}")

    if result.status_code != 200:
        return templates.TemplateResponse("error.html", {"request": request})

    # TODO открыть полку с книжкой

    return templates.TemplateResponse("shelf-out.html", {"request": request})


@app.get("/return", response_class=HTMLResponse)
async def render_return(request: Request, code: str | None = None):
    if not code:
        return templates.TemplateResponse("return.html", {"request": request})

    result = post(
        f"{URL_RETURN}",
        json={"book_code": code, "shelf_id": SHELF_ID}
    )

    if result.status_code != 200:
        return templates.TemplateResponse("error.html", {"request": request})

    # TODO открыть какую-нибудь полку

    return templates.TemplateResponse("shelf-in.html", {"request": request})


@app.get("/fetch-qr")
async def fetch_qr():
    # TODO считать код с камеры, раскодировать его и вернуть результат
    return {"code": "0"}


@app.get("/fetch-door")
async def fetch_door():
    # TODO считать датчик закрытия двери и вернуть результат
    #      false = дверь открыта, true = дверь закрыта
    return {"door": False}
