<template>
    <h1 style="text-align: center;"> Ajoutez une question ! </h1>
    <form>
        <p>
            <label class="form-label" >Thème de la question </label>
            <input v-model="title" type="text" id="title" placeholder="Thème" class='form-control'>
            
            <label class="form-label" style="margin-top: 10px"  >Intitulé de la question : </label>
            <input v-model="text" type="text" id="text" placeholder="intitulé" class='form-control'>
        </p>    
            <form style="display: flex; justofy-content: space-between;"> 
                <div class="left">            
                    <label class="form-label" style="margin-top: 10px"  >Position dans le quiz : </label>
                    <input v-model.number="position" type="number" id="text" placeholder="Position" class='form-control' style="width: 600px">
                    
                    <label class="form-label" style="margin-top: 10px"  >Réponse 1 :
                        <input v-model="possibleAnswers1Text" type="text" id="text" placeholder="Réponse 1" class='form-control' style="width: 600px">
                        <label for="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox1" 
                            :value="1" 
                            v-model="possibleAnswers1Bool" 
                            :disabled="possibleAnswers2Bool || possibleAnswers3Bool || possibleAnswers4Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
                    
                    <label class="form-label" >Réponse 2 :
                        <input v-model="possibleAnswers2Text" type="text" id="text" placeholder="Réponse 2" class='form-control' style="width: 600px">
                        <label for="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox2" 
                            :value="2" 
                            v-model="possibleAnswers2Bool"
                            :disabled="possibleAnswers1Bool || possibleAnswers3Bool || possibleAnswers4Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
                   
                    
                    <label class="form-label"  >Réponse 3 :
                        <input v-model="possibleAnswers3Text" type="text" id="text" placeholder="Réponse 3" class='form-control' style="width: 600px">
                        <label for="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox3" 
                            :value="3" 
                            v-model="possibleAnswers3Bool"
                            :disabled="possibleAnswers1Bool || possibleAnswers2Bool || possibleAnswers4Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
                    
                    
                    <label class="form-label"  >Réponse 4 :
                        <input v-model="possibleAnswers4Text" type="text" id="text" placeholder="Réponse 4" class='form-control' style="width: 600px">
                        <label for="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox4" 
                            :value="4" 
                            v-model="possibleAnswers4Bool"
                            :disabled="possibleAnswers1Bool || possibleAnswers2Bool || possibleAnswers3Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
            </div> 
            
            <div class="right" style="margin-left: 70px">
                <label class="form-label" >Image pour la question : </label>
                <br />
                <input
                    type="file"
                    accept="image/jpeg/*"
                    @change="convertToBase64($event)"
                />
                <br />
                <div v-if="image !== '' ">
                    <img style="width:500px; display:block;height: 300px; margin-top:10px" v-if="image" :src="image" />
                </div>
                <br />
                <p>
                    <button type="button" @click="Send" class="btn btn-success">Ajouter la question</button>
                </p>
            </div>
        
        </form>
    </form>
    <br />

</template>

<script>

import quizApiService from "@/services/QuizApiService";
import ParticipationStorageService from "@/services/ParticipationStorageService";

export default{
    data() {
        return {
            title: "",
            text: "",
            image: "",
            position : "",
            selected : [],
            possibleAnswers1Text : "",
            possibleAnswers2Text : "",
            possibleAnswers3Text : "",
            possibleAnswers4Text : "",
            possibleAnswers1Bool : false,
            possibleAnswers2Bool : false,
            possibleAnswers3Bool : false,
            possibleAnswers4Bool : false,
        }
    }, 
    created(){
        const check = ParticipationStorageService.checkIsValid();
        if (! check) {
            this.$router.push({
                name : "admin"
            })
        }
    },
    methods : {
        convertToBase64(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                this.image = reader.result;
            };
            reader.onerror = (error) => {
                console.log('Error: ', error);
            };
        },
        async Send(){
            const check = ParticipationStorageService.checkIsValid();
            if (! check) {
                this.$router.push({
                    name : "admin"
                })
            }
            const data = this.CreateData();
            console.log(data);
            const token = ParticipationStorageService.getToken();
            var response = await quizApiService.postAddQuestion(data,token);
            if (response == undefined) {
                this.$router.push("/admin");
            }
            console.log(response);
            this.$router.push({
                name:"all-questions"
            })
        },
        CreateData() {
            var response = {
                "title" : this.title,
                "text" : this.text,
                "position":this.position,
                "image" : this.image,
                "possibleAnswers" : [
                    {
                        "text" : this.possibleAnswers1Text,
                        "isCorrect" : this.possibleAnswers1Bool
                    },
                    {
                        "text" : this.possibleAnswers2Text,
                        "isCorrect" : this.possibleAnswers2Bool
                    },
                    {
                        "text" : this.possibleAnswers3Text,
                        "isCorrect" : this.possibleAnswers3Bool
                    },
                    {
                        "text" : this.possibleAnswers4Text,
                        "isCorrect" : this.possibleAnswers4Bool
                    }
                ]
            };
            return response;
        }
    }
}
</script>

<style>

</style>