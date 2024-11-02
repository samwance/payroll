<template>
  <BaseTemplate>
    <div class="dashboard-container">
      <h2 class="dashboard-title">Welcome to the User Dashboard</h2>
      <div class="options">
        <button @click="viewAllUsers" class="btn btn-info">View All Users</button>
        <button @click="viewUserInfo" class="btn btn-info">View Your Information</button>
        <button @click="editUserInfo" class="btn btn-info">Edit Your Information</button>
        <button v-if="isAdmin" @click="createUser" class="btn btn-info">Register New User</button>
        <button @click="getAllTasks" class="btn btn-info">View Tasks</button>
        <button @click="createTask" class="btn btn-info">Create New Task</button>
      </div>
      <div v-if="tasks.length > 0" class="tasks">
        <h3>Your Tasks:</h3>
        <ul>
          <li v-for="task in tasks" :key="task.id" class="task-item">{{ task.name }}</li>
        </ul>
      </div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'UserDashboard',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      userId: null,
      isAdmin: false,
      tasks: [],
    };
  },
  created() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/payroll/profile/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.userId = response.data.id;
        this.isAdmin = response.data.is_admin;
        localStorage.setItem('userId', this.userId);
        localStorage.setItem('isAdmin', this.isAdmin);
      } catch (error) {
        console.error('Failed to fetch user info:', error);
      }
    },
    viewAllUsers() {
      this.$router.push({ name: 'AllUsers' });
    },
    viewUserInfo() {
      this.$router.push({ name: 'MyInfo'});
    },
    editUserInfo() {
      this.$router.push({ name: 'EditUserInfo', params: { userId: this.userId } });
    },
    createUser() {
      this.$router.push({ name: 'UserCreate' });
    },
    getAllTasks() {
      this.$router.push({ name: 'AllTasks' });
    },
    createTask() {
      this.$router.push({ name: 'CreateTask' });
    },
  },
};
</script>

<style>
.dashboard-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.light .dashboard-container {
  background-color: #ffffff; /* Light background */
  color: #333; /* Light text color */
}

.dark .dashboard-container {
  background-color: #495057; /* Dark background */
  color: #f8f9fa; /* Dark text color */
}

.dashboard-title {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 600;
}

.options {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px; /* Space between buttons */
}

.btn {
  padding: 12px 20px;
  border-radius: 10px;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.light .btn-info {
  background: linear-gradient(135deg, #17a2b8, #00d4ff);
  color: white;
}

.dark .btn-info {
  background: linear-gradient(135deg, #007bff, #00d4ff);
  color: white;
}

.btn-info:hover {
  transform: translateY(-2px);
}

.light .btn-info:hover {
  background: linear-gradient(135deg, #138496, #00bfff);
}

.dark .btn-info:hover {
  background: linear-gradient(135deg, #0056b3, #00bfff);
}

.tasks {
  margin-top: 30px;
}

.task-item {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 10px;
  margin-bottom: 10px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.light .task-item {
  background-color: #ffffff; /* Light task item background */
}

.dark .task-item {
  background-color: #6c757d; /* Dark task item background */
}

.task-item:hover {
  transform: translateY(-1px);
}

.light .task-item:hover {
  background-color: #e9ecef; /* Light task item hover */
}

.dark .task-item:hover {
  background-color: #5a6268; /* Dark task item hover */
}
</style>
