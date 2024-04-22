from ast import Tuple
import socket
from time import sleep
from typing import Optional
from sqlalchemy import true
from stockfish import Stockfish
from app.dtos.response import Response
import uuid

from socketio import AsyncServer, ASGIApp
from app.core.chess import chess
from app.core.chess.type import CellName, PieceColor
from app.dtos.response import Response
sio = AsyncServer(async_mode='asgi', cors_allowed_origins=[])

sio_app = ASGIApp(sio,
                  socketio_path='socket.io',
                  )



@sio.event
async def make_move_to_bot(sid, data):
    fen = data["fen"]
    move = data["move"]
    game = chess.Chess()
    game.load(fen)
    moveRs=  game.move(CellName(move["from"]),CellName(move["to"]), move.get("promotion") if move.get("promotion") is not None else 'q')
    if moveRs is None:
        return Response(True, message="Nước đi không hợp lệ").to_dict()
    current_color = PieceColor.WHITE if game._turn == PieceColor.BLACK else PieceColor.BLACK    
    newFen = game.fen()
    
    async def get_move_from_bot_async( fen):
        st= Stockfish(path="stockfish/windows/stockfish.exe",
                        depth=1,
                        parameters={
                            "Threads": 1, "Minimum Thinking Time": 30
                        }
                        )
        st.set_skill_level(1)
        st.set_fen_position(fen)
        bot_move = st.get_best_move()
        
        st.make_moves_from_current_position([ bot_move])
        newFen = st.get_fen_position()
        return newFen, bot_move
    promise= get_move_from_bot_async(newFen)
    await sio.emit("update_fen", room=sid, data={"fen": newFen, "move": move})
    print("waiting for bot move")
    newFen, bot_move = await promise
    game.load(newFen)
    checked = False
    if game.is_check(current_color):
        checked =True
    
    await sio.emit("update_fen", room=sid, data={"fen": newFen, "move": bot_move, "checked": checked})
    print("bot move done")




# todo: refactor this and implement your own logic

class Room:
    id: str
    player_1: Optional[str] = None
    player_2: Optional[str] = None
    game: Optional[chess.Chess] = None
    white_id: Optional[str] = None
    player_1_remaining_time: int = 15*60
    player_2_remaining_time: int = 15*60

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
    def to_dict(self):
        return {
            "id": self.id,
            "player_1": self.player_1,
            "player_2": self.player_2,
            "fen": self.game.fen() if self.game is not None else None,
            "white_id": self.white_id,
            "player_1_remaining_time": self.player_1_remaining_time,
            "player_2_remaining_time": self.player_2_remaining_time,
            "player_1_name": self.player_1_name,
            "player_2_name": self.player_2_name
        }
    


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
    session = await sio.get_session(sid)
    session['room_id'] = room_id

    new_room = Room()
    new_room.id = room_id
    new_room.player_1 = sid
    new_room.white_id = sid if am_i_white else None
    new_room.player_1_name = session.get("display_name", "")

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
        sio.emit("game_started", room=room.id, data=room.to_dict())
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
    session = await sio.get_session(sid)
    session['room_id'] = data
    await sio.emit("a_player_joined", room=data)
    room.player_2 = sid
    room.game = chess.Chess()
    room.white_id = room.white_id if room.white_id is not None else sid
    room.player_2_name = session.get("display_name", "")
    await sio.emit("game_started", room=room.id, data=room.to_dict())
    print(f"emit game_started {room.id}")
    return Response(False, message="Joined room").to_dict()

@sio.on("time_out")
async def time_out(sid, data):
    # room = rooms_dict.get(data)
    # if room is None:
    #     return Response(True, message="Room not found").to_dict()
    # room = rooms_dict[room]
    # if room.white_id == sid:
    #     room.player_1_remaining_time = 0
    # else:
    #     room.player_2_remaining_time = 0
    # await sio.emit("time_out", room=room.id, data=room.to_dict())
    room_id = data["room_id"]
    room = get_room(room_id)
    if room is None:
        return Response(True, message="Room not found").to_dict()
    if room.white_id == sid:
        room.player_1_remaining_time = 0
    else:
        room.player_2_remaining_time = 0
    is_over, winner = check_game_over(room)
    print(is_over, winner)
    if is_over:
        await sio.emit("game_over", room=room_id, data={"winner": winner})
        await sio.emit("stop_game", room=room_id)
    else:
        # Nếu trò chơi chưa kết thúc, cập nhật thông tin và gửi sự kiện 'time_out'
        await sio.emit("time_out", room=room_id, data=room.to_dict())    
    #await sio.emit("time_out", room=room_id, data=room.to_dict())
