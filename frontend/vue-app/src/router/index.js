import Vue from 'vue';
import Router from 'vue-router';
import UserLogin from '../components/UserLogin.vue';
import UserDashboard from '../components/UserDashboard.vue';
import AllUsers from '../components/AllUsers.vue';
import UserInfo from '../components/UserInfo.vue';
import UserCreate from '../components/UserCreate.vue';
import MyInfo from '../components/MyInfo.vue';
import EditUserInfo from '../components/EditUserInfo.vue';
import AllTasks from '../components/AllTasks.vue';
import CreateTask from '../components/CreateTask.vue';
import Task from '../components/Task.vue';

Vue.use(Router);

const routes = [
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: UserDashboard
  },
  {
    path: '/users',
    name: 'AllUsers',
    component: AllUsers
  },
  {
    path: '/user/:userId',
    name: 'UserInfo',
    component: UserInfo
  },
  {
    path: '/',
    name: 'UserCreate',
    component: UserCreate
  },
  {
    path: '/profile',
    name: 'MyInfo',
    component: MyInfo
  },
  {
    path: '/edit/',
    name: 'EditUserInfo',
    component: EditUserInfo
  },
  {
    path: '/tasks/',
    name: 'AllTasks',
    component: AllTasks
  },
  {
    path: '/tasks/create/',
    name: 'CreateTask',
    component: CreateTask
  },
  {
    path: '/tasks/:taskId/',
    name: 'Task',
    component: Task
  },
];

const router = new Router({
  mode: 'history',
  routes
});

export default router;
