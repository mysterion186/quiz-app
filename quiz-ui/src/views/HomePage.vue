<template>
  
  <h1 style="text-align: center;">Home page</h1>
  <br />
  <div style="text-align: center;">
    <router-link to="/NewQuiz">Démarrer le quiz !</router-link>
  </div>
  <br />
  <ul style="width:590px; margin: 0 auto;">
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date" >
      <div class="container">
        <div class="row row-cols-2">
          <div class="col" style="height: 40px;">{{ scoreEntry.playerName }}</div>
          <div class="col">{{ scoreEntry.score }}</div>
        </div>
      </div>
    </div>
  </ul>
  
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

