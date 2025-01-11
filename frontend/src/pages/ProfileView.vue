<template>
    <div class="profile">
      <h1>Profile</h1>
      <form @submit.prevent="updateProfile" novalidate>
        <!--Name-->
        <div class="input-group mb-3">
          <span class="input-group-text" id="basic-addon1">Name</span>
          <input v-model="name" type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
        </div>

        <!--Email-->
        <div class="input-group mb-3">
          <span class="input-group-text" id="basic-addon1">Email</span>
          <input v-model="email" type="email" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
        </div>

        <!--Date of Birth-->
        <div class="input-group mb-3">
          <span class="input-group-text" id="basic-addon1">Date of Birth</span>
          <input v-model="date_of_birth" type="date" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
        </div>

        <!--Save button-->
        <div class="input-group mb-3">
          <button class="btn btn-primary" type="submit">Save</button>
        </div>
        
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
  const date_of_birth = ref<string | null>(null);;
  const message = ref('');
  const error = ref('');


  const formatDate = (date: string | null): string | null => {
    if (!date) return null;
    const d = new Date(date);
    if (isNaN(d.getTime())) return null; // Handle invalid dates
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
  // Fetch user profile on mount
  onMounted(async () => {
    try {
      const response = await axios.get('/api/profile/', { withCredentials: true });
      name.value = response.data.name;
      email.value = response.data.email;
      date_of_birth.value = formatDate(response.data.date_of_birth);
      console.log(response.data)
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
  