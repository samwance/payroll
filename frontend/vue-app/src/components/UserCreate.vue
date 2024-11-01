<template>
  <BaseTemplate>
    <div class="container">
      <h2>Create New User</h2>
      <form v-if="currentUserIsAdmin" @submit.prevent="createUser">
        <div class="form-group" v-for="(field, index) in fields" :key="index">
          <label :for="field.id">{{ field.label }}:</label>
          <input
            v-if="field.type !== 'select'"
            :type="field.type"
            v-model="userData[field.model]"
            :id="field.id"
            class="form-control"
          />
          <select
            v-else
            v-model="userData[field.model]"
            :id="field.id"
            class="form-control"
          >
            <option v-for="option in field.options" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" v-model="userData.username" id="username" required class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          Create User
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        </button>
      </form>
      <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
      <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'CreateUser',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      userData: {
        name: '',
        second_name: '',
        surname: '',
        phone: '',
        email: '',
        position: '',
        salary: null,
        username: '',
      },
      currentUserIsAdmin: false,
      errorMessage: '',
      successMessage: '',
      loading: false,
      fields: [
        { id: 'name', label: 'Name', model: 'name', type: 'text' },
        { id: 'secondName', label: 'Second Name', model: 'second_name', type: 'text' },
        { id: 'surname', label: 'Surname', model: 'surname', type: 'text' },
        { id: 'phone', label: 'Phone', model: 'phone', type: 'text' },
        { id: 'email', label: 'Email', model: 'email', type: 'text' },
        { id: 'position', label: 'Position', model: 'position', type: 'text' },
        { id: 'salary', label: 'Salary', model: 'salary', type: 'number', step: '0.01' },
      ],
    };
  },
  created() {
    this.checkAdminStatus();
  },
  methods: {
    async checkAdminStatus() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/payroll/profile/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.currentUserIsAdmin = response.data.is_admin;
        if (!this.currentUserIsAdmin) {
          this.showAdminAlert();
        }
      } catch (error) {
        console.error('Failed to fetch user info:', error);
        this.currentUserIsAdmin = false;
        this.showAdminAlert();
      }
    },
    showAdminAlert() {
      alert('This page is only available for admins.');
    },
    async createUser() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://localhost:8000/payroll/', this.userData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.successMessage = 'User created successfully!';
        this.errorMessage = '';
        this.resetForm();
      } catch (error) {
        this.handleError(error);
      } finally {
        this.loading = false;
      }
    },
    resetForm() {
      this.userData = {
        name: '',
        second_name: '',
        surname: '',
        phone: '',
        email: '',
        position: '',
        salary: null,
        username: '',
      };
    },
    handleError(error) {
      if (error.response && error.response.data) {
        this.errorMessage = error.response.data.detail || 'An error occurred while creating the user.';
      } else {
        this.errorMessage = 'An unexpected error occurred.';
      }
      this.successMessage = '';
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}
.spinner-border {
  margin-left: 10px;
}
</style>
