import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('userStore', {
  state: () => ({
    similarUsers: [] as Array<{ id: number; username: string; email: string; name: string; calculated_age: number; similarity_score: number; }>,
    pagination: { next: null as string | null, previous: null as string | null, count: 0, // Total number of users
    },
  }),
  actions: {
    async fetchSimilarUsers(minAge: number, maxAge: number, url?: string) {
      try {
        const endpoint = url || '/api/similar-users/'; // Default to the main endpoint
        const response = await axios.get(endpoint, {
          params: url ? {} : { min_age: minAge, max_age: maxAge }, // Only send params for the initial request
        });

        // Update state with the response data
        this.similarUsers = response.data.results; // Paginated results
        this.pagination.next = response.data.links.next; // Next page link
        this.pagination.previous = response.data.links.previous; // Previous page link
        this.pagination.count = response.data.count; // Total number of users
      } catch (error) {
        console.error('Failed to fetch similar users:', error);
      }
    },
  },
});