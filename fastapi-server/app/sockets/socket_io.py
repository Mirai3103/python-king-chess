from fastapi import Depends
import socketio
from app.core.chess import chess


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

sio_app = socketio.ASGIApp(sio,
                           socketio_path='socket.io',
                           )


@sio.event
async def connect(sid, environ):
    session = await sio.get_session(sid)
    session['chess']= chess.Chess()
    print(f"connect {sid}")
@sio.event
async def message(sid, data):
    session = await sio.get_session(sid)
    print(session['chess'].fen())
    print(f"message {sid} {data}")
    
