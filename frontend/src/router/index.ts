// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';

import LoginForm from '../pages/LoginForm.vue';
import RegisterForm from '../pages/RegisterForm.vue';
import ProfileView from '../pages/ProfileView.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Main Page', component: MainPage },
        { path: '/other/', name: 'Other Page', component: OtherPage },
        { path: '/login', component: LoginForm },
        { path: '/register', component: RegisterForm },
        { path: '/profile', component: ProfileView }
    ]
})

export default router
