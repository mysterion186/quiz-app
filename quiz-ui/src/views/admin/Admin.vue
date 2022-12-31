<template>
    <form>
        <p>
            <label class="form-label" >Votre identifiant : </label>
            <input v-model="username" type="text" id="username" placeholder="Identifiant" class='form-control'>
            
            <label class="form-label" >Votre mot de passe : </label>
            <input v-model="password" type="password" id="password" placeholder="password" class='form-control'>
        </p> 
        <p>
            <button type="button" @click="Connect" class="btn btn-success">Connexion</button>
        </p>
    </form>
</template>

<script>

import ParticipationStorageService from '../../services/ParticipationStorageService';
import quizApiService from '../../services/QuizApiService';

export default {
    data(){
        return {
            username : "",
            password : "",
            
        }
    },
    methods : {
        async Connect() {
            const response = await quizApiService.postLogin({
                "username" : this.username,
                "password" : this.password
            });
            const token = response.data["token"];
            ParticipationStorageService.saveToken(token);
            console.log(token);
            this.$router.push("admin/all-questions")
        }
    }
}
</script>

<style>

</style>