<template>
    <div class="profile container-fluid row">
      <h1>My Profile</h1>
      <form @submit.prevent="updateProfile" novalidate class="col">
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

      <div class="col" >
        <form @submit.prevent="updateHobbyTextToUserApi">
          <!--add 1 Hobby-->
          <div class="input-group mb-3">
            <button class="btn btn-secondary" type="submit" id="button-addon1">Add Hobby</button>
            <input v-model="hobby" type="text" class="form-control" placeholder="" aria-label="add hobby text" aria-describedby="button-addon1">
          </div>
        </form>
        

        <!--Multiple Hobbies-->
        <div class="input-group mb-3">
          <button class="btn btn-outline-secondary" type="submit">Add Hobby</button>
          <select class="form-select" id="inputGroupSelect03" aria-label="select hobby with button">
            <option selected>Choose...</option>
            <option v-for="item in selectHobbies" :key="hobby" >{{ item }}</option>
          </select>
        </div>

        <div class="card">
          <h1>My Hobbies</h1>
          <ul class="list-group">
            <li class="list-group-item" v-for="item in personalHobbies" >{{ item }}</li>
          </ul>
        </div>
      </div>

      <p v-if="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const name = ref('');
  const email = ref('');
  const date_of_birth = ref<string | null>(null);
  const message = ref('');
  const personalHobbies = ref([]); 
  const repositoryHobbies = ref([]);
  let selectHobbies = ref([]);
  const hobby = ref('');
  const error = ref('');




  // Fetch user profile on mount
  onMounted(async () => {
    try {
      const reHobby = await axios.get('/api/hobbies');
      repositoryHobbies.value = reHobby.data;
      console.log(reHobby.data)

      const response = await axios.get('/api/profile/', { withCredentials: true });
      name.value = response.data.name;
      email.value = response.data.email;
      date_of_birth.value = (response.data.date_of_birth);
      personalHobbies.value = response.data.hobbies;  // Assuming hobbies are stored in an array in the API response
      console.log(response.data)
      console.log(response.data.hobbies);
      
    } catch (err) {
      error.value = 'Failed to load profile';
    }


  });
  
  function selectHobby(){
    console.log(personalHobbies);
    console.log(repositoryHobbies);
    selectHobbies.value = [];
    console.log(selectHobbies);
  }
  // Update profile
  const updateProfile = async () => {
    try {
      const csrftoken = getCookie('csrftoken');  // Get CSRF token
      await axios.patch('/api/profile/', {
        name: name.value,
        email: email.value,
        date_of_birth: date_of_birth.value,
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
  
  // updates hobby
  const updateHobbyTextToHobbyApi = async () => {
    try {
      console.log(personalHobbies.value);
      
      const csrftoken = getCookie('csrftoken');  // Get CSRF token
      await axios.post('/api/hobbies/', {
        name: hobby.value,
      }, {
        headers: {
          'X-CSRFToken': csrftoken  // Attach CSRF token
        },
        withCredentials: true  // Include session cookies
      });
      message.value = 'Profile updated successfully';
    } catch (err) {
      error.value = String(err);
      error.value = 'Failed to add hobby';
    }
  };

  const updateHobbyTextToUserApi = async () => {
    try {
      const csrftoken = getCookie('csrftoken');  // Get CSRF token
      await axios.patch('/api/profile/', {
        hobbies: [1,2],
      }, {
        headers: {
          'X-CSRFToken': csrftoken  // Attach CSRF token
        },
        withCredentials: true  // Include session cookies
      });
      message.value = 'Profile updated successfully';
    } catch (err) {
      error.value = String(err);
      error.value = 'Failed to add hobby';
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
  