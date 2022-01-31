from stockfish import Stockfish
import time

stockfish = Stockfish(path="C:\\Users\\danie\\OneDrive\\Desktop\\stockfish_14.1_win_x64_popcnt\\stockfish_14.1_win_x64_popcnt.exe", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})
LIST = []
JUGADAS_INCORRECTAS = 0
TERMINADO = False

while True:
    if TERMINADO == True:
        break
    jugada = input("Jugada: ")
    if jugada == "end":
        LIST.clear
        print("FIN")
        break
    else:
        if stockfish.is_move_correct(jugada):
            LIST.append(jugada)
            stockfish.set_position(LIST)

            oJugada = stockfish.get_best_move()
            print(oJugada)
            LIST.append(oJugada)
            stockfish.set_position(LIST)

            # print(stockfish.get_board_visual()) Para ver el tablero
            print(stockfish.get_evaluation()["type"])
        else:
            print("Jugada incorrecta")
            JUGADAS_INCORRECTAS = JUGADAS_INCORRECTAS + 1
            if JUGADAS_INCORRECTAS == 3:
                print("3 Jugadas incorrectas")
                TERMINADO = True
                time.sleep(2)