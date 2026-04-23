import { createRouter, createWebHistory } from 'vue-router'
import login from '../src/login.vue'
import home from '../src/home.vue'
import messageboard from '../src/messageboard.vue'

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
        {
            path: '/messageboard',
            name: 'messageboard',
            component: messageboard,
        },
    ]


})

export default router
