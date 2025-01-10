import { defineStore} from 'pinia'

export const useAuth = defineStore('useAuth', {
    state: () => ({
        isAuthenticated: false,
    }),
    getters: {
        isLoggedIn(state){
            return state.isAuthenticated
        }
    },
    actions: {
        login() {
            // Simulate authentication logic
            this.isAuthenticated = true;
        },
        logout() {
            this.isAuthenticated = false;
        },
    },
})