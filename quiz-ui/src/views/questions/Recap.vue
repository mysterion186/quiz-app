<template>
  <h1>
    {{ this.username }} ton score pour le jeu est de : {{ this.score }} !
  </h1>
  <div v-for="question, index in questions" v-bind:key="question.id" @click="Detail(question.id)" style="margin: 0 auto">
    <div class="col" v-bind:style="[answersSummaries[index][1]==='true' ? {'border-color' : 'hsla(160, 100%, 37%, 1)'} : {'border-color' : '#ed1a3a'}]" style="color : white; text-align: center; margin:10px; width: 600px">{{ question.text }} </div>
  </div>
  <br />
  <button type="button" @click="goBack" class="btn btn-success" style="width: 450px; margin: 0 auto;">Retour page d'accueil</button>
  <br />
</template>
  
  <script>
  import ParticipationStorageService from "@/services/ParticipationStorageService";
  import QuizApiService from "@/services/QuizApiService";
  
  export default {
    data() {
      return {
        score:'',
        username : '',
        answersSummaries : [],
        questions : []
      };
    }, 
    async created() {
      this.score = ParticipationStorageService.getParticipationScore();
      this.username = ParticipationStorageService.getPlayerName();
      const temp = ParticipationStorageService.getAnswersSummaries().split(",");
      for (let i = 0; i < temp.length - 1; i = i+2) {
        this.answersSummaries.push([temp[i], temp[i+1]]);
      }
      const questions = await QuizApiService.getQuestion("all");
      this.questions = questions.data;
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
  