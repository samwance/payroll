<template>
  <div>
    <div v-if="isAuthenticated" class="header">
      <button @click="goBack" class="btn btn-secondary return-button">Return Back</button>
      <button @click="logout" class="btn btn-danger logout-button">Logout</button>
    </div>
    <slot v-if="isAuthenticated"></slot>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isAuthenticated: false,
    };
  },
  created() {
    this.checkAuthentication();
  },
  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('You need to be logged in to access this page.');
        this.redirectToLogin();
      } else {
        this.isAuthenticated = true; // Set this based on your logic
      }
    },
    redirectToLogin() {
      this.$router.push({ name: 'UserLogin' });
    },
    async logout() {
      try {
        const token = localStorage.getItem('token');
        await axios.delete('http://localhost:8000/logout/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        localStorage.removeItem('token');
        localStorage.removeItem('userId');
        localStorage.removeItem('isAdmin');
        this.redirectToLogin(); // Redirect after logout
      } catch (error) {
        console.error('Logout failed:', error);
      }
    },
    goBack() {
      this.$router.go(-1); // Navigate back to the previous page
    }
  },
};
</script>
