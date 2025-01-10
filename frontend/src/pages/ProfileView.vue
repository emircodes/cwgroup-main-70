<template>
    <div class="profile">
      <h1>Profile</h1>
      <form @submit="updateProfile">
        <div>
          <div>
            <label for="name">Name:</label>
          </div>
          <input v-model="name" type="text" placeholder="Name" required />
        </div>
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="date_of_birth" type="date" />
        <button type="submit">Save</button>
      </form>
      <p v-if="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const name = ref('');
  const email = ref('');
  const date_of_birth = ref('');
  const message = ref('');
  const error = ref('');
  
  // Fetch user profile on mount
  onMounted(async () => {
    try {
      const response = await axios.get('/api/profile/', { withCredentials: true });
      name.value = response.data.name;
      email.value = response.data.email;
      date_of_birth.value = response.data.date_of_birth;
    } catch (err) {
      error.value = 'Failed to load profile';
    }
  });
  
  // Update profile
  const updateProfile = async () => {
    try {
      const csrftoken = getCookie('csrftoken');  // Get CSRF token
      await axios.patch('/api/profile/', {
        name: name.value,
        email: email.value,
        date_of_birth: date_of_birth.value
      }, {
        headers: {
          'X-CSRFToken': csrftoken  // Attach CSRF token
        },
        withCredentials: true  // Include session cookies
      });
      message.value = 'Profile updated successfully';
    } catch (err) {
      error.value = 'Failed to update profile';
    }
  };
  
  // Get CSRF token from cookies
  function getCookie(name: string | any[]) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  </script>
  
  <style scoped>
  .error {
    color: red;
  }
  </style>
  