import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('userStore', {
  state: () => ({
    similarUsers: [] as Array<{ id: number; username: string; email: string; name: string; calculated_age: number; similarity_score: number; }>,
    pagination: { next: null as string | null, previous: null as string | null, count: 0, // Total number of users
    },
  }),
  actions: {
    async fetchSimilarUsers(minAge: number, maxAge: number, url?: string ) {
      try {
        let endpoint = url || '/api/similar-users/';
        
        const response = await axios.get(endpoint, {
          withCredentials: true,
          // Only send `min_age` & `max_age` as query params on the *first* call
          params: url ? {} : { min_age: minAge, max_age: maxAge },
        });

        // Update state with the response data
        this.similarUsers = response.data.results;       // Paginated results
        this.pagination.next = response.data.links.next; // Next page link (full URL)
        this.pagination.previous = response.data.links.previous; // Previous page link (full URL)
        this.pagination.count = response.data.count;     // Total number of users
      } catch (error) {
        console.error('Failed to fetch similar users:', error);
      }
    },
    
  },
});