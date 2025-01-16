<template>
  <Nav />
  <div class="d-flex justify-content-center h-75 align-items-center">
    <div class="card h-75 w-75">
      <div class="card-body ">

        <!--Nav -->
        <ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link position-relative" :class="{active: activeTab === 'home'}" @click="tabActive('home')" id="home-tab" data-bs-toggle="tab" data-bs-target="#home-tab-pane" type="button" role="tab" aria-controls="home-tab-pane" >
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {{ friendReq.length }}
                <span class="visually-hidden">unread messages</span>
              </span>
              <i class="pi pi-bell"></i>
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" :class="{active: activeTab === 'profile'}" @click="tabActive('profile')" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile-tab-pane" type="button" role="tab" aria-controls="profile-tab-pane" >
              <i class="pi pi-user-plus"></i>
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" :class="{active: activeTab === 'contact'}" @click="tabActive('contact')" id="contact-tab" data-bs-toggle="tab" data-bs-target="#contact-tab-pane" type="button" role="tab" aria-controls="contact-tab-pane" >
              <i class="pi pi-address-book"></i>
            </button>
          </li>
        </ul>

        <!--Tabs-->
        <div class="tab-content" id="myTabContent">

          <!--Friend Request-->
          <div class="tab-pane fade" :class="{'show active': activeTab === 'home'}" id="home-tab-pane" role="tabpanel" aria-labelledby="home-tab" tabindex="0">
            <div v-if="friendReq.length">
                <form >
                  <div  >
                    <div v-for="item in friendReq" :key="item.id" class="input-group">
                      <span class="input-group-text">ID {{ item.id }}</span>
                      <input type="text" class="form-control" 
                      :placeholder="usersCanAddFriends.find(x => x.id === item.sender)?.username || 'unknown'" 
                      aria-label="Recipient's username with two button addons" readonly>
                      <button class="btn btn-success" @click="acceptFriend('accept', item.id, item.sender)" value="accept" type="button">Accept</button>
                      <button class="btn btn-danger" @click="acceptFriend('reject', item.id, item.sender)" value='reject' type="button">Reject</button>
                    </div>
                    
                  </div>
                </form>
            </div>

            <div v-else class="center">
              <h3 class="center">no friend requests ... </h3>
            </div>
          </div>

          <!--Add Friends Tab -->
          <div class="tab-pane fade" :class="{'show active': activeTab === 'profile'}" id="profile-tab-pane" role="tabpanel" aria-labelledby="profile-tab" tabindex="0">
            <div>
                <h1> Add Friend</h1>
                <form>
                  <div class="input-group mb-3" 
                  v-for="friend in usersCanAddFriends":key="friend.id">
                    <input type="text" class="form-control" 
                    :value="friend.username" readonly
                    aria-label="Recipient's username" aria-describedby="button-addon2">
                    <button class="btn btn-primary" 
                    :class="{'btn-outline-secondary': pendingUsers.includes(friend.id) || friendReq.some(x=> x.sender === friend.id)}"
                    @click="sendFriendRequest(friend.id)"
                    type="button" id="button-addon2" :disabled="pendingUsers.includes(friend.id) || friendReq.some(x=> x.sender === friend.id)">
                      {{ (pendingUsers.includes(friend.id) || friendReq.some(x=> x.sender === friend.id)) ? 'Pending': 'Add Friend' }}
                    </button>
                    <button v-if="pendingUsers.includes(friend.id)"
                    class="btn btn-danger" 
                    @click="cancelFriendReq(friend.id)"
                    type="button" id="button-addon2" >
                      Cancel
                    </button>
                  </div>
                </form>
            </div>
          </div>

          <!--My Friends Tab-->
          <div class="tab-pane fade" :class="{'show active': activeTab === 'contact'}" id="contact-tab-pane" role="tabpanel" aria-labelledby="contact-tab" tabindex="0">
            <div v-if="myFriendsName.length">
              <h1>My Friends</h1>
              <form v-for="item in myFriendsName" :key="item">
                <div class="input-group mb-3" >
                  <input type="text" class="form-control" 
                  :value="item.username" readonly
                  aria-label="Recipient's username" aria-describedby="button-addon2">
                  <button class="btn btn-outline-secondary" 
                  @click="removeFriend(item.id)"
                  type="button" id="button-addon2">Remove Friend</button>
                </div>
              </form>
            </div>

            <div v-else class="center">
              <h3 class="center">add more friends !!  </h3>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios, { AxiosHeaderValue } from 'axios';
import { onMounted, onUnmounted, ref, toRaw, watch } from 'vue';
import { usePersonal } from '../stores/personalAccount';
import Nav from './Nav.vue';

const activeTab = ref('home');
const users = ref([]);
const usersCanAddFriends = ref([]);
const friendReq = ref([]);
const friends = ref([]);
const myFriendsName = ref([]);
const pendingUsers = ref([]);
const pendingUsersData = ref([]);
const id = ref();
const error= ref('');
const csrfToken = ref('') //

watch(users, async () => {
  filter();
});

function tabActive(tabName: string){
  activeTab.value = tabName;
}

