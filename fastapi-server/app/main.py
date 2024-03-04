from typing import Union

from fastapi import FastAPI
from app.sockets import socket_io
from app.database.database import init_db
from app.routers.user import UserRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
)


app.mount("/", socket_io.sio_app)

app.include_router(UserRouter)
init_db()