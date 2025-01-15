<template>
    <div class="user-list">
      <h2 class="table-heading">Users with Similar Hobbies</h2>
      <table>
        <thead>
          <tr>
            
            <th>Username</th>
            <th>Email</th>
            <th>Name</th>
            <th>Similarity</th> 
            <th>Age</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.similarity_score }}</td>
            <td>{{ user.calculated_age }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted, computed } from 'vue';
  import { useUserStore } from '../stores/userStore';
  
  interface User {
    id: number;
    username: string;
    email: string;
    name: string;
    calculated_age: number;
    similarity_score: number;
  }
  
  const userStore = useUserStore();
  
  onMounted(async () => {
    try {
      if (!userStore.similarUsers.length) {
        await userStore.fetchSimilarUsers();
      }
    } catch (error) {
      console.error("Error fetching similar users:", error);
    }
  });
  
  const users = computed<User[]>(() => userStore.similarUsers);
  </script>

<style scoped>
.user-list {
  margin-top: 10px; /* Adjusts positioning under navigation */
  text-align: center; /* Optional: Centers the content */
}

.table-heading {
  margin-top: 20px; /* Space between navbar and heading */
  font-size: 24px; /* Adjust heading size */
  color: white;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto; /* Centers the table horizontally */
  margin-top: 10px; /* Space under heading */
}

th {
  background-color: #f2f2f2;
  text-align: left;
  color: black; /* Make the text color black for table headers */
  text-align: center;
}

td {
  border: 1px solid #ddd;
  padding: 8px;
  color: white; /* Keep the text color white for table data */
}
</style>
