<template>
    <div style="display: flex; flex-direction: row; justify-content: center; margin-top: 20px;">
      <button type="button" style="margin-right: 10px;" @click="this.$router.go(-1)" class="btn btn-info">Revenir en arrière</button>
        <button type="button" style="margin-right: 10px;" @click="LogOut" class="btn btn-danger">Déconnexion</button>
    </div>
    <br/>
    <img style="width:500px; display:block;margin: 0 auto; height: 300px;"  v-if="question.image" :src="question.image" />
    <br />
    <h1>{{this.question.text}} - {{ this.question.position }} / {{ this.total}}</h1>
    <br />
    <div class="container">
      <div class="row row-cols-2" >
        <div v-for="answer, index in this.question.possibleAnswers" v-bind:key="answer.id">
        <div style="border: 1px solid white; height: 70px; display: flex; align-items: center; justify-content: center; text-align: center; width: 610px">{{ answer.text }} </div>
        </div>
      </div>
    </div>
    <br />
    <div class="container">
      <div class="row row-cols-2" style="justify-content: center; margin-left: 12px;" >
        <button type="button" @click="Delete" class="btn btn-success" style="width: 300px; margin-right: 10px;" >Supprimer la question</button>
        <button type="button" @click="Update" class="btn btn-success" style="width: 300px; ">Modifier la question</button>
      </div>
    </div>
    <br />
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
    const check = ParticipationStorageService.checkIsValid();
    console.log("Depuis created ",check);
    if (! check) {
        this.$router.push({
            name : "admin"
        })
    }
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
        // if (response === undefined) {
        //     this.$router.push("/admin");
        // }
        // else {
        //     this.$router.push("/admin/all-questions")
        // }
        this.$router.push("/admin/all-questions");
    },
    Update(){
      const check = ParticipationStorageService.checkIsValid();
      if (! check) {
          this.$router.push({
              name : "admin"
          })
      }

        this.$router.push({
            name : "edit-question",
            params : {
                id : this.question_id
            }
        })
    },
    LogOut(){
            ParticipationStorageService.logOut();
            this.$router.push({
                name:"HomePage"
            })
        }
  }
};
</script>

<style>

</style>