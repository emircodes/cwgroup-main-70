import { defineStore } from "pinia";
import { ref } from "vue";
export const usePersonal = defineStore('usePersonal', {
    state: () => ({
        id: ref(),
    }),
    getters: {
        getUserID(state){
            return this.id
        }
    },
    actions: {
        setUserID(id: string) {
            this.id = id;
        },
        getUserID(){
            return this.id;
        }
    }
})