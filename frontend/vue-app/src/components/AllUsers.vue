<template>

  <BaseTemplate>
  <div class="container">
    <h2>All Users</h2>
    <ul class="list-group">
      <li v-for="user in users" :key="user.id" class="list-group-item">
        <router-link 
          :to="user.id === currentUserId 
            ? { name: 'MyInfo', query: { token: token } } 
            : { name: 'UserInfo', params: { userId: user.id } }">
          {{ user.name }} ({{ user.phone }}) 
          <span v-if="user.id === currentUserId">(you)</span>
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
      token: localStorage.getItem('token') // Store token in data
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
  }
};
</script>
