<template>
  <BaseTemplate>
    <div class="container-user">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="title">Your Information</h2>
      <div v-if="user" class="user-info">
        <div class="user-details">
          <img v-if="user.photo" :src="user.photo" alt="User Photo" class="user-photo" />
          <div class="info">
            <p><strong>Name:</strong> {{ user.name }}</p>
            <p><strong>Second Name:</strong> {{ user.second_name }}</p>
            <p><strong>Surname:</strong> {{ user.surname }}</p>
            <p><strong>Phone:</strong> {{ user.phone }}</p>
            <p><strong>Position:</strong> {{ user.position }}</p>
            <p><strong>Salary:</strong> {{ user.salary.toFixed(2) }}</p>
          </div>
        </div>
        <router-link 
          v-if="user.id === currentUserId" 
          :to="{ name: 'EditUserInfo', params: { userId: user.id } }"
          class="btn btn-warning">
          Edit Your Information
        </router-link>
      </div>
      <div v-else>
        <p class="error-message">User not found.</p>
      </div>
    </div>

    <div class="tasks-container">
      <h3>Your Tasks</h3>
      <ul v-if="user.assigned_tasks && user.assigned_tasks.length > 0" class="task-list">
        <li v-for="task in user.assigned_tasks" :key="task.id" class="task-item">
          <strong>{{ task.title }}</strong> - {{ task.description }} 
          <span class="task-status">(Status: {{ task.status }})</span>
        </li>
      </ul>
      <p v-else class="no-tasks">No assigned tasks.</p>
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
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container-user {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 12px;
  background-color: #ffffff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.light .container-user {
  background-color: #ffffff; /* Light background */
  color: #333; /* Light text color */
}

.dark .container-user {
  background-color: #495057; /* Dark background */
  color: #f8f9fa; /* Dark text color */
}

.tasks-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 12px;
  background-color: #ffffff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.light .tasks-container {
  background-color: #ffffff; /* Light background */
  color: #333; /* Light text color */
}

.dark .tasks-container {
  background-color: #495057; /* Dark background */
  color: #f8f9fa; /* Dark text color */
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-details {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-photo {
  border-radius: 50%;
  width: 100px;
  height: 100px;
  margin-right: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.info {
  text-align: left;
}

.error-message {
  color: #dc3545;
  text-align: center;
}

.tasks-container {
  margin-top: 30px;
}

.task-list {
  list-style-type: none;
  padding: 0;
}

.task-item {
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: background-color 0.3s, transform 0.2s;
}

.task-item:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
}

.task-status {
  font-style: italic;
}

.no-tasks {
  text-align: center;
  color: #6c757d;
}
</style>
