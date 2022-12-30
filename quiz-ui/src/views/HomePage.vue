<template>
  <h1>Home page</h1>
  <ul>
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>
  </ul>
  <router-link to="/NewQuiz">Démarrer le quiz !</router-link>
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
