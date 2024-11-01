<template>
  <BaseTemplate>
    <div class="container">
      <h2>All Tasks</h2>
      <div v-if="tasks.length > 0" class="tasks">
        <ul>
          <li v-for="task in tasks" :key="task.id">
            <h4>{{ task.title }}</h4>
            <p>{{ task.description }}</p>
            <p>Status: {{ task.status }}</p>
            <p>Priority: {{ task.priority }}</p>
            <p>Deadline: {{ new Date(task.deadline).toLocaleString() }}</p>
            <p>
              Assignee: 
              <router-link 
                v-if="task.assignee.username" 
                :to="{ name: 'UserInfo', params: { userId: task.assignee_id } }" 
                class="btn btn-warning">
                {{ task.assignee.username }}
              </router-link>
            </p>
            <p v-if="isTaskCreator(task.creator_id)">
              <button @click="deleteTask(task.id)" class="btn btn-danger">
                <i class="fas fa-trash-alt"></i> <!-- Font Awesome Trash Icon -->
              </button>
            </p>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No tasks available.</p>
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
      userId: localStorage.getItem('userId'), // Get user ID directly from local storage
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
        console.log(response);
        console.log('User IDD:', this.userId)
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
  },
};
</script>

<style scoped>
.tasks {
  margin-top: 20px;
}
.tasks li {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
.btn-danger {
  color: white;
  background-color: red;
}
</style>
