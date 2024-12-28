<template>
    <div class="login">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p v-if="error">{{ error }}</p>
    </div>
</template>
  
<script setup lang="ts">
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  const router = useRouter();
  
  const email = ref('');
  const password = ref('');
  const error = ref('');
  
  const login = async () => {
    try {
      const response = await axios.post('/api/login/', {
        email: email.value,
        password: password.value
      });
      localStorage.setItem('token', response.data.token);
      router.push('/profile');
    } catch (err) {
      error.value = 'Invalid credentials';
    }
  };
</script>
  