<template>
  <h1>
    {{ this.username }} your score for the game is {{ this.score }} !
  </h1>
  <button type="button" @click="goBack" class="btn btn-success">Retour page d'accueil</button>
</template>
  
  <script>
  import ParticipationStorageService from "@/services/ParticipationStorageService";
  
  export default {
    data() {
      return {
        score:'',
        username : ''
      };
    }, 
    created() {
      this.score = ParticipationStorageService.getParticipationScore();
      this.username = ParticipationStorageService.getPlayerName();
    },
    methods : {
      goBack(){
        console.log("go back ");
        this.$router.push("/");
      }
    }

}

  
  </script>
  
  <style>

  </style>
  