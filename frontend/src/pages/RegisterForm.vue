<template>
    <div class="register-container">
      <div class="register-box">
        <h3>REGISTER</h3>
        <form @submit.prevent="register">
          <div class="input-group">
            <input v-model="name" type="text" placeholder="Name" required />
          </div>
          <div class="input-group">
            <input v-model="email" type="email" placeholder="Email" required />
          </div>
          <div class="input-group">
            <input v-model="password" type="password" placeholder="Password" required />
          </div>
          <button type="submit">REGISTER</button>
          <h5 class="redirect-text">Already have an account? <router-link to="/login">Login</router-link></h5>
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

<style scoped>

html, body {
    height: 100%;  
    margin: 0;
    padding: 0;
}

#app {
    height: 100vh;  
}


.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;  
}

/* Glass effect */
.register-box {
    background: rgba(255, 255, 255, 0.2);  
    backdrop-filter: blur(20px);  
    -webkit-backdrop-filter: blur(20px);  
    border: 1px solid rgba(255, 255, 255, 0.4);  
    border-radius: 16px;
    padding: 3rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);  
    width: 100%;
    max-width: 400px;
    text-align: center;
    color: white;  
    margin: 0 auto;
    margin-bottom: 2.5rem;
}

.redirect-text {
    margin-top: 1rem;
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
