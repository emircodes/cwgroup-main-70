<template>
    <div>
        <h1>Friends</h1>
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { onMounted, ref } from 'vue';

const friends = ref([]);
const error= ref('');

onMounted(async () => {
    try {
      const response = await axios.get('/api/profile/', { withCredentials: true });
      friends.value = response.data.friends;
      console.log(response.data)
      console.log(response.data.friends);
      
    } catch (err) {
      error.value = 'Failed to load profile';
    }
});
</script>