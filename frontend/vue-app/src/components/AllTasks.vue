<template>
  <BaseTemplate>
    <div class="container-tasks">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="title">All Tasks</h2>
      <div v-if="tasks.length > 0" class="tasks">
        <ul class="task-list">
          <li v-for="task in tasks" :key="task.id" class="task-card">
            <div class="task-content">
            <router-link :to="{ name: 'Task', params: { taskId: task.id } }" class="task-title">
              <h4 class="task-title">{{ task.title }}</h4>
            </router-link>
              <p class="task-description">{{ task.description }}</p>
              <div class="task-details">
                <p><strong>Status:</strong> {{ task.status }}</p>
                <p><strong>Priority:</strong> {{ task.priority }}</p>
                <p><strong>Deadline:</strong> {{ new Date(task.deadline).toLocaleString() }}</p>
                <p>
                  <strong>Assignee:</strong>
                  <router-link
                    v-if="task.assignee.username"
                    :to="{ name: 'UserInfo', params: { userId: task.assignee_id } }"
                    class="btn btn-warning">
                    {{ task.assignee.username }}
                  </router-link>
                </p>
              </div>
            </div>
            <div class="task-actions" v-if="isTaskCreator(task.creator_id) || isAdmin">
              <button @click="deleteTask(task.id)" class="btn btn-danger">
                <i class="fas fa-trash-alt"></i> <!-- Font Awesome Trash Icon -->
              </button>
            </div>
          </li>
        </ul>
      </div>
      <div v-else>
        <p class="no-tasks-message">No tasks available.</p>
      </div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'AllTasks',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      tasks: [], // Array to hold tasks
      userId: localStorage.getItem('userId'),
      isAdmin: localStorage.getItem('isAdmin') === 'true',
    };
  },
  created() {
    this.fetchAllTasks();
  },
  methods: {
    async fetchAllTasks() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/tasks/', {
          headers: {
            Authorization: `Bearer ${token}`,
            accept: 'application/json',
          },
        });
        this.tasks = response.data.tasks; // Accessing the tasks array from the response
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      }
    },
    isTaskCreator(creatorId) {
      return Number(this.userId) === creatorId;
    },
    async deleteTask(taskId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://localhost:8000/tasks/${taskId}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
            accept: 'application/json',
          },
        });
        this.tasks = this.tasks.filter(task => task.id !== taskId); // Remove the deleted task from the list
      } catch (error) {
        console.error('Failed to delete task:', error);
      }
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container-tasks {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.light .dashboard-tasks {
  background-color: #ffffff; /* Light background */
  color: #333; /* Light text color */
}

.dark .dashboard-tasks {
  background-color: #495057; /* Dark background */
  color: #f8f9fa; /* Dark text color */
}

.task-title {
  display: block; /* Makes the entire area clickable */
  padding: 10px;
  border: 1px solid transparent; /* Border for better visibility */
  border-radius: 5px;
  color: #333; /* Text color */
  text-decoration: none; /* Remove underline */
  font-weight: bold; /* Make the text bold */
  transition: background-color 0.3s, border-color 0.3s;
}

.task-title:hover {
  background-color: #e0f7fa; /* Change background on hover */
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
}

.tasks {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.task-list {
  list-style: none;
  padding: 0;
}

.task-card {
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  padding: 15px;
  transition: box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.task-card:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.task-content {
  flex-grow: 1;
}

.task-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
  transform: scale(1.05);
}

.btn-warning {
  background-color: #ffc107;
  color: black;
}

.btn-warning:hover {
  background-color: #e0a800;
  transform: scale(1.05);
}

.no-tasks-message {
  text-align: center;
  color: #6c757d;
  font-size: 1.2rem;
}
</style>
