<template>
  <div>
    <div id="name_form" v-show="name_form">
      <label for="name" class="form-label">Enter Name</label>
      <input id="name" type="text" placeholder="John Doe" v-model="name" class="form-control">
      <br>
      <button @click="play_online" class="btn btn-outline-light">Play Online</button>
      <br><br><br><br>
      <input type="text" class="form-control" placeholder="Enter Game ID here" v-model="game_id">
      <br>
      <div style="float: inline-start;">
        <button @click="create_game" class="btn btn-outline-light">Create</button>
      </div>
      <div style="float: inline-end;">
        <button @click="join_game" class="btn btn-outline-light">Join</button>
      </div>
    </div>
    <div id="game" v-if="game_view">
      <!-- v-show can not be used because it will render the component and its created function will execute before the game_id is generated -->
      <TicTacToe :socket="socket" :game_id="game_id" :prop="prop"></TicTacToe>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';
import TicTacToe from './TicTacToe.vue';

export default {
  name : 'HomePage',
  components : {
    TicTacToe
  },
  data() {
    return {
      name_form : true,
      game_view : false,
      socket : null,
      name : "",
      game_id : "",
      prop : "",
    }
  },
  methods : {
    create_game() {
      if (this.name != "") {
        this.socket.emit("create_game", this.name);
      }
    },
    join_game() {
      if (this.name != "") {
        this.socket.emit("join_game", this.name, this.game_id);
      }
    },
    play_online() {
      if (this.name != "") {
        this.socket.emit("play_online", this.name);
      }
    },
    reload_game() {
      if (this.name != "" && this.game_id != "" && this.prop != "") {
        this.socket.emit("reload_game", this.name, this.game_id, this.prop);
      }
    }
  },
  created() {
    this.socket = io("http://192.168.113.138:5000");
    document.title = "Home - Tic Tac Toe";

    this.name = localStorage.getItem("name") || "";
    this.game_id = localStorage.getItem("game_id") || "";
    this.prop = localStorage.getItem("prop") || "";
    this.reload_game()

    this.socket.on("game_id", (data) => {
      if (data.game_id.length != 4) {
        return;
      }
      this.game_id = data.game_id;
      this.prop = data.prop;
      this.name_form = false;
      this.game_view = true;
      document.title = `Game ${this.game_id} - Tic Tac Toe`;
      localStorage.setItem("name", this.name);
      localStorage.setItem("game_id", this.game_id);
      localStorage.setItem("prop", this.prop);
    });

    this.socket.on("leave_game", () => {
      localStorage.setItem("game_id", "");
      this.game_id = "";
      this.game_view = false;
      this.name_form = true;
    })
  }
}
</script>

<style scoped>
  #name_form {
    max-width: fit-content;
    margin: 100px auto;
  }
</style>