import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('userStore', {
  state: () => ({
    similarUsers: [] as Array<{ id: number; username: string; email: string; name: string; similarity_score: number; }>,
  }),
  actions: {
    async fetchSimilarUsers() {
      try {
        const response = await axios.get('/api/similar-users/');
        console.log("API Response in Pinia:", response.data);
        this.similarUsers = response.data;
      } catch (error) {
        console.error("Error fetching similar users:", error);
      }
    },
  },
});
