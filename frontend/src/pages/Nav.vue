<template>
    <nav 
    class="navbar navbar-expand-lg bg-body-tertiary "
    >
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item" >
                    <button class="nav-link active" aria-current="page" 
                    @click="router.push('/')">
                    Home
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link active" aria-current="page" 
                    @click="router.push('profile')">
                    My Profile
                    </button>
                </li>
                <li class="nav-item">
                    <button class="nav-link" @click="router.push('friends')">Friends</button>
                </li>
            </ul>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import FriendReq from './FriendReq.vue';

const router = useRouter();


</script>