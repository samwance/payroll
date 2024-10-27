<template>
  <BaseTemplate>
  <div class="container">
    <h2>Create New User</h2>
    <form v-if="currentUserIsAdmin" @submit.prevent="createUser">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" v-model="userData.name" id="name" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="secondName">Second Name:</label>
        <input type="text" v-model="userData.second_name" id="secondName" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="surname">Surname:</label>
        <input type="text" v-model="userData.surname" id="surname" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="phone">Phone:</label>
        <input type="text" v-model="userData.phone" id="phone" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="position">Position:</label>
        <input type="text" v-model="userData.position" id="position" required class="form-control" />
      </div>
      <div class="form-group">
        <label for="salary">Salary:</label>
        <input type="number" v-model="userData.salary" id="salary" required class="form-control" step="0.01" />
      </div>
      <button type="submit" class="btn btn-primary">Create User</button>
    </form>
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>
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
        position: '',
        salary: null,
      },
      currentUserIsAdmin: false,
      errorMessage: '',
      successMessage: '',
    };
  },
  created() {
    this.checkAdminStatus(); // Check if the user is an admin on component creation
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
        this.currentUserIsAdmin = response.data.is_admin; // Set currentUserIsAdmin based on the response

        if (!this.currentUserIsAdmin) {
          alert('This page is only available for admins.'); // Show alert if not admin
        }
      } catch (error) {
        console.error('Failed to fetch user info:', error);
        this.currentUserIsAdmin = false; // Default to false if there's an error
        alert('This page is only available for admins.'); // Show alert if an error occurs
      }
    },
    async createUser() {
      try {
        const token = localStorage.getItem('token');
        await axios.post('http://localhost:8000/payroll/', this.userData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.successMessage = 'User created successfully!';
        this.errorMessage = '';
        this.userData = {
          name: '',
          second_name: '',
          surname: '',
          phone: '',
          position: '',
          salary: null,
        };
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || 'An error occurred while creating the user.';
        } else {
          this.errorMessage = 'An unexpected error occurred.';
        }
        this.successMessage = '';
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
