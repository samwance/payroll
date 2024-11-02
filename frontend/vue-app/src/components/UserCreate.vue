<template>
  <BaseTemplate>
    <div class="container-user">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="title">Create New User</h2>
      <form v-if="currentUserIsAdmin" @submit.prevent="createUser" class="user-form">
        <div class="form-group" v-for="(field, index) in fields" :key="index">
          <label :for="field.id">{{ field.label }}:</label>
          <input
            v-if="field.type !== 'select'"
            :type="field.type"
            v-model="userData[field.model]"
            :id="field.id"
            class="form-control"
            :placeholder="field.label"
            required
          />
          <select
            v-else
            v-model="userData[field.model]"
            :id="field.id"
            class="form-control"
          >
            <option value="" disabled>Select {{ field.label }}</option>
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
        { id: 'email', label: 'Email', model: 'email', type: 'email' },
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
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.container-user {
  max-width: 600px;
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

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
}

.user-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-control {
  padding: 12px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.btn {
  padding: 12px;
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

.alert {
  border-radius: 8px;
  padding: 10px;
  margin-top: 15px;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
