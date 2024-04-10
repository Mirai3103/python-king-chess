from stockfish import Stockfish
st= Stockfish(path="stockfish/windows/stockfish.exe",
                      depth=10,
                      parameters={
                          "Threads": 1, "Minimum Thinking Time": 30
                      }
                      )



st.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
move = st.get_best_move()
print(move)
print(st.get_board_visual())
