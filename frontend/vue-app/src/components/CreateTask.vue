<template>
  <BaseTemplate>
    <div class="container-task">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="title">Create New Task</h2>
      <form @submit.prevent="createTask" class="task-form">
        <div class="form-group">
          <label for="title">Title:</label>
          <input type="text" id="title" v-model="task.title" required class="form-control" placeholder="Enter task title" />
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="task.description" class="form-control" placeholder="Enter task description" rows="4"></textarea>
        </div>
        <div class="form-group">
          <label for="status">Status:</label>
          <select id="status" v-model="task.status" class="form-control status-select">
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
        </div>
        <div class="form-group">
          <label for="priority">Priority:</label>
          <input type="number" id="priority" v-model="task.priority" class="form-control" min="1" max="5" placeholder="1-5" />
        </div>
        <div class="form-group">
          <label for="deadline">Deadline:</label>
          <input type="date" id="deadline" v-model="task.deadline" class="form-control" />
        </div>
        <div class="form-group">
          <label for="assignee">Assignee:</label>
          <select id="assignee" v-model="task.assignee_id" class="form-control" required>
            <option value="" disabled>Select an assignee</option>
            <option v-for="user in users" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Create Task</button>
      </form>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'CreateTask',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      task: {
        title: '',
        description: '',
        status: 'pending',
        priority: null,
        deadline: null,
        assignee_id: null,
      },
      users: [],
    };
  },
  async created() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/payroll/users', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.users = response.data.users;
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    },
    async createTask() {
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://localhost:8000/tasks', this.task, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.$router.push({ name: 'AllTasks' }); // Redirect to the task list after creation
      } catch (error) {
        console.error('Failed to create task:', error);
      }
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
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
}

.task-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-control {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Taller status dropdown */
.status-select {
  height: 45px; /* Adjust height as needed */
}

.btn {
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}
</style>
