<template>
  <div :class="theme" class="full-page">
    <div v-if="isAuthenticated" class="header">
      <button @click="logout" class="btn-menu btn-danger logout-button" title="Logout" aria-label="Logout">
        <i class="fas fa-sign-out-alt"></i> Logout
      </button>
      <button @click="toggleTheme" class="btn-menu btn-info theme-button" title="Toggle Theme" aria-label="Toggle Theme">
        <i :class="theme === 'light' ? 'fas fa-sun' : 'fas fa-moon'"></i> 
        {{ theme === 'light' ? 'Light Mode' : 'Dark Mode' }}
      </button>
    </div>
    <slot v-if="isAuthenticated"></slot>

    <!-- Loading Spinner -->
    <div v-if="loading" class="spinner-overlay">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>

    <!-- Toast Notifications -->
    <div v-if="notification" class="toast" :class="notification.type">
      <div class="toast-body">
        {{ notification.message }}
        <button type="button" class="btn-close" aria-label="Close" @click="notification = null"></button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isAuthenticated: false,
      theme: 'light', // Default theme
      loading: false,
      notification: null, // For toast notifications
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
      this.loading = true; // Show loading spinner
      try {
        const token = localStorage.getItem('token');
        await axios.delete('http://localhost:8000/logout/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        localStorage.removeItem('token');
        this.showNotification('Successfully logged out!', 'success');
        this.redirectToLogin(); // Redirect after logout
      } catch (error) {
        console.error('Logout failed:', error);
        this.showNotification('Logout failed. Please try again.', 'error');
      } finally {
        this.loading = false; // Hide loading spinner
      }
    },
    showNotification(message, type) {
      this.notification = { message, type }; // type can be 'success' or 'error'
      setTimeout(() => {
        this.notification = null; // Auto-dismiss notification after 3 seconds
      }, 3000);
    }
  },
};
</script>

<style scoped>
.full-page {
  min-height: 100vh;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s ease;
}

.header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 20px 40px;
  width: 100%;
  background-color: var(--header-bg-color);
}

.btn-menu {
  padding: 12px 20px; /* Increased padding for bigger buttons */
  font-size: 1rem; /* Increased font size */
  border-radius: 8px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin-left: 10px; /* Space between buttons */
}

.btn-menu:hover {
  transform: scale(1.05); /* Slightly enlarge on hover */
}

.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  z-index: 1000;
}

.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  min-width: 250px;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: opacity 0.5s ease;
}

.toast.success {
  background-color: #d4edda;
  color: #155724;
}

.toast.error {
  background-color: #f8d7da;
  color: #721c24;
}

.toast-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
}
</style>
