<template>
  <BaseTemplate>
    <div class="container-users">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="title">All Users</h2>
      <ul class="list-group">
        <li 
          v-for="user in users" 
          :key="user.id"
          class="list-item"
        >
          <router-link 
            :to="user.id === currentUserId 
              ? { name: 'MyInfo', query: { token: token } } 
              : { name: 'UserInfo', params: { userId: user.id } }"
            class="user-link"
          >
            <span class="username">{{ user.username }}</span>
            <span v-if="user.id === currentUserId" class="current-user">(you)</span>
          </router-link>
        </li>
      </ul>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'AllUsers',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      users: [],
      currentUserId: null,
      token: localStorage.getItem('token'), // Store token in data
    };
  },
  async created() {
    await this.fetchAllUsers(); // Fetch all users on component creation
    this.currentUserId = Number(localStorage.getItem('userId')); // Get current user ID
    console.log('Storing User ID:', this.currentUserId); 
  },
  methods: {
    async fetchAllUsers() {
      try {
        const response = await axios.get('http://localhost:8000/payroll/users/', {
          headers: {
            Authorization: `Bearer ${this.token}`, // Use token from data
          },
        });
        this.users = response.data.users; // Store the list of users
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style>
.container-users {
  max-width: 800px;
  margin: 50px auto;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.title {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 600;
}

.list-group {
  list-style-type: none;
  padding: 0;
}

.list-item {
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.light .list-item {
  background-color: #ffffff; /* Light list item background */
}

.dark .list-item {
  background-color: #343a40; /* Dark list item background */
}

.user-link {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  border-radius: 10px;
  text-decoration: none;
  color: inherit; /* Inherit color from parent */
}

.light .user-link {
  color: #333; /* Light text color */
}

.dark .user-link {
  color: #f8f9fa; /* Dark text color */
}

.user-link:hover {
  transform: translateY(-2px);
}

.current-user {
  font-weight: bold;
  color: #007bff; /* Highlight current user */
}

.light .user-link:hover {
  background-color: #f8f9fa; /* Light hover background */
}

.dark .user-link:hover {
  background-color: #495057; /* Dark hover background */
}
</style>
