<template>
  <BaseTemplate>
    <div class="container">
      <h2>Welcome to the User Dashboard</h2>
      <div class="options">
        <button @click="viewAllUsers" class="btn btn-info">View All Users</button>
        <button @click="viewUserInfo" class="btn btn-info">View Your Information</button>
        <button @click="editUserInfo" class="btn btn-info">Edit Your Information</button>
        <button v-if="isAdmin" @click="createUser" class="btn btn-info">Register New User</button>
      </div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from 'axios';
import BaseTemplate from './BaseTemplate.vue';

export default {
  name: 'UserDashboard',
  components: {
    BaseTemplate,
  },
  data() {
    return {
      userId: null,
      isAdmin: false, // Initialize isAdmin here
    };
  },
  created() {
    this.fetchUserInfo();
  },
  methods: {
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/payroll/profile/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.userId = response.data.id;
        this.isAdmin = response.data.is_admin; // Ensure this is a boolean
        localStorage.setItem('userId', this.userId);
        localStorage.setItem('isAdmin', this.isAdmin);
        console.log(localStorage.getItem('userId'));
        console.log(localStorage.getItem('isAdmin'));
      } catch (error) {
        console.error('Failed to fetch user info:', error);
      }
    },
    viewAllUsers() {
      this.$router.push({ name: 'AllUsers' });
    },
    viewUserInfo() {
      this.$router.push({ name: 'UserInfo', params: { userId: this.userId } });
    },
    editUserInfo() {
      this.$router.push({ name: 'EditUserInfo', params: { userId: this.userId } });
    },
    createUser() {
      this.$router.push({ name: 'UserCreate' });
    },
  },
};
</script>

<style scoped>
.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
