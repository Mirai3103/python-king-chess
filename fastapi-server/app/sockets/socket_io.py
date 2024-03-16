from typing import Optional
from uuid import UUID
import uuid
from chess import Board, Move
from socketio import AsyncServer, ASGIApp
from app.core.chess import chess
from app.core.chess.type import PieceColor
from app.dtos.response import Response

sio = AsyncServer(async_mode='asgi', cors_allowed_origins=[])

sio_app = ASGIApp(sio,
                  socketio_path='socket.io',
                  )


# todo: refactor this and implement your own logic

class Room:
    id: str
    player_1: Optional[str] = None
    player_2: Optional[str] = None
    game: Optional[chess.Chess] = None
    white_id: Optional[str] = None

    def leave(self, sid):
        if self.player_1 == sid:
            self.player_1 = None
        else:
            self.player_2 = None
        if self.player_1 is None and self.player_2 is None:
            del rooms_dict[self.id]

    def is_full(self):
        return self.player_1 is not None and self.player_2 is not None

    def is_empty(self):
        return self.player_1 is None and self.player_2 is None

    def is_in_room(self, sid):
        return self.player_1 == sid or self.player_2 == sid


rooms_dict: dict[str, Room] = {}


def get_room(room_id: str) -> Optional[Room]:
    return rooms_dict.get(room_id)


@sio.event
async def connect(sid, environ):
    session = await sio.get_session(sid)
    session['chess'] = chess.Chess()
    print(f"connect {sid}")


@sio.event
async def message(sid, data):
    session = await sio.get_session(sid)
    print(session['chess'].fen())
    print(f"message {sid} {data}")


@sio.event
async def disconnect(sid):
    in_room = None
    for room in rooms_dict.values():
        if room.is_in_room(sid):
            in_room = room
            break
    if in_room is not None:
        in_room.leave(sid)
        await sio.emit("a_player_left", room=in_room.id)
        del rooms_dict[in_room.id]
    print(f"disconnect {sid}")


@sio.on("create_invite")
async def create_invite(sid, data):
    am_i_white = data["am_i_white"]
    my_room = sio.rooms(sid)
    my_room.remove(sid)
    if len(my_room) > 0:
        await sio.leave_room(sid, my_room[0])
        room = rooms_dict[my_room[0]]
        room.leave(sid)
        if room.is_empty():
            if rooms_dict.get(room.id) is not None:
                del rooms_dict[room.id]
    room_id = str(uuid.uuid4())
    await sio.enter_room(sid, room_id)
    new_room = Room()
    new_room.id = room_id
    new_room.player_1 = sid
    new_room.white_id = sid if am_i_white else None

    rooms_dict[room_id] = new_room
    return Response(False, data={"room_id": room_id}, message="Room created").to_dict()


@sio.on("start_game")
async def start_game(sid, data):
    my_room = sio.rooms(sid)
    my_room.remove(sid)
    if len(my_room) == 0:
        return Response(True, message="You are not in a room").to_dict()
    room = rooms_dict[my_room[0]]
    if room.player_1 != sid:
        return Response(True, message="You are not the host").to_dict()
    if room.is_full():
        room.game = chess.Chess()
        await sio.emit("game_started", room=room.id, data={"white_id": room.white_id, "fen": room.game.fen()})
        return Response(False, message="Game started").to_dict()
    return Response(True, message="Room is not full").to_dict()


@sio.on("join_invite")
async def join_invite(sid, data):
    room = rooms_dict.get(data)
    if room is None:
        return Response(True, message="Room not found").to_dict()
    if room.is_full():
        return Response(True, message="Room is full").to_dict()
    await sio.enter_room(sid, data)
    await sio.emit("a_player_joined", room=data)
    room.player_2 = sid
    room.game = chess.Chess()
    room.white_id = room.white_id if room.white_id is not None else sid
    await sio.emit("game_started", room=room.id, data={"white_id": room.white_id, "fen": room.game.fen()})
    print(f"emit game_started {room.id}")
    return Response(False, message="Joined room").to_dict()


@sio.on("move")
async def move(sid, data):
    room = data["room_id"]
    if room is None:
        return Response(True, message="Room not found").to_dict()
    room = rooms_dict[room]
    game = room.game
    own_color = PieceColor.WHITE if room.white_id == sid else PieceColor.BLACK
    if game is None:
        return Response(True, message="Game not started").to_dict()
    if game._turn != own_color:
        return Response(True, message="Not your turn").to_dict()

    move = data["move"]
    from_square = move["from"]
    to_square = move["to"]

    board = Board(game.fen())
    board.push_uci(f"{from_square}{to_square}")
    game.load(board.fen())
    await sio.emit("moved", room=room.id, data={"board": board.fen()})
