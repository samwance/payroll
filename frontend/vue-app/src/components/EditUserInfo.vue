<template>
  <BaseTemplate>
    <div class="container-user">
      <button @click="goBack" class="btn btn-secondary">Go Back</button>
      <h2 class="text-center mb-4">Edit User</h2>
      <form @submit.prevent="updateUser">
        <div class="form-group">
          <label for="phone">Phone:</label>
          <input type="text" id="phone" v-model="user.phone" class="form-control">
        </div>
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="user.name" class="form-control">
        </div>
        <div class="form-group">
          <label for="second_name">Second Name:</label>
          <input type="text" id="second_name" v-model="user.second_name" class="form-control">
        </div>
        <div class="form-group">
          <label for="surname">Surname:</label>
          <input type="text" id="surname" v-model="user.surname" class="form-control">
        </div>
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="user.username" class="form-control">
        </div>
        <div class="form-group">
          <label for="position">Position:</label>
          <input type="text" id="position" v-model="user.position" class="form-control">
        </div>
        <div class="form-group">
          <label for="salary">Salary:</label>
          <input type="number" id="salary" v-model="user.salary" class="form-control" min="0">
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="user.password" class="form-control">
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          Update User
        </button>
      </form>
      <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'EditUserInfo',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      user: {
        phone: '',
        name: '',
        second_name: '',
        surname: '',
        position: '',
        salary: 0,
        password: '',
        username: '',
      },
      error: null,
      successMessage: '',
      loading: false,
    };
  },
  async created() {
    await this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      const token = localStorage.getItem('token');

      try {
        const response = await axios.get(`http://localhost:8000/payroll/profile/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.user = response.data; // Autofill user data
      } catch (error) {
        this.error = error.response.data.detail || 'An error occurred while fetching user data.';
        console.error(error);
      }
    },
    async updateUser() {
      this.loading = true;
      const token = localStorage.getItem('token');

      try {
        const payload = {
          username: this.user.username,
          second_name: this.user.second_name,
          name: this.user.name,
          surname: this.user.surname,
          phone: this.user.phone,
          position: this.user.position,
          salary: this.user.salary,
          password: this.user.password // Include if required
        };
        await axios.patch(`http://localhost:8000/payroll/users/`, payload, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.successMessage = 'User updated successfully!';
        this.error = null;
        this.$router.push({ name: 'MyInfo',});
      } catch (error) {
        this.error = error.response.data.detail || 'An error occurred';
        this.successMessage = '';
      } finally {
        this.loading = false;
      }
    },
    goBack() {
      this.$router.go(-1);
    },
  }
};
</script>

<style scoped>
.container-user {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.alert {
  margin-top: 20px;
}
</style>
