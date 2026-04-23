import { createRouter, createWebHistory } from 'vue-router'
import login from '../src/login.vue'
import home from '../src/home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            name: 'home',
            component: home,
        },
        {
            path: '/login',
            name: 'login',
            component: login,
        },
    ]


})

export default router
