<template>
  <br />
  <div style="margin-left: 100px; "  >
    <h1 >Inscription</h1>
  </div>

  <br />

  <form>
  <p>
    <label class="form-label" >Nom du joueur : </label>
    <input v-model="username" type="text" id="username" placeholder="Username" class='form-control'>
  </p> 
  <p>
    <button type="button" @click="launchNewQuiz" class="btn btn-success">Envoyer</button>
  </p>
  </form>
  
  <br/>

</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      username:''
    };
  },
  methods:{
    launchNewQuiz(){
      console.log("Launch new quiz with", this.username);
      participationStorageService.savePlayerName( this.username);
      const playerName = participationStorageService.getPlayerName();
      this.$router.push('/questions');
    },
  }

};

</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
