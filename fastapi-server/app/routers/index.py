from fastapi import APIRouter, Depends, Request
from app.templates import templates
from fastapi.responses import HTMLResponse
from app.sockets.socket_io import get_room
MainRouter = APIRouter(
    prefix="/home",
)


@MainRouter.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html",context= {"request": request})
@MainRouter.get("/game/{game_id}", response_class=HTMLResponse)
async def game_page(request: Request, game_id: int):
    room = get_room(game_id)
    if room is None:
        return templates.TemplateResponse("not_found.html",context= {"request": request},status_code=404)
    return templates.TemplateResponse("game.html",context= {"request": request, "game_id": game_id, "room": room})