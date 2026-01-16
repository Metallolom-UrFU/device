from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from requests import post
from shelves.manager import ShelfManager

import atexit
from RPi import GPIO

app = FastAPI(title="ShelfLocal")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

shelf_manager = ShelfManager("shelves/config.yaml")

URL_BASE = "http://158.160.198.52:8000/"
URL_PICKUP = f"{URL_BASE}/reservations/pickup"
URL_RETURN = f"{URL_BASE}/reservations/return"


@atexit.register
def cleanup_gpio():
    GPIO.cleanup()

def get_free_shelf():
    
    for shelf in shelf_manager.all():
        if shelf.is_closed() and shelf.locked:
            return shelf
    return None

@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/download", response_class=HTMLResponse)
async def render_download(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})

@app.get("/pickup", response_class=HTMLResponse)
async def pickup(request: Request, code: str | None = None):
    if not code:
        return templates.TemplateResponse("pickup.html", {"request": request})

    result = post(f"{URL_PICKUP}?pickup_code={code}")
    if result.status_code != 200:
        return templates.TemplateResponse("error.html", {"request": request})

    data = result.json()
    shelf_id = data.get("shelf_id")

    shelf = shelf_manager.get(shelf_id)
    if not shelf:
        return templates.TemplateResponse("error.html", {"request": request})

    shelf.unlock()

    return templates.TemplateResponse(
        "shelf-out.html",
        {"request": request, "shelf_id": shelf.id}
    )

@app.get("/return", response_class=HTMLResponse)
async def render_return(request: Request, code: str | None = None):
    if not code:
        return templates.TemplateResponse("return.html", {"request": request})

    result = post(URL_RETURN, json={"book_code": code})
    if result.status_code != 200:
        return templates.TemplateResponse("error.html", {"request": request})

    shelf = get_free_shelf()
    if not shelf:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Нет свободных полок"}
        )

    shelf.unlock()

    return templates.TemplateResponse(
        "shelf-in.html",
        {"request": request, "shelf_id": shelf.id}
    )

@app.get("/fetch-door/{shelf_id}")
async def fetch_door(shelf_id: str):
    shelf = shelf_manager.get(shelf_id)
    if not shelf:
        return {"error": "unknown shelf"}

    if shelf.is_closed():
        shelf.lock()
        return {"door": True}

    return {"door": False}
