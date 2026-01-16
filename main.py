from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from requests import post
from shelves.manager import ShelfManager

import time

app = FastAPI(title="ShelfLocal")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

shelf_manager = ShelfManager("shelves/config.yaml")

URL_BASE = "http://158.160.198.52:8000/"
URL_PICKUP = f"{URL_BASE}/reservations/pickup"
URL_RETURN = f"{URL_BASE}/reservations/return"

ACTIVE_SHELF = None
ACTIVE_SHELF_OPEN_TIME = None
DOOR_TIMEOUT = 30 


@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/download", response_class=HTMLResponse)
async def render_download(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})


@app.get("/pickup", response_class=HTMLResponse)
async def pickup(request: Request, code: str | None = None):
    global ACTIVE_SHELF, ACTIVE_SHELF_OPEN_TIME

    if not code:
        return templates.TemplateResponse("pickup.html", {"request": request})

    result = post(f"{URL_PICKUP}?pickup_code={code}")
    if result.status_code != 200:
        return templates.TemplateResponse("error.html", {"request": request})

    shelf = shelf_manager.get_free_shelf()
    if not shelf:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Нет свободных полок"}
        )

    shelf.unlock()
    ACTIVE_SHELF = shelf
    ACTIVE_SHELF_OPEN_TIME = time.time()

    return templates.TemplateResponse("shelf-out.html", {"request": request})


@app.get("/return", response_class=HTMLResponse)
async def render_return(request: Request, code: str | None = None):
    global ACTIVE_SHELF, ACTIVE_SHELF_OPEN_TIME

    if not code:
        return templates.TemplateResponse("return.html", {"request": request})

    result = post(URL_RETURN, json={"book_code": code})
    if result.status_code != 200:
        return templates.TemplateResponse("error.html", {"request": request})

    shelf = shelf_manager.get_free_shelf()
    if not shelf:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Нет свободных полок"}
        )

    shelf.unlock()
    ACTIVE_SHELF = shelf
    ACTIVE_SHELF_OPEN_TIME = time.time()

    return templates.TemplateResponse("shelf-in.html", {"request": request})


@app.get("/fetch-door")
async def fetch_door():
    global ACTIVE_SHELF, ACTIVE_SHELF_OPEN_TIME

    if not ACTIVE_SHELF:
        return {"door": False}

    if ACTIVE_SHELF.is_closed():
        shelf_manager.release_shelf(ACTIVE_SHELF)
        ACTIVE_SHELF = None
        ACTIVE_SHELF_OPEN_TIME = None
        return {"door": True}

    if time.time() - ACTIVE_SHELF_OPEN_TIME > DOOR_TIMEOUT:
        shelf_manager.release_shelf(ACTIVE_SHELF)
        ACTIVE_SHELF = None
        ACTIVE_SHELF_OPEN_TIME = None
        return {"door": False, "timeout": True}

    return {"door": False}
