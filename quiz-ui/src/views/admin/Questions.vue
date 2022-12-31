<template>
    <h1>Listes toutes les questions;</h1>
    <div v-for="question in questions" v-bind:key="question.id" @click="Detail(question.id)">
      {{ question.title }} - {{ question.text }} - {{ question.position }}
    </div>
</template>

<script>
import QuizApiService from '../../services/QuizApiService';

export default{
    data() {
        return {
            questions : []
        }
    },
    async created(){
        const questions = await QuizApiService.getQuestion("all");
        this.questions = questions.data;
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