function filter( ) {
  if(users.value && friends.value && pendingUsers.value) {
      const filteredUsers = users.value.filter(user =>!friends.value.includes(user.id) && user.id != id.value);
      console.log("users");
      usersCanAddFriends.value = filteredUsers;

      const  filteredUsersFriendsName = users.value.filter(user =>friends.value.includes(user.id));
      myFriendsName.value = filteredUsersFriendsName;

      console.log(usersCanAddFriends.value);
      console.log(friends.value);
  }
}

onMounted(() => {
  // Initial fetch on mount
  fetchUpdatedData().then(() => {
    filter();
    console.log(myFriendsName.value);
  }).catch(err => {
    error.value = 'Failed to load profile: ' + err.message;
    console.error(err);
  });

  // Set interval to fetch updated data every 5 seconds
  const intervalId = setInterval(() => {
    fetchUpdatedData().then(() => {
      filter();
      console.log(myFriendsName.value);
    }).catch(err => {
      error.value = 'Failed to fetch updated data: ' + err.message;
      console.error(err);
    });
  }, 5000); // Interval set to 5 seconds

  // Cleanup the interval when the component is unmounted
  onUnmounted(() => {
    clearInterval(intervalId);
  });
});

async function acceptFriend(value: string, id:number, userSenderID: number){
  if (value === 'accept') {
    try{
      // patch pending requests to accepted
      const res = await axios.patch(`/api/friend-requests/${id}/`, {
        status: 'accepted'
      }, {
        headers: {
          'X-CSRFToken': csrfToken.value
        },
        withCredentials: true
      })

      friends.value = [...friends.value, userSenderID]

      const raw = toRaw(friends.value)

      // update friends list
      const updateFriend = await axios.patch('/api/profile/', {
        friends: raw
      }, {
        headers: {
          'X-CSRFToken': csrfToken.value
        },
        withCredentials: true
      })

      console.log(raw);
      

      const removeFriendRequest = await axios.delete(`/api/friend-requests/${id}/`, {
        headers: {
          'X-CSRFToken': csrfToken.value
        },
        withCredentials: true
      })
      console.log(friends.value);
      
      await fetchUpdatedData();
      filter();
      tabActive('home');

    } catch (err) {
      error.value = 'Failed to accept friend';
    }

  } else {
    try{
      const res = await axios.patch(`/api/friend-requests/${id}/`, {
          status:'rejected'
      }, {
        headers: {
          'X-CSRFToken': csrfToken.value
        },
        withCredentials: true
      })

      const removeFriendRequest = await axios.delete(`/api/friend-requests/${id}/`, {
        headers: {
          'X-CSRFToken': csrfToken.value
        },
        withCredentials: true
      })

      await fetchUpdatedData();
      filter();
      tabActive('home');

    } catch (err) {
      error.value = 'Failed to reject friend';
    }
  }
}

async function fetchUpdatedData() {
  try {
    const resPendingUsers = await axios.get('/api/getPendingRequests/', {withCredentials: true})
    pendingUsers.value = resPendingUsers.data.map(x => x.receiver)
    pendingUsersData.value = resPendingUsers.data;
    console.log(resPendingUsers.data);
    
    
    const res = await axios.get('/api/get-token/', {withCredentials:true})
    csrfToken.value = res.data.token;

    const responseFriendReq = await axios.get('/api/friend-requests/', { withCredentials: true });
    friendReq.value = responseFriendReq.data
    console.log(friendReq.value);
    

    const responseUsers = await axios.get('/api/users/', { withCredentials: true});
    users.value = responseUsers.data

    const responseFriend = await axios.get('/api/profile/', {withCredentials: true});
    id.value = responseFriend.data.id;
    friends.value = responseFriend.data.friends;


  } catch (err) {
    error.value = 'Failed to fetch updated data';
  }
}


async function removeFriend(index: number){
  const x = friends.value.indexOf(index);
  if (x != -1){
    friends.value.splice(x, 1)
  }
  try {
    const updateFriend = await axios.patch('/api/profile/', {
      friends: friends.value
    }, {
      headers: {
        'X-CSRFToken': csrfToken.value
      },
      withCredentials: true
    })

    await fetchUpdatedData()
    filter();
    tabActive('contact');

  } catch (err) {
    error.value = 'Failed to remove friend';
  }
}

async function sendFriendRequest(receiverID: number){
  try{
    await axios.post('/api/addFriendRequest/', {
      sender: id.value,  // user's id
      receiver: receiverID,
      status: 'pending',
    }, {
      headers: {
        'X-CSRFToken': csrfToken.value
      },
      withCredentials: true
    })

    await fetchUpdatedData();
    filter();
    tabActive('profile');
  } catch (err) {
    error.value = 'Failed to send friend request';
  }
}

async function cancelFriendReq(id: number){
  const x = pendingUsersData.value.find(x => x.receiver === id)
  id = x.id;
  try{
    const res = await axios.delete(`/api/friend-requests/${id}/`, {
      headers: {
        'X-CSRFToken': csrfToken.value
      },
      withCredentials: true
    })

    await fetchUpdatedData();
    filter();
    tabActive('profile');
  } catch (err) {
    error.value = 'Failed to delete friend request';
  }
} 

</script>