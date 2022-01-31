from stockfish import Stockfish
import time

stockfish = Stockfish(path="C:\\Users\\danie\\OneDrive\\Desktop\\stockfish_14.1_win_x64_popcnt\\stockfish_14.1_win_x64_popcnt.exe", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})
LIST = []

print("Inicio del Juego")
print("")
time.sleep(5)

while True:
    jugada = stockfish.get_best_move()
    print(jugada)
    LIST.append(jugada)
    stockfish.set_position(LIST)
    # time.sleep(1)

    if stockfish.get_evaluation()["type"] == "mate":
        print("Fin del Juego")
        print("Gano el BOT 1")
        time.sleep(5)
        break

    oJugada = stockfish.get_best_move()
    print(oJugada)
    LIST.append(oJugada)
    stockfish.set_position(LIST)
    # time.sleep(1)

    if stockfish.get_evaluation()["type"] == "mate":
        print("Fin del Juego")
        print("Gano el BOT 2")
        time.sleep(5)
        break
