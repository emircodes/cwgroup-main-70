<template>


  <div class="input-group">
    <ul class="nav nav-pills">
      <li class="nav-item">
        <a class="nav-link active" aria-current="page" @click="goToProfile" >My Profile</a>
      </li>

      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
    import { useRouter } from "vue-router";

    const router = useRouter();

    const goToProfile = () => {
        router.push("/profile");
    }

</script>

<style >
</style>
