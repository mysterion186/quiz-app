import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuiz from '../views/questions/NewQuiz.vue'
import QuestionManager from '../views/questions/QuestionManager.vue'
import Recap from '../views/questions/Recap.vue'
import Admin from '../views/admin/Admin.vue'
import Questions from '../views/admin/Questions.vue'
import AddQuestion from '../views/admin/AddQuestion.vue'
import EditQuestion from '../views/admin/EditQuestion.vue'
import DetailedQuestion from '../views/admin/DetailedQuestion.vue'

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
      component: QuestionManager,
    },
    {
      path: "/recap",
      name: "recap",
      component: Recap,
    },
    {
      path: "/admin",
      name: "admin",
      component: Admin,
    },
    {
      path: "/admin/all-questions",
      name: "all-questions",
      component: Questions,
    },
    {
      path: "/admin/add-question",
      name: "add-question",
      component: AddQuestion,
    },
    {
      path: "/admin/edit-question/:id",
      name: "edit-question",
      component: EditQuestion,
    },
    {
      path: "/admin/question/:id",
      name: "question",
      component: DetailedQuestion,
    },

    // ... autres routes
]
})

export default router
