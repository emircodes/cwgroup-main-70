<template>
    <div v-if="friendReq">
        <h1 class="rounded-4">Friend Requests</h1>

        <form >
          <div  >
            <div v-for="item in friendReq.received_requests" :key="item" class="input-group">
              <input type="text" class="form-control" :placeholder="item.sender" aria-label="Recipient's username with two button addons">
              <button class="btn btn-success" value="accept" type="button">Accept</button>
              <button class="btn btn-danger" value='reject' type="button">Reject</button>
            </div>
            
          </div>
        </form>
    </div>

    <div>
      <h1> Add Friend</h1>
      <form>
        <ul>
          <li v-for="friend in addFriends" :key="friend.id">
            {{ friend.username }}
          </li>
        </ul>
      </form>
    </div>

    <div>
      <h1>My Friends</h1>
      <ul v-for="item in friends">
        <li :key="item">{{ item }}</li>
      </ul>
    </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { onMounted, ref } from 'vue';

const addFriends = ref([]);
const friendReq = ref([]);
const friends = ref([]);
const error= ref('');

onMounted(async () => {
    try {
      const responseFriendReq = await axios.get('/api/get-friend-request/', { withCredentials: true });
      friendReq.value = responseFriendReq.data

      const responseUsers = await axios.get('/api/users/', { withCredentials: true});
      addFriends.value = responseUsers.data

      const responseFriend = await axios.get('/api/profile/', {withCredentials: true});
      friends.value = responseFriend.data.friends;

      console.log(responseFriendReq.data);
      console.log(responseUsers);
      console.log(responseFriend.data.friends);
      
      
    } catch (err) {
      error.value = 'Failed to load profile';
    }
});
</script>