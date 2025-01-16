import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('userStore', {
  state: () => ({
    similarUsers: [] as Array<{ id: number; username: string; email: string; name: string; calculated_age: number; similarity_score: number; }>,
  }),
  actions: {
    async fetchSimilarUsers(minAge : number, maxAge : number) {
      try {
        const response = await axios.get('/api/similar-users/', {
          params: {
            min_age: minAge,
            max_age: maxAge,
          },
        });
        this.similarUsers = response.data;
      } catch (error) {
        console.error('Failed to fetch similar users:', error);
      }
    },
  },
});

