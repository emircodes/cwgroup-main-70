<template>
<Nav />
<div class="d-flex justify-content-center h-75 align-items-center">
  <div class="card h-75 w-75">
    <div class="card-body ">

      <!--Nav -->
      <ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link position-relative" :class="{active: activeTab === 'home'}" 
          @click="tabActive('home')" id="home-tab" data-bs-toggle="tab" data-bs-target="#home-tab-pane" 
          type="button" role="tab" aria-controls="home-tab-pane" >
            <i class="pi pi-user-edit"></i>
            Edit Profile
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" :class="{active: activeTab === 'profile'}" 
          @click="tabActive('profile')" id="profile-tab" data-bs-toggle="tab" 
          data-bs-target="#profile-tab-pane" type="button" role="tab" aria-controls="profile-tab-pane" >
            <i class="pi pi-face-smile"></i>
            Add Hobbies
          </button>
        </li>
      </ul>
      
    <!--Tabs-->
    <div class="tab-content" id="myTabContent">

      <!-- My Profile -->
      <div class="tab-pane fade" :class="{'show active': activeTab === 'home'}" id="home-tab-pane" role="tabpanel" aria-labelledby="home-tab" tabindex="0">
        <h1>My Profile</h1>
        <form @submit.prevent="updateProfile" novalidate class="col">
          <!--Name-->
          <div class="input-group mb-3">
            <span class="input-group-text" id="basic-addon1">Name</span>
            <input v-model="name" type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
          </div>

          <div class="mb-3">
            <!--Password-->
            <div class="row g-3 align-items-center input-group ">
              <div class="col-auto">
                <span class="input-group-text" id="basic-addon1">Password</span>
              </div>
              <div class="col-auto">
                <input v-model="password" type="password" id="inputPassword6" class="form-control" :class="outlineCSS" aria-describedby="passwordHelpInline">
              </div>
            </div>

            <!--Validate Password-->
            <div class="row g-3 align-items-center input-group">
              <div class="col-auto">
                <span class="input-group-text" id="basic-addon1">Validate Password</span>
              </div>
              <div class="col-auto">
                <input v-model="validatePassword" @change="validator" type="password" id="inputPassword6" class="form-control " :class="outlineCSS" aria-describedby="passwordHelpInline">
              </div>
            
            </div>
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
            <button class="btn btn-primary m-2" type="submit">Save</button>
            <button @click="toHome" class="btn btn-primary m-2" type="button">Back to Home</button>
          </div>
          
        </form>
      </div>
    </div>

    <div class="tab-pane fade" 
    :class="{'show active': activeTab === 'profile'}" 
    id="profile-tab-pane" role="tabpanel" aria-labelledby="profile-tab" 
    tabindex="0">
      <div class="col" >
        <form @submit.prevent="updateHobby">
          <!--add 1 Hobby-->
          <div class="input-group mb-3">
            <button class="btn btn-secondary" type="submit" id="button-addon1">Add Hobby</button>
            <input v-model="hobby" list='datalistOptions' type="text" class="form-control" placeholder="" aria-label="add hobby text" aria-describedby="button-addon1">
            <datalist id="datalistOptions">
              <option v-for="item in selectHobbies" >{{ item.name }}</option>
            </datalist>
          </div>
        </form>

        <div class="card">
          <h1>My Hobbies</h1>

          <form>
            <div class="input-group mb-3" v-for=" item in personalHobbiesNameIdentifier">
              <input type="text" class="form-control" :value='item.name'  readonly >
              <button @click="extractHobbyToDelete(item.id)" type="submit" class="btn btn-danger">Delete</button>            
            </div>
          </form>

        </div>
      </div>
    </div>

      <p v-if="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</div>

  
</template>

<script setup lang="ts">
import { ref, onMounted, toRaw } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Nav from './Nav.vue';

const activeTab = ref('home');
const outlineCSS = ref<'is-valid'| 'is-invalid'>();
const name = ref('');
const email = ref('');
const date_of_birth = ref<string | null>(null);
const message = ref('');
const password = ref<string | null>();
const validatePassword = ref<string | null>();
const personalHobbies = ref([]); 
const personalHobbiesNameIdentifier = ref([]);
const repositoryHobbies = ref([]);
let selectHobbies = ref([]);
const hobby = ref('');
const error = ref('');
const router = useRouter();

function tabActive(tabName: string){
  activeTab.value = tabName;
}

function toHome() {
  router.push('/');
}

function validator() {
  if(password.value !== validatePassword.value) {
    error.value = 'Passwords do not match';
    outlineCSS.value = 'is-invalid';
    password.value = null
  } else {
    outlineCSS.value = 'is-valid'
    error.value = '';
  }
}

