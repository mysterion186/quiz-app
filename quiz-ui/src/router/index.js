import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuiz from '../views/NewQuiz.vue'
import questions from '../views/questions.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/NewQuiz",
      name: "NewQuiz",
      component: NewQuiz,
    },
    {
      path: "/questions",
      name: "questions",
      component: questions,
    },
    // ... autres routes
]
})

export default router
