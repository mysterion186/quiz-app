<template>
    <h1 style="text-align: center;">Page édition question</h1>
    <button type="button" style="margin-right: 10px;" @click="LogOut" class="btn btn-danger">Déconnexion</button>
    <form>
        <p>
            <label class="form-label" >Thème de la question </label>
            <input v-model="title" type="text" id="title" placeholder="Thème" class='form-control'>
            
            <label class="form-label" style="margin-top: 10px" >Intitulé de la question : </label>
            <input v-model="text" type="text" id="text" placeholder="intitulé" class='form-control'>
            
        </p>    
            <form style="display: flex; justofy-content: space-between;">
                <div class="left">
                    <label class="form-label" style="margin-top: 10px"  >Position dans le quiz : </label>
                    <input v-model.number="position" type="number" id="text" placeholder="Position" class='form-control' style="width: 600px">
                    
                    <label class="form-label" style="margin-top: 10px" >Réponse 1 :
                        <textarea v-model="possibleAnswers1Text" type="text" id="text" placeholder="Réponse 1" class='form-control' style="width: 600px;"></textarea>
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
                        <textarea v-model="possibleAnswers2Text" type="text" id="text" placeholder="Réponse 2" class='form-control' style="width: 600px;"></textarea>
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
                        <textarea v-model="possibleAnswers3Text" type="text" id="text" placeholder="Réponse 3" class='form-control' style="width: 600px;"></textarea>
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
                        <textarea v-model="possibleAnswers4Text" type="text" id="text" placeholder="Réponse 4" class='form-control' style="width: 600px;"></textarea>
                        <label for="checkbox">Bonne réponse : </label>
                        <input 
                            type="checkbox" 
                            id="checkbox4" 
                            :value="4" 
                            v-model="possibleAnswers4Bool"
                            :disabled="possibleAnswers1Bool || possibleAnswers2Bool || possibleAnswers3Bool"
                            
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
                    <div v-if="image !== '' ">
                        <img style="width:500px; display:block;height: 300px; margin-top:10px" v-if="image" :src="image" />
                    </div>
                    <br />
             
                    <p>
                        <router-link to="/admin/all-questions">
                            <button type="button" style="margin-right: 10px;" @click="Update" class="btn btn-danger">Annuler</button>
                        </router-link>
                        <button type="button" @click="Update" class="btn btn-success">Mettre à jour</button>
                    </p>
                </div>
            </form>
        
        
    </form>
    <br />
</template>

<script>
import QuizApiService from '../../services/QuizApiService'; 
import ParticipationStorageService from '../../services/ParticipationStorageService';
export default {   
  data(){
      return {
        question_id: "",
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
  async created() {
    const check = ParticipationStorageService.checkIsValid();
    if (! check) {
        this.$router.push({
            name : "admin"
        })
    }

    this.question_id = this.$route.params.id;
    const response = await QuizApiService.getQuestionById(this.question_id);
    const question = response.data;
    this.title = question.title;
    this.text = question.text;
    this.image = question.image;
    this.position = question.position;
    this.possibleAnswers1Text = question.possibleAnswers[0]["text"];
    this.possibleAnswers1Bool = question.possibleAnswers[0].isCorrect;
    
    this.possibleAnswers2Text = question.possibleAnswers[1]["text"];
    this.possibleAnswers2Bool = question.possibleAnswers[1].isCorrect;
    
    this.possibleAnswers3Text = question.possibleAnswers[2]["text"];
    this.possibleAnswers3Bool = question.possibleAnswers[2].isCorrect;
    
    this.possibleAnswers4Text = question.possibleAnswers[3]["text"];
    this.possibleAnswers4Bool = question.possibleAnswers[3].isCorrect;
  },
  methods : {
    async Update(){
        const check = ParticipationStorageService.checkIsValid();
        if (! check) {
            this.$router.push({
                name : "admin"
            })
        }
        
        const data = this.CreateData();
        console.log(data);
        const token = ParticipationStorageService.getToken();
        var response = await QuizApiService.updateQuestion(this.question_id,data,token);
        if (response === undefined) {
            this.$router.push("/admin");
        }
        else {
            this.$router.push({
                name : "all-questions"
            })
        }
        console.log(response);
    },
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
    },
    LogOut(){
            ParticipationStorageService.logOut();
            this.$router.push({
                name:"HomePage"
            })
        }
  }   
};
</script>

<style>

</style>