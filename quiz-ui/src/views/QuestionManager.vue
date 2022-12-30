<template>
      <h1>Question manager</h1>
      <QuestionDisplayVue :question = "currentQuestion" :total = "totalNumberOfQuestions" @answer-selected = "answerClickedHandler" :key="this.currentQuestionPosition"/>
</template>

<script>

import quizApiService from "@/services/QuizApiService";
import QuestionDisplayVue from "../components/QuestionDisplay.vue";
import ParticipationStorageService from "../services/ParticipationStorageService";

export default {
    data(){
        return {
            currentQuestion : {},
            currentQuestionPosition : 1,
            totalNumberOfQuestions : 1,
            userAnswer : []
        }
    },
    async created(){
        console.log("Composant Question manager 'created'");
        this.totalNumberOfQuestions = ParticipationStorageService.getSize();
        await this.loadQuestionByPosition();
    },
    methods:{
        async loadQuestionByPosition(){
            if (this.currentQuestionPosition <= this.totalNumberOfQuestions){
                try {
                    const question = await quizApiService.getQuestion(this.currentQuestionPosition);
                    this.currentQuestion = question.data;
                }
                catch (error) {
                    console.error(error);
                }
            }
            else {
                await this.endQuiz();
            }
            
        },
        async answerClickedHandler(position){
            this.userAnswer.push(position);
            this.currentQuestionPosition++;
            await this.loadQuestionByPosition();
            console.log(this.userAnswer);
        },
        async endQuiz(){
            const player = ParticipationStorageService.getPlayerName();
            const data = {
                "playerName" : player,
                "answers" : this.userAnswer
            };
            const response = await quizApiService.postParticipation(data);
            ParticipationStorageService.saveParticipationScore(response.data["score"]);
            this.$router.push('/recap');
        }
    },
    components : {
        QuestionDisplayVue
    }
};
</script>

<style>


</style>