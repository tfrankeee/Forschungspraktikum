import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Test from '../views/test.vue'
import Login from '../views/LoginRegistrationView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Test Runner Home',
      requiresAuth: false
    }
  },
  {
    path: '/test/:id',
    name: 'Test',
    // route level code-splitting
    // this generates a separate chunk (test.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "test" */ '../views/TestRunner.vue'),
    meta: {
      title: 'Test Runner',
      requiresAuth: true
    }
  },
  {
    path: '/form',
    name: 'form',
    component: Test,
    meta: {
      title: 'Test erstellen'
    }
  },
  {
    path: '/login',
    name: 'Login/Registrierung',
    component: Login,
    meta: {
      title: 'Login/Registrierung'
    }
  }
]

// Make this work when deployed to a /testrunner/ folder in production
const publicPath = process.env.NODE_ENV === 'production'
    ? '/testrunner/'
    : '/'

const router = new VueRouter({
  mode: 'history',
  base: publicPath,
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  if (to.matched.some((record) => record.meta.requiresAuth) && !token) {
    next("/login");
  } else {
    next();
  }
});
export default router
