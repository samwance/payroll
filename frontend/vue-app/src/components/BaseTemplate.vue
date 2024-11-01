<template>
  <div :class="theme" class="full-page">
    <div v-if="isAuthenticated" class="header">
      <button @click="goBack" class="btn-menu btn-secondary return-button" title="Return Back">
        <i class="fas fa-arrow-left"></i>
      </button>
      <button @click="logout" class="btn-menu btn-danger logout-button" title="Logout">
        <i class="fas fa-sign-out-alt"></i>
      </button>
      <button @click="toggleTheme" class="btn-menu btn-info theme-button" title="Toggle Theme">
        <i :class="theme === 'light' ? 'fas fa-sun' : 'fas fa-moon'"></i>
      </button>
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
      theme: 'light', // Default theme
    };
  },
  created() {
    this.checkAuthentication();
    this.loadTheme();
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
    loadTheme() {
      const savedTheme = localStorage.getItem('theme') || 'light';
      this.theme = savedTheme;
    },
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', this.theme);
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

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.btn-menu {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
}
.btn-menu i {
  font-size: 24px;
}
</style>
