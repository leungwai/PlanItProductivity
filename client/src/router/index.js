import Vue from 'vue';
import Router from 'vue-router';
import PingPage from '../components/PingPage.vue';
import CreateEvent from '../components/CreateEvent.vue';
import CreateTask from '../components/CreateTask.vue';
import CreateSubcategory from '../components/CreateSubcategory.vue';
import CreateCategory from '../components/CreateCategory.vue';
import TodayComponent from '../components/TodayComponent.vue';
import SuccessPage from '../components/SuccessPage.vue';
import ErrorPage from '../components/ErrorPage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import HomePage from '../components/HomePage.vue';
import ShowTask from '../components/ShowTask.vue';
import ShowEvent from '../components/ShowEvent.vue';
import store from '../store';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: PingPage,
      meta: { guest: true },
    },
    {
      path: '/createEvent',
      name: 'CreateEvent',
      component: CreateEvent,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/createTask',
      name: 'CreateTask',
      component: CreateTask,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/showTask',
      name: 'ShowTask',
      component: ShowTask,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/showEvent',
      name: 'ShowEvent',
      component: ShowEvent,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/createSubcategory',
      name: 'CreateSubcategory',
      component: CreateSubcategory,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/createCategory',
      name: 'CreateCategory',
      component: CreateCategory,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/today',
      name: 'Today',
      component: TodayComponent,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/success',
      name: 'Success',
      component: SuccessPage,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
    {
      path: '/error',
      name: 'Error',
      component: ErrorPage,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (from.matched.some((record) => record.meta.requiresAuth)) {
          if (!store.getters.isLoggedIn) {
            next('/home');
            return;
          }
          next();
        } else {
          next();
        }
      },
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage,
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterPage,
      meta: { guest: true },
    },
    {
      path: '/home',
      name: 'Home',
      component: HomePage,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        if (!store.getters.isLoggedIn) {
          next('/login');
          return;
        }
        next();
      },
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.guest)) {
    if (store.getters.isAuthenticated) {
      next('/home');
      return;
    }
    next();
  } else {
    next();
  }
});

export default router;
