
from fastapi import FastAPI
from app.sockets import socket_io
from app.database.database import init_db
from app.routers.user import UserRouter
app = FastAPI()



app.include_router(UserRouter)

@app.get("/")
async def root():
    return {"message": "Hello World"}

#  đường dẫn /socket.io
app.mount("/", socket_io.sio_app)

init_db()