<template>
  <BaseTemplate>
  <div class="container">
    <h2>Edit User</h2>
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
        <input type="number" id="salary" v-model="user.salary" class="form-control">
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="user.password" class="form-control">
      </div>
      <button type="submit" class="btn btn-primary">Update User</button>
    </form>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
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
      error: null
    };
  },
  async created() {
    try {
      const token = localStorage.getItem('token'); 
      const response = await axios.get(`http://localhost:8000/payroll/profile/`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
      this.user = response.data;
      console.log(response.data); 
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    async updateUser() {
      const userId = this.$route.params.userId;
        const token = localStorage.getItem('token'); 
      try {
            const payload = {
                        username: this.user.username,
                        second_name: this.user.second_name, // Ensure these fields exist in your user object
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
        alert('User updated successfully!');
        this.$router.push({ name: 'UserInfo', params: { userId } });
      } catch (error) {
        this.error = error.response.data.detail || 'An error occurred';
      }
    }
  }
};
</script>
