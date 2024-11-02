<template>
  <BaseTemplate>
    <div class="container-task">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="title">Task Details</h2>

      <div v-if="loading" class="loading">
        <span class="spinner-border" role="status" aria-hidden="true"></span>
        Loading task details...
      </div>

      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

      <div v-if="task" class="task-details">
        <h3>{{ task.title }}</h3>
        <p><strong>Description:</strong> {{ task.description || 'No description provided.' }}</p>
        <p><strong>Status:</strong> {{ task.status }}</p>
        <p><strong>Priority:</strong> {{ task.priority || 'N/A' }}</p>
        <p><strong>Deadline:</strong> {{ task.deadline ? formatDate(task.deadline) : 'No deadline set.' }}</p>
        <p><strong>Creator ID:</strong> {{ task.creator_id }}</p>
        <p><strong>Assignee ID:</strong> {{ task.assignee_id }}</p>
        <p v-if="task.assignee">
          <strong>Assignee:</strong> {{ task.assignee.name }} (ID: {{ task.assignee.id }})
        </p>
      </div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'TaskDetails',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      task: null,
      loading: false,
      errorMessage: '',
    };
  },
  created() {
    const taskId = this.$route.params.taskId;
    this.fetchTask(taskId);
  },
  methods: {
    async fetchTask(taskId) {
      this.loading = true;
      this.errorMessage = '';
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://localhost:8000/tasks/${taskId}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.task = response.data;
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || 'An error occurred while retrieving the task.';
        } else {
          this.errorMessage = 'An unexpected error occurred.';
        }
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container-task {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

.light .container-task {
  background-color: #ffffff; /* Light background */
  color: #333; /* Light text color */
}

.dark .container-task {
  background-color: #495057; /* Dark background */
  color: #f8f9fa; /* Dark text color */
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
  color: #333;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.task-details {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid;
  border-radius: 8px;
}

.btn {
  margin-top: 20px;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 1rem;
}

.alert {
  margin-top: 15px;
  border-radius: 8px;
}
</style>
