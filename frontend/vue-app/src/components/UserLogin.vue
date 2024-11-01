<template>
  <div class="container">
    <h2>{{ isRegister ? 'Register' : 'Login' }}</h2>
    <form @submit.prevent="submitForm">
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
        />
        <input
          v-else
          type="text"
          id="phone"
          v-model="phone"
          class="form-control"
          required
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
        />
      </div>
      <button type="submit" class="btn btn-primary">{{ isRegister ? 'Register' : 'Login' }}</button>
    </form>
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
      isRegister: true, // Start with the registration form
      isUsernameLogin: true,
      username: '',
      phone: '',
      password: ''
    };
  },
  methods: {
    async submitForm() {
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
        // Optionally, handle error display to the user
      }
    },
    toggleForm() {
      this.isRegister = !this.isRegister; // Toggle between register and login
      this.username = ''; // Reset username
      this.phone = ''; // Reset phone
      this.password = ''; // Reset password
    }
  }
};
</script>

<style>
.toggle-login {
  cursor: pointer;
  color: blue;
  text-decoration: underline;
}
</style>
