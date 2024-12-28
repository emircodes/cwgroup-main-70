<template>
    <div class="register">
      <h1>Register</h1>
      <form @submit.prevent="register">
        <input v-model="name" type="text" placeholder="Name" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
      <p v-if="error">{{ error }}</p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const name = ref('');
  const email = ref('');
  const password = ref('');
  const error = ref('');
  
  const register = async () => {
    try {
      await axios.post('/api/register/', {
        name: name.value,
        email: email.value,
        password: password.value
      });
      router.push('/login');
    } catch (err) {
      error.value = 'Registration failed';
    }
  };
  </script>
  