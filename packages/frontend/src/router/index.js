import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import LoginView from '../views/LoginView.vue'
import CreateProjectView from '../views/CreateProjectView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/projets',
      name: 'projets',
      component: ProjectsView
    },
    {
      path: '/projets/nouveau',
      name: 'create-project',
      component: CreateProjectView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }
  ]
})

export default router
