from flask import Flask, session, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from random import randint


app = Flask(__name__)
app.config["SECRET_KEY"] = "a"
CORS(app, origins="*", supports_credentials=True)
io = SocketIO(app, cors_allowed_origins="*")


games = {}


def generate_game_id():
    id = "".join(str(randint(0, 9)) for _ in range(4))
    while id in games.keys():
        return generate_game_id()
    return id


@app.route("/")
def test():
    return jsonify("Test", "Server Running !")


@io.on("connect")
def handle_connect():
    pass


@io.on("disconnect")
def handle_disconnect():
    if session.get("game_id"):
        leave_room(session["game_id"])

        if games[session.get("game_id")]["players"] != 0:
            games[session.get("game_id")]["players"] -= 1
        if games[session.get("game_id")]["players"] == 0:
            del games[session.get("game_id")]


@io.on("play_online")
def play_online(name):
    session["name"] = name
    for game_id in games:
        if games[game_id]["type"] == "online" and games[game_id]["players"] == 1:
            session["game_id"] = str(game_id)
            games[str(game_id)]["players"] += 1
            games[str(game_id)]["O"] = name
            join_room(game_id)
            emit("game_id", {"game_id" : game_id, "prop" : "O"}, to=request.sid)
            return

    game_id = generate_game_id()
    session["game_id"] = game_id
    games[str(game_id)] = {"type" : "online", "players" : 1, "mapped_val" : {}, "winner" : "", "turn" : "X", "X" : name}
    join_room(game_id)
    print(games)
    emit("game_id", {"game_id" : game_id, "prop" : "X"}, to=request.sid)
    return


@io.on("create_game")
def create_game(name):
    session["name"] = name
    game_id = generate_game_id()
    session["game_id"] = game_id

    games[str(game_id)] = {"type" : "room", "players" : 1, "mapped_val" : {}, "winner" : "", "turn" : "X", "X" : name}
    join_room(game_id)
    print(games)
    emit("game_id", {"game_id" : game_id, "prop" : "X"}, to=request.sid)


@io.on("join_game")
def join_game(name, game_id):
    session["name"] = name
    if str(game_id) not in games.keys() or games[str(game_id)]["players"] > 1:
        return

    if games[game_id]["type"] != "room":
        return

    session["game_id"] = str(game_id)
    games[str(game_id)]["players"] += 1
    games[str(game_id)]["O"] = name
    join_room(game_id)

    emit("game_id", {"game_id" : game_id, "prop" : "O"}, to=request.sid)


@io.on("initialize")
def initialize(game_id):
    mapped_val = games[game_id]["mapped_val"]
    turn = games[game_id]["turn"]
    emit("initialize", {"mapped_val" : mapped_val, "turn" : turn}, to=str(game_id))


@io.on("make_move")
def make_move(game_id, mapped_val):
    turn = games[str(game_id)]["turn"]
    if turn == "X":
        turn = "O"
    else:
        turn = "X"

    games[game_id]["mapped_val"] = mapped_val
    games[game_id]["turn"] = turn
    emit("next_move", {"mapped_val" : mapped_val, "turn" : turn}, to=str(game_id))


@io.on("winner")
def win_game(game_id, winner):
    games[game_id]["winner"] = winner
    emit("winner", winner, to=str(game_id))


@io.on("reset")
def reset(game_id):
    games[game_id]["mapped_val"] = {}
    games[game_id]["winner"] = ""
    emit("reset", to=str(game_id))


@io.on("reload_game")
def reload_game(name, game_id, prop):
    if game_id not in games.keys():
        return
    
    if games[game_id][prop] != name:
        return
    
    session["name"] = name
    session["game_id"] = game_id
    join_room(game_id)
    games[game_id]["players"] += 1
    emit("game_id", {"game_id" : game_id, "prop" : prop}, to=request.sid)
    emit("winner", games[game_id]["winner"], to=request.sid)


@io.on("leave_game")
def leave_game(game_id, prop):
    games[game_id][prop] = ""
    games[game_id]["players"] -= 1
    if games[game_id]["players"] == 0:
        del games[game_id]
    leave_room(game_id)
    emit("leave_game", to=request.sid)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")