#is_over
def check_game_over(room: Room) :
    game = room.game
    if game.is_checkmate(PieceColor.WHITE):
        return True, "white"
    if game.is_checkmate(PieceColor.BLACK):
        return True, "black"
    if game.is_stalemate(PieceColor.WHITE) or game.is_stalemate(PieceColor.BLACK):
        return True, "draw"
    if room.player_1_remaining_time <= 0 and room.player_2_remaining_time <= 0:
        return True, "draw"
    if room.player_1_remaining_time <= 0:
        return True, "black"
    if room.player_2_remaining_time <= 0:
        return True, "white"
    return False, ""

#is_over
@sio.on("move")
async def move(sid, data):
    print(data)
    room = data["room_id"]
    own_remaining_time = data["remaining_time"]
    
    if room is None:
        return Response(True, message="Room not found").to_dict()
    room = rooms_dict[room]
    if room.player_1 == sid:
        room.player_1_remaining_time = own_remaining_time
    else:
        room.player_2_remaining_time = own_remaining_time
    game = room.game
    own_color = PieceColor.WHITE if room.white_id == sid else PieceColor.BLACK
    if game is None:
        return Response(True, message="Game not started").to_dict()
    if game._turn != own_color:
        return Response(True, message="Not your turn").to_dict()

    move = data["move"]
    from_square = move["from"]
    to_square = move["to"]

    moveRs = game.move(CellName(from_square), CellName(to_square), move.get("promotion") if move.get("promotion") is not None else 'q')
    if moveRs is None:
        return Response(True, message="Nước đi không hợp lệ").to_dict()
    
    if game.is_check(PieceColor.WHITE):
        await sio.emit("checked", room=room.id, data={"color": "white"})
        # // kiểm tra có phải chiếu hết không
        #  chỉ kiểm tra khi bị chiếu để tối ưu
        is_over, winner = check_game_over(room)
        if is_over:
            await sio.emit("game_over", room=room.id, data={"winner": winner})
            await sio.emit("stop_game", room=room.id)
    if game.is_check(PieceColor.BLACK):
        await sio.emit("checked", room=room.id, data={"color": "black"})
    is_over, winner = check_game_over(room)
    if is_over:
        await sio.emit("game_over", room=room.id, data={"winner": winner})
        await sio.emit("stop_game", room=room.id)
    else:
        await sio.emit("moved", room=room.id, data={"is_game_over": False, "checked": False, "room": room.to_dict()})
    return Response(False, message="Moved").to_dict()    
    #await sio.emit("moved", room=room.id, data={ "is_game_over": False,"checked": False,"room": room.to_dict()})
    #return Response(False, message="Moved").to_dict()
#chat
#over
@sio.on("stop_game")
async def stop_game(sid, data):
    room_id = data["room_id"]
    await sio.emit("stop_game", room=room_id)
@sio.event
async def checked(sid, data):
    room_id = data["room_id"]
    room = rooms_dict.get(room_id)
    if room is not None:
        await sio.emit("checked", room=room_id, data={"color": data["color"]})

@sio.event
async def game_over(sid, data):
    room_id = data["room_id"]
    room = rooms_dict.get(room_id)
    if room is not None:
        await sio.emit("game_over", room=room_id, data={"winner": data["winner"]})
#over
@sio.event
async def send_message(sid, data):
    room = await sio.get_session(sid)
    room_id = room.get("room_id")
    message = data["message"]
    if room_id is None:
        return
    await sio.emit("receive_message", room=room_id, data={
        "sender": sid,
        "message": message
    })


@sio.on("set_display_name")
async def set_display_name(sid, data):
    session = await sio.get_session(sid)
    session['display_name'] = data["name"]



@sio.on("my_time_out")
async def my_time_out(sid):
    session = await sio.get_session(sid)
    room_id = session.get("room_id")
    print(room_id, "my_time_out")
    if room_id is None:
        return
    room=get_room(room_id)
    sio.emit("game_over", room=room_id, data={
        "winner": room.player_1 if room.player_2 == sid else room.player_2,
        "color": "white" if room.player_1 == sid else "black"
    })

  