from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="ShelfLocal")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pickup", response_class=HTMLResponse)
async def render_pickup(request: Request):
    return templates.TemplateResponse("pickup.html", {"request": request})


@app.get("/return", response_class=HTMLResponse)
async def render_return(request: Request):
    return templates.TemplateResponse("return.html", {"request": request})


@app.get("/download", response_class=HTMLResponse)
async def render_download(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})
