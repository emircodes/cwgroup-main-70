<template>


  <div class="input-group">
    <ul class="nav nav-pills">
      <li class="nav-item">
        <a class="nav-link active" aria-current="page" @click="goToProfile" >My Profile</a>
      </li>

      <li class="nav-item">
        <a class="nav-link" @click="goToFriendRequest">Friends</a>
      </li>
    </ul>
    
    

  </div>
  
  <!-- User List -->
  <div class="input-group">
    <UserList />
  </div>
  
</template>

<script setup lang="ts">
    import { useRouter } from "vue-router";
    import UserList from "./UserList.vue"

    const router = useRouter();

    const goToProfile = () => {
        router.push("/profile");
    }

    const goToFriendRequest = () => {
      router.push("/friends");
    }

</script>

<style >
.nav {
  margin-bottom: 20px;
}
</style>
