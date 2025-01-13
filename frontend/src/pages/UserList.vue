<template>
    <div class="user-list">
      <h2 class="table-heading">User List</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Name</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.name }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted, computed } from 'vue';
  import { useUserStore } from '../stores/userStore';
  
  // Define the User interface to enforce static typing
  interface User {
    id: number;
    username: string;
    email: string;
    name: string;
  }
  
  // Initialize the Pinia store for user data
  const userStore = useUserStore();
  
  // Fetch users when the component is mounted
  onMounted(async () => {
    if (!userStore.users.length) {
      console.log("Fetching users...");
      await userStore.fetchUsers();
    }
  });
  
  // Create a computed property to bind users from the store
  const users = computed<User[]>(() => userStore.users);
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
  }
  
  td {
    border: 1px solid #ddd;
    padding: 8px;
    color: white; /* Keep the text color white for table data */
  }
  </style>
  