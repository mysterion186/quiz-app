<template>
  
  <h1 style="text-align: center;">Home page</h1>
  <br />
  <br />
  <div style="width:590px; height:300px; margin: 0 auto; overflow:hidden; overflow-y:scroll;" class="">
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date" >
      <div class="container">
        <div class="row row-cols-2">
          <div class="col" style="height: 40px;">{{ scoreEntry.playerName }}</div>
          <div class="col">{{ scoreEntry.score }}</div>
        </div>
      </div>
    </div>
  </div>
  
  <div style="text-align: center; margin-top:25px;">
    <router-link to="/NewQuiz"><button type="button" class="btn btn-success">Démarrer le quiz</button></router-link>
  </div>
  <br />
  
  
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import ParticipationStorageService from "../services/ParticipationStorageService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  async created() {
    console.log("Composant Home page 'created'");
    try {
      const scores = await quizApiService.getQuizInfo();
      this.registeredScores = scores.data['scores'];
      ParticipationStorageService.saveSize(scores.data["size"]);
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<style>

  .row {
    display: flex;
  }

  .col {
    border: 1px solid white;
  }



</style>

