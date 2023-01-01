<template>
    <h1>Listes toutes les questions;</h1>
    <div v-for="question in questions" v-bind:key="question.id" @click="Detail(question.id)">
      {{ question.title }} - {{ question.text }} - {{ question.position }}
    </div>
</template>

<script>
import QuizApiService from '../../services/QuizApiService';
import ParticipationStorageService from '../../services/ParticipationStorageService';
export default{
    data() {
        return {
            questions : []
        }
    },
    async created(){
        const check = ParticipationStorageService.checkIsValid();
        if (check){
            const questions = await QuizApiService.getQuestion("all");
            this.questions = questions.data;
        }
        else{
            this.$router.push({
                name : "admin"
            })
        }
    },
    methods : {
        Detail(question) {
            this.$router.push({
                name : "question",
                params : {
                    id : question
                }
            })
        }
    }
}
</script>

<style>

</style>