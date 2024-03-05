from fastapi import Depends
import socketio



sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

sio_app = socketio.ASGIApp(sio,
                           socketio_path='socket.io',
                           )


@sio.event
async def connect(sid, environ):
    print(f"connect {sid}")

