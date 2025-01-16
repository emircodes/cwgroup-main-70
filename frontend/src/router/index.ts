// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'
// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';

import LoginForm from '../pages/LoginForm.vue';
import RegisterForm from '../pages/RegisterForm.vue';
import ProfileView from '../pages/ProfileView.vue';
import UserList from '../pages/UserList.vue';
import {useAuth} from '../stores/auth.ts'
import FriendReq from '../pages/FriendReq.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''


// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { 
            path: '/', name: 'Main Page', component: MainPage, 
            meta: {requiresAuth: true}
        },
        { path: '/other/', name: 'Other Page', component: OtherPage },
        { path: '/login', component: LoginForm },
        { path: '/register', component: RegisterForm },
        { path: '/profile', component: ProfileView, 
            meta: {requiresAuth: true}},
        { path: '/friends', component: FriendReq, meta: {requiresAuth: true}},
        { path: '/users', name: 'User List', component: UserList, 
            meta: {requiresAuth: true}},

        // Wildcard route to catch all routes not explicitly defined
        { path: '/:pathMatch(.*)*', redirect: '/' },
        {
            path: '/:catchAll(.*)', // Handle all undefined routes
            redirect: '/',
        },
    ]
})

router.beforeEach((to, from, next) => {
    const auth = useAuth()

    if(to.meta.requiresAuth && !auth.isLoggedIn) {
        next ({
            path: '/login/',
            query: { redirect: to.fullPath }
        })
    }
    else if (!auth.isLoggedIn && from.meta.requiresAuth) {
        next('/login'); // Redirect to login if navigating back to protected pages
    } 
    else {
        next();
    }
})

export default router
