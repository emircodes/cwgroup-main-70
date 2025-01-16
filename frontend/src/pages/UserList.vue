<template>
  <div class="user-list">
    <h2 class="table-heading">Users with Similar Hobbies</h2>
    <div class="age-filter">
    <label>
      Select Age Range:
      <select v-model="selectedAgeRange" @change="filterUsersByAge">
        <option v-for="range in ageRanges" :key="range.label" :value="range">
          {{ range.label }}
        </option>
      </select>
    </label>
  </div>
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Name</th>
          <th>Similarity</th>
          <th>Age</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
         
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.similarity_score }}</td>
          <td>{{ user.calculated_age }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useUserStore } from '../stores/userStore';

interface User {
  id: number;
  username: string;
  email: string;
  name: string;
  calculated_age: number;
  similarity_score: number;
}


interface AgeRange {
  label: string;
  min: number;
  max: number;
}
const ageRanges = ref<AgeRange[]>([
  { label: '7-18', min: 7, max: 18 },
  { label: '19-25', min: 19, max: 25 },
  { label: '26-31', min: 26, max: 31 },
  { label: '32-40', min: 32, max: 40 },
  { label: '41-50', min: 41, max: 50 },
  { label: '51-60', min: 51, max: 60 },
  { label: '61-70', min: 61, max: 70 },
]);


const selectedAgeRange = ref<AgeRange>(ageRanges.value[1]); // Default to the first range



// Pinia store for user data
const userStore = useUserStore();

const filterUsersByAge = async () => {
  const { min, max } = selectedAgeRange.value; // Get the min and max age
  await userStore.fetchSimilarUsers(min, max);
};

filterUsersByAge();



// Computed property for the list of users
const users = computed<User[]>(() => userStore.similarUsers);
</script>



<style scoped>
.user-list {
margin-top: 10px; /* Adjusts positioning under navigation */
text-align: center; /* Optional: Centers the content */
}


.table-heading {
margin-top: 20px; /* Space between navbar and heading */
font-size: 24px; /* Adjust heading size */
color: white;
}


table {
width: 100%;
border-collapse: collapse;
margin: 0 auto; /* Centers the table horizontally */
margin-top: 10px; /* Space under heading */
}


th {
background-color: #f2f2f2;
text-align: left;
color: black; /* Make the text color black for table headers */
text-align: center;
}


td {
border: 1px solid #ddd;
padding: 8px;
color: white; /* Keep the text color white for table data */
}
</style>
