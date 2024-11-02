<template>
  <BaseTemplate>
    <div class="container-user">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="title">User Information</h2>
      <div v-if="user" class="user-info">
        <div class="user-details">
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Second Name:</strong> {{ user.second_name }}</p>
          <p><strong>Surname:</strong> {{ user.surname }}</p>
          <p><strong>Phone:</strong> {{ user.phone }}</p>
          <p><strong>Position:</strong> {{ user.position }}</p>
          <img 
            v-if="user.photo" 
            :src="user.photo" 
            alt="User Photo" 
            class="user-photo" 
            @click="openModal" 
          />
          <p v-if="user.id === currentUserId || currentUserIsAdmin">
            <strong>Salary:</strong> {{ user.salary }}
          </p>
          <router-link 
            v-if="user.id === currentUserId" 
            :to="{ name: 'EditUserInfo', params: { userId: user.id } }" 
            class="btn btn-warning">
            Edit User
          </router-link>
        </div>
      </div>
      <div v-else>
        <p>User not found.</p>
      </div>
      
      <div class="container-tasks">
        <h3>Assigned Tasks</h3>
        <input 
          type="text" 
          v-model="taskFilter" 
          placeholder="Filter tasks..." 
          class="task-filter" 
        />
        <ul v-if="filteredTasks.length > 0">
          <li v-for="task in filteredTasks" :key="task.id" class="task-item">
            <router-link :to="{ name: 'Task', params: { taskId: task.id } }">
              <strong>{{ task.title }}</strong> - {{ task.description }} (Status: {{ task.status }})
            </router-link>
          </li>
        </ul>
        <p v-else>No assigned tasks.</p>
      </div>

      <div v-if="modalVisible" class="modal" @click="closeModal">
        <div class="modal-content" @click.stop>
          <span class="close" @click="closeModal">&times;</span>
          <img :src="user.photo" alt="User Photo" class="modal-image" />
        </div>
      </div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'UserInfo',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      user: null,
      currentUserId: null,
      currentUserIsAdmin: false,
      taskFilter: '',
      modalVisible: false,
    };
  },
  computed: {
    filteredTasks() {
      if (!this.user || !this.user.assigned_tasks) return [];
      return this.user.assigned_tasks.filter(task =>
        task.title.toLowerCase().includes(this.taskFilter.toLowerCase())
      );
    },
  },
  async created() {
    const userId = this.$route.params.userId;
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8000/payroll/users/${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      this.user = response.data;

      this.currentUserId = Number(localStorage.getItem('userId'));
      this.currentUserIsAdmin = localStorage.getItem('isAdmin') === 'true';
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    openModal() {
      this.modalVisible = true;
    },
    closeModal() {
      this.modalVisible = false;
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container-user {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.light .container-user {
  background-color: #ffffff; /* Light background */
  color: #333; /* Light text color */
}

.dark .container-user {
  background-color: #495057; /* Dark background */
  color: #f8f9fa; /* Dark text color */
}

.container-tasks {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.light .container-tasks {
  background-color: #ffffff; /* Light background */
  color: #333; /* Light text color */
}

.dark .container-tasks {
  background-color: #495057; /* Dark background */
  color: #f8f9fa; /* Dark text color */
}


.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: left;
}

.user-photo {
  width: 100px;
  cursor: pointer;
  border-radius: 8px;
  transition: transform 0.3s;
}

.user-photo:hover {
  transform: scale(1.1);
}

.task-filter {
  margin: 15px 0;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  width: 100%;
}

.task-item {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.task-item:hover {
  background-color: #f8f9fa;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
}
</style>
