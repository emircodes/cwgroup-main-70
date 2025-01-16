<template>
    <nav 
    class="navbar navbar-expand-lg bg-body-tertiary "
    >
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ">
                <li class="nav-item" >
                    <button class="nav-link btn btn-secondary" aria-current="page" 
                    :class="{'active': activeNav === 'home' }"
                    @click="goToHome">
                    Home
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link btn btn-secondary" 
                    :class="{'active': activeNav === 'profile' }"
                    @click="goToProfile">
                    My Profile
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link btn btn-secondary" 
                    :class="{'active': activeNav === 'friends' }"
                    @click="goToFriends">
                    Friends
                    </button>
                </li>

                
            </ul>

            <!--Logout-->
            <div class="nav-item ms-auto">
                <button class="nav-link btn btn-secondary" 
                :class="{'active': activeNav === 'logout' }"
                @click="logout">
                <i class="pi pi-sign-out"></i>
                Logout
                </button>
            </div>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';

const router = useRouter();
const activeNav = ref('');
const token = ref('');

function goToHome() {
    router.push('/');
    activeNav.value = 'home';
}

function goToFriends() {
    router.push('friends');
    activeNav.value = 'friends';
}

function goToProfile() {
    router.push('profile');
    activeNav.value = 'profile';
}

async function fetchToken() {
  try {
    const res = await axios.get('/api/get-token/');
    token.value = res.data.token;
  } catch (error) {
    console.error(error);
  }
}

async function logout() {
    try {
        await fetchToken();
        
        await axios.post('/api/logout/',{}, {
            headers: {
                'X-CSRFToken': token.value
            }
        });
        router.push('/login');
    } catch (err) {
        console.error(err);
    }
}
</script>