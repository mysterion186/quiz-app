<template>
    <br />
    <img  style="width:500px; display:block;margin: 0 auto; height: 300px;" v-if="question.image" :src="question.image" />
    <br />
    <h1>{{this.question.text}} - {{ this.question.position }} / {{ this.total}}</h1>
    <br />
    <!-- <div v-for="answer, index in this.question.possibleAnswers" v-bind:key="answer.id"> -->
      <div class="container">
        <div class="row row-cols-2" >
          <div v-for="answer, index in this.question.possibleAnswers" v-bind:key="answer.id">
          <div class="green_hover" @click="selectedAnswer(index + 1)"  style="border : 1px solid white; height: 70px; display: flex; align-items: center; justify-content: center; text-align: center; width: 610px">{{ answer.text }} </div>
          </div>
        </div>
      <!-- <li @click="selectedAnswer(index + 1)">{{ answer.text }} </li> -->
      </div>
    <br />
</template>

<script>

export default {
  props :{
    question : {
        type : Object
    },
    total : {
      type : String
    }
  },   
  emits : ["answer-selected"],
  data(){
      return {
      }
  },
  methods : {
    selectedAnswer(answerID){
        this.$emit("answer-selected", answerID);
    }
  }
};
</script>

<style>


</style>