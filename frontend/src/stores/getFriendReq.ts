import { defineStore } from "pinia";
import { ref } from "vue";

export const useFriendReqData = defineStore('useFriendReqData', {
    state: () => ({
        length: ref(),
    }), getters: {
        getLength(state) {
            return state.length
        }
    }, actions: {
        setLength(length: number) {
            this.length = length;
        }
    }
})