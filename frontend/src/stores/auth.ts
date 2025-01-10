import { defineStore} from 'pinia'
import { ref } from 'vue';

export const useAuth = defineStore('useAuth', {
    state: () => ({
        isAuthenticated: false,
        token: ref(),
    }),
    getters: {
        isLoggedIn(state){
            return state.isAuthenticated
        },
        token(state){
            return state.token
        },
    },
    actions: {
        login() {
            // Simulate authentication logic
            this.isAuthenticated = true;
        },
        logout() {
            this.isAuthenticated = false;
        },
        setToken(token: object) {
            this.token = token;
        },
    },
})