// delete hobbies
async function extractHobbyToDelete( item: number) {
  if (item){
    const number = personalHobbies.value.findIndex((x) => x === item)

    if(number != -1){
      await deleteHobby(number);
    }
    
    else{
      error.value = 'No such Hobby is found'
    }
  } else {
    error.value = 'No item selected to delete'
  }
  
}

// extracts personal hobbies from api to name
function personalHobbiesName() {
  personalHobbiesNameIdentifier.value = repositoryHobbies.value.filter((hobby) => personalHobbies.value.includes(hobby.id) === true);
}

// filters personal hobbies and repos 
function filter() {
  selectHobbies.value = repositoryHobbies.value.filter((hobby) => personalHobbies.value.includes(hobby.id) === false);
}

// refresh hobbies repos
async function refreshHobbies() {
  try {
    const response = await axios.get('/api/hobbies');
    repositoryHobbies.value = response.data;
  } catch (err) {
    error.value = 'Failed to refresh hobbies';
  }
}

// Fetch user profile on mount
onMounted(async () => {
  try {
    await refreshHobbies();
    console.log(repositoryHobbies.value)

    const response = await axios.get('/api/profile/', { withCredentials: true });
    name.value = response.data.name;
    email.value = response.data.email;
    date_of_birth.value = (response.data.date_of_birth);
    personalHobbies.value = response.data.hobbies; 
    password.value = response.data.password; // Assuming hobbies are stored in an array in the API response
    console.log(response.data)
    console.log(response.data.hobbies);
    console.log(personalHobbies.value);
    
  } catch (err) {
    error.value = 'Failed to load profile';
  }

  filter();  // Filter out hobbies that are already in the user's list
  personalHobbiesName();
  
});


const deleteHobby = async(item: number) => {
  try {
    personalHobbies.value.splice(item, 1);

    const csrfToken = getCookie('csrftoken');
    await axios.patch('/api/profile/', {
      hobbies: personalHobbies.value,
    }, {
      headers: {
        'X-CSRFToken': csrfToken  // Attach CSRF token
      },
      withCredentials: true  // Include session cookies
    })
    console.log(personalHobbies.value);
    
  } catch (err) {
    console.error(err);
  }
}

// update hobby to hobby api 
const updateHobbyToApiHobby = async() => {
  try {
    const csrfToken = getCookie('csrftoken');
    const res = await axios.post('/api/hobbies/', {
      name: hobby.value,
    }, {
      headers: {
        'X-CSRFToken': csrfToken  // Attach CSRF token
      },
      withCredentials: true  // Include session cookies
    })
  } catch(err) {
    console.error('Failed to add hobby to API:', err);
  }
}

// update hobby to user api profile
const updateHobbyToApiProfile = async() => {
  try {
    const csrfToken = getCookie('csrftoken');
    const matchedHobby = repositoryHobbies.value.find((x) => x.name === hobby.value);
    const hobbyId = matchedHobby.id

    if (matchedHobby) {
      personalHobbies.value.push(hobbyId);
    } else {
      console.error(`Hobby with name "${hobby.value}" not found in repositoryHobbies.`);
    }

    const raw = toRaw(personalHobbies.value)
    console.log(raw);

    console.log("add" + personalHobbies.value);
    await axios.patch('/api/profile/', {
      hobbies: raw,
    }, {
      headers: {
        'X-CSRFToken': csrfToken  // Attach CSRF token
      },
      withCredentials: true  // Include session cookies
    })
  } catch(err) {
    console.error('Failed to add hobby to API:', err);
  }
}

// update hobby from textfield
const updateHobby = async () => {
  try {
    if (repositoryHobbies.value.find((x) => x.name !== hobby.value)){
      const apihobby = await updateHobbyToApiHobby();

      if (!apihobby) {
        message.value = 'Hobby added successfully';
        await refreshHobbies();
        const apiprofile = await updateHobbyToApiProfile();
        if (!apiprofile) {
          message.value = 'Profile updated successfully';
          await refreshHobbies();
          filter();
          personalHobbiesName();

        } else {
          message.value = 'Profile failed to update after adding hobby';
        }
      } else {
        error.value = 'Hobby already exists';
      }
    }
  } catch (err) {
    error.value = 'Failed to add hobby';
  }  
}

// Update profile
const updateProfile = async () => {
  
  try {
    const csrftoken = getCookie('csrftoken');  // Get CSRF token
    await axios.patch('/api/profile/', {
      name: name.value,
      email: email.value,
      date_of_birth: date_of_birth.value,
      password: password.value,
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
