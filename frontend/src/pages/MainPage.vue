<template>

  <Nav />

  <!-- User List -->
  <div class="input-group">
    <UserList />
  </div>
  
</template>

<script setup lang="ts">
    import { useRouter } from "vue-router";
    import UserList from "./UserList.vue"
import Nav from "./Nav.vue";

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
