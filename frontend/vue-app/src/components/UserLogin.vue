<template>
  <div class="container">
    <h2 class="form-title">{{ isRegister ? 'Register' : 'Login' }}</h2>
    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label v-if="isUsernameLogin" for="username">Username:</label>
        <label v-else for="phone">Phone:</label>
        <input
          v-if="isUsernameLogin"
          type="text"
          id="username"
          v-model="username"
          class="form-control"
          required
          placeholder="Enter your username"
        />
        <input
          v-else
          type="text"
          id="phone"
          v-model="phone"
          class="form-control"
          required
          placeholder="Enter your phone number"
        />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
          required
          placeholder="Enter your password"
        />
      </div>
      <button type="submit" class="btn btn-primary">{{ isRegister ? 'Register' : 'Login' }}</button>
    </form>
    <p v-if="errorMessage" class="error-message text-danger">{{ errorMessage }}</p>
    <p @click="toggleForm" class="toggle-login">
      {{ isRegister ? 'Already have an account? Log in' : 'Don’t have an account? Register' }}
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserAuth',
  data() {
    return {
      isRegister: true,
      isUsernameLogin: true,
      username: '',
      phone: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async submitForm() {
      this.errorMessage = '';
      try {
        const endpoint = this.isRegister ? 'http://localhost:8000/register/' : 'http://localhost:8000/login/';
        const payload = {
          [this.isUsernameLogin ? 'username' : 'phone']: this.isUsernameLogin ? this.username : this.phone,
          password: this.password
        };

        const response = await axios.post(endpoint, payload);
        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/dashboard');
      } catch (error) {
        console.error(error);
        this.errorMessage = error.response?.data?.detail || 'An error occurred. Please try again.';
      }
    },
    toggleForm() {
      this.isRegister = !this.isRegister;
      this.username = '';
      this.phone = '';
      this.password = '';
    }
  }
};
</script>

<style>
.container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, #ffffff, #f0f4f8);
}

.form-title {
  text-align: center;
  margin-bottom: 20px;
  font-weight: 600;
  color: #333;
}

.form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

.form-control {
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 10px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn {
  padding: 12px;
  border-radius: 10px;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #007bff, #00d4ff);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0056b3, #00bfff);
  transform: translateY(-2px);
}

.toggle-login {
  cursor: pointer;
  color: #007bff;
  text-align: center;
  margin-top: 15px;
  text-decoration: underline;
}

.error-message {
  margin-top: 10px;
  color: #dc3545;
  text-align: center;
}
</style>
