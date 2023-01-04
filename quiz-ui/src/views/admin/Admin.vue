<template>
    <h1 style="text-align: center;">Connexion </h1>
    <br />
    <form style="margin: 0 auto">
        <p>
            <label class="form-label" >Votre identifiant : </label>
            <input v-model="username" type="text" id="username" placeholder="Identifiant" class='form-control' style="width: 400px">

            <label class="form-label" style="margin-top: 10px" >Votre mot de passe : </label>
            <input v-model="password" type="password" id="password" placeholder="password" class='form-control' style="width: 400px">
        </p> 
        <p>
            <button type="button" @click="Connect" class="btn btn-success">Connexion</button>
        </p>
        <div v-if="showErrorMsg">Mot de passe incorrect</div>
    </form>
    <br />
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