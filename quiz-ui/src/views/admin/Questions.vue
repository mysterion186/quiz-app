<template>
    <h1 style="text-align: center;">Listes toutes les questions :</h1>
    <button type="button" style="margin-right: 10px;" @click="LogOut" class="btn btn-danger">Déconnexion</button>
    <br />

    <div v-for="question in questions" v-bind:key="question.id" @click="Detail(question.id)" style="margin: 0 auto">
        <div class="container green_hover">
            <div class="row row-cols-2" style="height: 60px; ">
            <div class="col" style="text-align: center;width: 50px">{{ question.position }}</div>
            <div class="col" style="text-align: center;width: 600px">{{ question.text }} </div>
            </div>
        </div>
    </div>
    <br />
    <button type="button" @click="Newquestion" class="btn btn-success" style="width: 200px; margin: 0 auto;">Nouvelle question</button>
    <br />
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
        },
        Newquestion(){
            this.$router.push('/admin/add-question');
        },
        LogOut(){
            ParticipationStorageService.logOut();
            this.$router.push({
                name:"HomePage"
            })
        }
    }
}
</script>

<style>

</style>