<template>
    <img v-if="question.image" :src="question.image" />
    <br />
    <h1>{{this.question.text}} - {{ this.question.position }} / {{ this.total}}</h1>
    <br />
    <div v-for="answer, index in this.question.possibleAnswers" v-bind:key="answer.id">
      <li @click="selectedAnswer(index + 1)">{{ answer.text }} </li>
    </div>
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