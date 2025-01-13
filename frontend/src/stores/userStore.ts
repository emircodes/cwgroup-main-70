// src/stores/userStore.ts
import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('userStore', {
    state: () => ({
      users: [] as Array<{ id: number; username: string; email: string; name: string }>
    }),
    actions: {
      async fetchUsers() {
        console.log("Fetching users from store...");
        try {
          const response = await axios.get('/api/users/');
          console.log("Store API Response:", response.data);
          this.users = response.data;
          console.log("Users stored in Pinia state:", this.users);
        } catch (error) {
          console.error("Error fetching users in store:", error);
        }
      }
    }
  });
  
