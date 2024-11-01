<template>
  <BaseTemplate>
    <div class="container">
      <h2>Create New Task</h2>
      <form @submit.prevent="createTask">
        <div class="form-group">
          <label for="title">Title:</label>
          <input type="text" id="title" v-model="task.title" required class="form-control" />
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="task.description" class="form-control"></textarea>
        </div>
        <div class="form-group">
          <label for="status">Status:</label>
          <select id="status" v-model="task.status" class="form-control">
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
        </div>
        <div class="form-group">
          <label for="priority">Priority:</label>
          <input type="number" id="priority" v-model="task.priority" class="form-control" min="1" max="5" />
        </div>
        <div class="form-group">
          <label for="deadline">Deadline:</label>
          <input type="date" id="deadline" v-model="task.deadline" class="form-control" />
        </div>
        <div class="form-group">
          <label for="assignee">Assignee:</label>
          <select id="assignee" v-model="task.assignee_id" class="form-control" required>
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
         console.log(this.users); 

      } catch (error) {
        console.error(error);
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
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}

.form-group {
  margin-bottom: 15px;
}
</style>
