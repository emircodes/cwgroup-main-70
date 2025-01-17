<template>
    <nav 
    class="navbar navbar-expand-lg bg-body-tertiary "
    >
        <div class="container-fluid">
            <button class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
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
                <li class="nav-item " id="profile-nav">
                    <button class="nav-link btn btn-secondary " 
                    :class="{'active': activeNav === 'profile' }"
                    @click="goToProfile">
                    My Profile
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link btn btn-secondary position-relative" 
                    :class="{'active': activeNav === 'friends' }"
                    @click="goToFriends">
                    <span v-if="friendReqLength.getLength > 0"
                    class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                        {{ friendReqLength.getLength }}
                        <span class="visually-hidden">unread messages</span>
                    </span>
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
import "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';
import { useAuth } from '../stores/auth';
import { useFriendReqData } from '../stores/getFriendReq';

const friendReqLength = useFriendReqData();
const auth = useAuth();
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
        router.push('/login');
        await axios.post('/api/logout/',{}, {
            headers: {
                'X-CSRFToken': token.value
            }
        });
        
        auth.logout();
    } catch (err) {
        console.error(err);
    }
}
</script>
