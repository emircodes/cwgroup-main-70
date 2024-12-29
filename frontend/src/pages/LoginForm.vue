<template>
    <div class="login-container">
      <div class="login-box">
        <h1>LOGIN</h1>
        <form @submit.prevent="login">
          <div class="input-group">
            <input v-model="email" type="email" placeholder="Email" required />
          </div>
          <div class="input-group">
            <input v-model="password" type="password" placeholder="Password" required />
          </div>
          <button type="submit">LOGIN</button>
        </form>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
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

<style scoped>

html, body {
    height: 100%;  
    margin: 0;
    padding: 0;
}

#app {
    height: 100vh;  
}

/* Center the form while keeping the parent's background */
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;  
}

/* Glass effect for the login box */
.login-box {
    background: rgba(255, 255, 255, 0.2);  /* Increase opacity */
    backdrop-filter: blur(20px);  /* Stronger blur for more separation */
    -webkit-backdrop-filter: blur(20px);  
    border: 1px solid rgba(255, 255, 255, 0.4);  
    border-radius: 16px;
    padding: 3rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);  /* Slightly darker shadow */
    width: 100%;
    max-width: 400px;
    text-align: center;
    color: white;  
    margin: 0 auto;
    
}


.input-group input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: none;  
    border-radius: 8px;
    font-size: 1rem;
    background: rgba(255, 255, 255, 0.3);  
    color: #fff;  
    outline: none;
}

.input-group input::placeholder {
    color: rgba(255, 255, 255, 0.7);  
}

button {
    width: 100%;
    padding: 12px;
    background-color: rgba(255, 255, 255, 0.3);  
    color: white;
    font-size: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.4);  
    border-radius: 8px;
    cursor: pointer;
    margin-top: 1rem;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: rgba(255, 255, 255, 0.5);  
}

.error {
    color: #ff7675;  
    margin-top: 1rem;
}

</style>
