<template>
    <div>
        <div id="turn">
            <span>Turn : {{ turn }}</span>
            <br>
            <span>Game ID : {{ game_id }}</span>
            <br>
            <span>Prop : {{ prop }}</span>
            <br>
            <button @click="leave_game" class="btn btn-outline-danger">Leave Game</button>
        </div>
        <div id="board">
            <div v-for="index in 9" :key="index" :id="index" class="box" :class="{'O' : (mapped_val[index] == 'O'), 'X' : (mapped_val[index] == 'X')}" @click="clickBtn(index)">{{ mapped_val[index] }}</div>
        </div>
        <div id="winner" v-show="winner">
            <span>{{ winner }}</span>
        </div>
        <div id="reset" v-show="winner && prop == 'X'">
            <button @click="resetBoard" class="btn btn-outline-light">Play Again !</button>
        </div>
    </div>
</template>

<script>
    export default {
        name : "TicTacToe",
        props : ["socket", "game_id", "prop"],
        data() {
            return {
                turn : "",
                mapped_val : {},
                winner : "",
            }
        },
        methods : {
            clickBtn(id) {
                if (!this.winner && !this.mapped_val[id]) {
                    if (this.prop == this.turn) {
                        this.$set(this.mapped_val, id, this.turn);
                        this.socket.emit("make_move", this.game_id, this.mapped_val);
                        this.checkWin();
                        this.socket.emit("winner", this.game_id, this.winner);
                    }
                }
            },
            checkWin() {
                let winCombinations = [
                    [1, 2, 3], [4, 5, 6], [7, 8, 9],
                    [1, 4, 7], [2, 5, 8], [3, 6, 9],
                    [1, 5, 9], [3, 5, 7]
                ];

                for (let combination of winCombinations) {
                    let [a, b, c] = combination;
                    if (this.mapped_val[a] && (this.mapped_val[a] == this.mapped_val[b]) && (this.mapped_val[a] == this.mapped_val[c])) {
                        this.winner = this.mapped_val[a] + " Wins !";
                        return;
                    }
                }

                let keys = Object.keys(this.mapped_val)
                if (keys.length == 9) {
                    this.winner = 'Draw !';
                }
            },
            resetBoard() {
                this.socket.emit("reset", this.game_id);
            },
            on_hover(id) {
                if (!this.mapped_val[id]) {
                    document.getElementById(id).innerHTML = this.prop;
                }
            },
            after_hover(id) {
                document.getElementById(id).innerHTML = this.mapped_val[id] || "";
            },
            leave_game() {
                this.socket.emit("leave_game", this.game_id, this.prop);
            }
        },
        created() {
            this.socket.emit("initialize", this.game_id);

            this.socket.on("initialize", (data) => {
                this.mapped_val = data.mapped_val;
                this.turn = data.turn;
            })

            this.socket.on("next_move", (data) => {
                this.mapped_val = data.mapped_val;
                this.turn = data.turn;
            });

            this.socket.on("winner", (winner) => {
                this.winner = winner;
            });

            this.socket.on("reset", () => {
                this.mapped_val = {};
                this.winner = "";
            })
        }
    }
</script>

<style scoped>
    #board {
    max-width: 350px;
    margin: 50px auto 40px auto;
    user-select: none;
    }
    .box {
    display: inline-block;
    width: 100px;
    height: 100px;
    border: 2px solid rgba(137, 43, 226, 0.798);
    margin: 3px;
    text-align: center;
    vertical-align: middle;
    align-content: center;
    cursor: pointer;
    font-size: 50px;
    border-radius: 10px;
    transition: box-shadow 0.3s ease;
    }
    #winner {
    color: green;
    font-size: 50px;
    max-width: fit-content;
    margin: 40px auto 20px auto;
    }
    .X {
    text-shadow: 
        0 0 5px red,
        0 0 10px red,
        0 0 15px darkred;
    }
    .O {
    text-shadow: 
        0 0 5px blue,
        0 0 10px blue,
        0 0 15px darkblue;

    /* text-shadow: 
        0 0 5px green,
        0 0 10px green,
        0 0 15px darkgreen; */
    }
    #turn {
    font-size: 30px;
    max-width: fit-content;
    margin: 100px auto 50px auto;
    color: yellow;
    }
    #reset {
    max-width: fit-content;
    margin: auto;
    }
    .box:hover {
    box-shadow: 
        0 0 5px rgba(137, 43, 226, 0.798),
        0 0 10px rgba(137, 43, 226, 0.798),
        0 0 15px rgba(137, 43, 226, 0.798),
        0 0 20px rgba(137, 43, 226, 0.798);
    }
</style>