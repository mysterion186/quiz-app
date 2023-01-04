<template>
  <h1>
    {{ this.username }} ton score pour le jeu est de : {{ this.score }} !
  </h1>
  <br />
  <button type="button" @click="goBack" class="btn btn-success" style="width: 450px; margin: 0 auto;">Retour page d'accueil</button>
  <br />
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
  