from fastapi import FastAPI

from app.dtos.response import Response
from app.sockets import socket_io
from app.database.database import init_db
from app.routers import MainRouter
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(MainRouter)


@app.get("/api/room/{room_id}")
async def get_room(room_id: str):
    room = socket_io.get_room(room_id)
    if room is None:
        return Response(is_error=True, message="Room not found").to_dict()
    return Response(data={"room": {
        "id": room.id,
        "player_1": room.player_1,
        "player_2": room.player_2,
        "game": room.game.fen() if room.game is not None else None,
        "white_id": room.white_id
    }}).to_dict()


#  đường dẫn /socket.io
app.mount("/", socket_io.sio_app)

init_db()
