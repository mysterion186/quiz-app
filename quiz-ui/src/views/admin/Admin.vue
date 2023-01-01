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
        <div v-if="showErrorMsg">Mot de passe incorrect</div>
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
            showErrorMsg : false,
        }
    },
    methods : {
        async Connect() {
            var response;
            try {
                response = await quizApiService.postLogin({
                    "username" : this.username,
                    "password" : this.password
                });
            }
            catch(error) {
                console.log(error);
            }
            if (response === undefined) {
                console.log("Mot de passe incorrect");
                this.showErrorMsg = true;
            }
            else {
                const token = response.data["token"];
                ParticipationStorageService.saveToken(token);
                ParticipationStorageService.saveDate();
                console.log(token);
                this.$router.push({
                    name : "all-questions"
                });
            }
        }
    }
}
</script>

<style>

</style>