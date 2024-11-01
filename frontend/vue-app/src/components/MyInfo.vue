<template>
  <BaseTemplate>
  <div class="container">
    <h2>Your Information</h2>
    <div v-if="user">
      <p><strong>Name:</strong> {{ user.name }}</p>
      <p><strong>Second Name:</strong> {{ user.second_name }}</p>
      <p><strong>Surname:</strong> {{ user.surname }}</p>
      <p><strong>Phone:</strong> {{ user.phone }}</p>
      <p><strong>Position:</strong> {{ user.position }}</p>
      <p><strong>Salary:</strong> {{ user.salary }}</p>
      <img v-if="user.photo" :src="user.photo" alt="User Photo" width="100" />
      <router-link 
        v-if="user.id === currentUserId" 
        :to="{ name: 'EditUserInfo', params: { userId: user.id } }"
        class="btn btn-warning">
        Edit Your Information
      </router-link>
    </div>
    <div v-else>
      <p>User not found.</p>
    </div>
  </div>
   <div class="container">
          <h3>Your Tasks</h3>
          <ul v-if="user.assigned_tasks && user.assigned_tasks.length > 0">
            <li v-for="task in user.assigned_tasks" :key="task.id">
              <strong>{{ task.title }}</strong> - {{ task.description }} (Status: {{ task.status }})
            </li>
          </ul>
          <p v-else>No assigned tasks.</p>
        </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'CurrentUserInfo',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      user: null,
      currentUserId: null,
    };
  },
  async created() {
    const userId = Number(localStorage.getItem('userId'));
    this.currentUserId = userId; // Set current user ID

    try {
        const token = localStorage.getItem('token'); // Get token from local storage
        const response = await axios.get('http://localhost:8000/payroll/profile/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      this.user = response.data; // Assuming response.data contains the user object structured according to your schema
    } catch (error) {
      console.error(error);
    }
  }
};
</script>
