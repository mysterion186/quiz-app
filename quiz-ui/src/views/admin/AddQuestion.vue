<template>
    Ajoutez une question ! 
    <form>
        <p>
            <label class="form-label" >Thème de la question </label>
            <input v-model="title" type="text" id="title" placeholder="Thème" class='form-control'>
            
            <label class="form-label" >Intitulé de la question : </label>
            <input v-model="text" type="text" id="text" placeholder="intitulé" class='form-control'>
            
            <label class="form-label" >Position dans le quiz : </label>
            <input v-model.number="position" type="number" id="text" placeholder="Position" class='form-control'>
            
            <label class="form-label" >Réponse 1 :
                <input v-model="possibleAnswers1Text" type="text" id="text" placeholder="Réponse 1" class='form-control'>
                <label for="checkbox">Bonne réponse : </label>
                <input 
                    type="checkbox" 
                    id="checkbox1" 
                    :value="1" 
                    v-model="possibleAnswers1Bool" 
                    :disabled="possibleAnswers2Bool || possibleAnswers3Bool || possibleAnswers4Bool"
                >
            </label>
            <br />
            
            <label class="form-label" >Réponse 2 :
                <input v-model="possibleAnswers2Text" type="text" id="text" placeholder="Réponse 2" class='form-control'>
                <label for="checkbox">Bonne réponse : </label>
                <input 
                    type="checkbox" 
                    id="checkbox2" 
                    :value="2" 
                    v-model="possibleAnswers2Bool"
                    :disabled="possibleAnswers1Bool || possibleAnswers3Bool || possibleAnswers4Bool"
                >
            </label>
            <br />
            
            <label class="form-label" >Réponse 3 :
                <input v-model="possibleAnswers3Text" type="text" id="text" placeholder="Réponse 3" class='form-control'>
                <label for="checkbox">Bonne réponse : </label>
                <input 
                    type="checkbox" 
                    id="checkbox3" 
                    :value="3" 
                    v-model="possibleAnswers3Bool"
                    :disabled="possibleAnswers1Bool || possibleAnswers2Bool || possibleAnswers4Bool"
                >
            </label>
            <br />
            
            <label class="form-label" >Réponse 4 :
                <input v-model="possibleAnswers4Text" type="text" id="text" placeholder="Réponse 4" class='form-control'>
                <label for="checkbox">Bonne réponse : </label>
                <input 
                    type="checkbox" 
                    id="checkbox4" 
                    :value="4" 
                    v-model="possibleAnswers4Bool"
                    :disabled="possibleAnswers1Bool || possibleAnswers2Bool || possibleAnswers3Bool"
                >
            </label>
            <br />
            
            <label class="form-label" >Image pour la question : </label>
            <br />
            <input
                type="file"
                accept="image/jpeg/*"
                @change="convertToBase64($event)"
            />
        </p> 
        <p>
            <button type="button" @click="Send" class="btn btn-success">Ajouter la question</button>
        </p>
    </form>
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