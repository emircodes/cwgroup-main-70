<template>
  <div class="m-auto d-flex">
    <div style="width: 85vw;">
      <div class="card-body mt-2">
        <div class="card">
          <h2 class="card-title">User List</h2>

          <!-- Age Range Dropdown -->
          <div class="age-filter">
            <label for="ageRange">Select Age Range:</label>
            <select v-model="selectedAgeRange" id="ageRange">
              <option v-for="range in ageRanges" :key="range.label" :value="range">
                {{ range.label }}
              </option>
            </select>
          </div>
        </div>
          

        <!-- User Table -->
        <table class="mb-2">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Age</th>
              <th>Similarity Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.calculated_age }}</td>
              <td>{{ user.similarity_score }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Controls -->
        <div class="pagination">
          <button :disabled="!pagination.previous" @click="navigateToPage(pagination.previous)">
            Previous
          </button>
          <button :disabled="!pagination.next" @click="navigateToPage(pagination.next)">
            Next
          </button>
        </div>
      </div>
    </div>
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

// Define predefined age ranges
const ageRanges = ref<AgeRange[]>([
  { label: 'Choose', min: 0, max: 99 },
  { label: '7-18', min: 7, max: 18 },
  { label: '19-25', min: 19, max: 25 },
  { label: '26-31', min: 26, max: 31 },
  { label: '32-40', min: 32, max: 40 },
  { label: '41-50', min: 41, max: 50 },
  { label: '51-60', min: 51, max: 60 },
  { label: '61-70', min: 61, max: 70 },
]);

// Pinia store for user data
const userStore = useUserStore();
const users = computed<User[]>(() => userStore.similarUsers);

// Pagination data
const pagination = ref({
  next: null as string | null,
  previous: null as string | null,
});

// Fetch users with pagination and filtering support
const fetchUsers = async (minAge?: number, maxAge?: number, url?: string) => {
  try {
    await userStore.fetchSimilarUsers(minAge || 0, maxAge || 100, url);
    pagination.value.next = userStore.pagination.next;
    pagination.value.previous = userStore.pagination.previous;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

// Default age range selection
const selectedAgeRange = ref<AgeRange>(ageRanges.value[0]); // Default to '19-25'

// Fetch users when the component is mounted
onMounted(() => {
  const { min, max } = selectedAgeRange.value;
  fetchUsers(min, max);
});

// Watch for changes in the selected age range
watch(selectedAgeRange, async (newRange) => {
  const { min, max } = newRange;
  await fetchUsers(min, max);
});

function extractRelativePath(absoluteUrl: string | null): string | null {
  if (!absoluteUrl) return null;

  try {
    // Attempt to parse it as an absolute URL
    const parsed = new URL(absoluteUrl, window.location.origin);
    // Return just the path + query string (and hash if needed)
    return parsed.pathname + parsed.search;
  } catch (error) {
    // If it's already relative or invalid, just return the original string
    return absoluteUrl;
  }
}

const navigateToPage = async (url: string | null) => {
  if (!url) return;

  // Convert "http://127.0.0.1:8000/api/similar-users/?page=2" 
  // into "/api/similar-users/?page=2"
  const relativeUrl = extractRelativePath(url);
  const { min, max } = selectedAgeRange.value;

  // Now fetch the data with the relative URL so the Vite proxy is used
  await fetchUsers(min, max, relativeUrl);
};

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
