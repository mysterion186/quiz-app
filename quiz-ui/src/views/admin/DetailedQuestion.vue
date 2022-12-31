<template>
    <img v-if="question.image" :src="question.image" />
    <br />
    <h1>{{this.question.text}} - {{ this.question.position }} / {{ this.total}}</h1>
    <br />
    <div v-for="answer, index in this.question.possibleAnswers" v-bind:key="answer.id">
      <li>{{ answer.text }} </li>
    </div>
    <button type="button" @click="Delete" class="btn btn-success">Supprimer la question</button>
    <button type="button" @click="Update" class="btn btn-success">Modifier la question</button>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import ParticipationStorageService from "../../services/ParticipationStorageService";

export default {  
  data(){
      return {
        question : {},
        question_id : "",
      }
  },
  async created() {
    this.question_id = this.$route.params.id;
    const response = await quizApiService.getQuestionById(this.question_id);
    this.question = response.data;
  },
  methods : {
    async Delete(){
        const user_token = ParticipationStorageService.getToken();
        var response;
        try {
            response = await quizApiService.deleteQuestion(this.question_id,user_token);
        }
        catch(error) {
            console.log(error);
        }
        // console.log(response);
        if (response === undefined) {
            this.$router.push("/admin");
        }
        else {
            this.$router.push("/admin/all-questions")
        }
    },
    Update(){
        this.$router.push({
            name : "edit-question",
            params : {
                id : this.question_id
            }
        })
    }
  }
};
</script>

<style>

</style>