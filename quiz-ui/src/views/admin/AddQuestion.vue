<template>
    <h1 style="text-align: center;"> Ajoutez une question ! </h1>
    <button type="button" style="margin-right: 10px;" @click="LogOut" class="btn btn-danger">Déconnexion</button>
    <div v-if="showErrorMsg" style="font-size: 16px; color: red"> Remplissez les champs manquants : {{ missingParams }}</div>
    <form>
        <p>
            <label class="form-label" >Thème de la question </label>
            <input v-model="title" type="text" id="title" placeholder="Thème" class='form-control' required >
            
            <label class="form-label" style="margin-top: 10px"  >Intitulé de la question : </label>
            <input v-model="text" type="text" id="text" placeholder="intitulé" class='form-control'>
        </p>    
            <form style="display: flex; justify-content: space-between;"> 
                <div class="left">            
                    <label class="form-label" style="margin-top: 10px"  >Position dans le quiz : </label>
                    <input v-model.number="position" type="number" id="position" placeholder="Position" class='form-control' style="width: 600px" required>
                    <label class="form-label" style="margin-top: 10px"  >Réponse 1 :
                        <textarea v-model="possibleAnswers1Text" type="text" id="possibleAnswers" placeholder="Réponse 1" class='form-control' style="width: 600px" required></textarea>
                        <label for="checkbox" id="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox" 
                            :value="1" 
                            v-model="possibleAnswers1Bool" 
                            :disabled="possibleAnswers2Bool || possibleAnswers3Bool || possibleAnswers4Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
                    
                    <label class="form-label" >Réponse 2 :
                        <textarea v-model="possibleAnswers2Text" type="text" id="possibleAnswers" placeholder="Réponse 2" class='form-control' style="width: 600px" required></textarea>
                        <label for="checkbox" id="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox" 
                            :value="2" 
                            v-model="possibleAnswers2Bool"
                            :disabled="possibleAnswers1Bool || possibleAnswers3Bool || possibleAnswers4Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
                   
                    
                    <label class="form-label"  >Réponse 3 :
                        <textarea v-model="possibleAnswers3Text" type="text" id="possibleAnswers" placeholder="Réponse 3" class='form-control' style="width: 600px" required></textarea>
                        <label for="checkbox" id="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox" 
                            :value="3" 
                            v-model="possibleAnswers3Bool"
                            :disabled="possibleAnswers1Bool || possibleAnswers2Bool || possibleAnswers4Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
                    
                    
                    <label class="form-label"  >Réponse 4 :
                        <textarea v-model="possibleAnswers4Text" type="text" id="possibleAnswers" placeholder="Réponse 4" class='form-control' style="width: 600px" required></textarea>
                        <label for="checkbox" id="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox" 
                            :value="4" 
                            v-model="possibleAnswers4Bool"
                            :disabled="possibleAnswers1Bool || possibleAnswers2Bool || possibleAnswers3Bool"
                            style="margin-left: 4px;"
                        >
                    </label>
            </div> 
            
            <div class="right" style="margin-right: 70px">
                <label class="form-label" >Image pour la question : </label>
                <br />
                <input
                    type="file"
                    id="image"
                    accept="image/jpeg/*"
                    @change="convertToBase64($event)"
                />
                <br />
                <div v-if="image !== '' ">
                    <img style="width:500px; display:block;height: 300px; margin-top:10px" v-if="image" :src="image" />
                </div>
                <br />
                <p>
                    <router-link to="/admin/all-questions">
                        <button type="button" style="margin-right: 10px;" @click="Update" class="btn btn-danger">Annuler</button>
                    </router-link>
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
            showErrorMsg : false,
            missingParams : "",
            missingParamsArry : [],
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
            const token = ParticipationStorageService.getToken();
            var response = await quizApiService.postAddQuestion(data,token);
            console.log(response);
            var status = response.status;
            console.log("status = ", status === 422, status === 200);
            if (status === 422){
                const required_params = ["title","text","image","position","possibleAnswers","Au moins une bonne réponse !"]; 
                required_params.forEach(element => {
                    if (element === "Au moins une bonne réponse !"){
                        const elt_array = document.querySelectorAll("#checkbox");
                        elt_array.forEach(elt => { 
                            console.log(elt.style.border)
                            if (elt.style.border){
                                elt.style.removeProperty("border");
                            }
                        })
                    }
                    else {
                        const elt_array = document.querySelectorAll("#"+element);
                        elt_array.forEach(elt => { 
                            console.log(elt.style.border)
                            if (elt.style.border){
                                elt.style.removeProperty("border");
                            }
                        })
                    }
                })
                this.showErrorMsg = true;
                this.missingParamsArry = response.data["missing_params"];
                console.log(this.missingParamsArry);
                response.data["missing_params"].forEach(element => {
                    if (element === "Au moins une bonne réponse !"){
                        const elt_array = document.querySelectorAll("#checkbox");
                        elt_array.forEach(elt => {
                            elt.style.border = "5px solid red"
                        })
                    }
                    else {
                        const elt_array = document.querySelectorAll("#"+element);
                        elt_array.forEach(elt => {
                            elt.style.border = "5px solid red"
                        })
                    }
                });
                this.missingParams = response.data["missing_params"].join();
                console.log("Il manque les données : ", this.missingParams);
            }
            else if (status === 200) {
                console.log("tout est bon");
                this.$router.push({
                        name : "all-questions"
                    });
                }
            else{
                console.log("error admin");
                this.$router.push("/admin");
            }
        },
        CreateData() {
            var response = {
                "title" : this.title,
                "text" : this.text,
                "position": this.position,
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