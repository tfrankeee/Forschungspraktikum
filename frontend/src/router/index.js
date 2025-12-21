import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Test from '../views/test.vue'
import Login from '../views/LoginRegistrationView.vue'

Vue.use(VueRouter)

//TODO: add "requiresAuth" for specific sites to handle expired tokens
const routes = [
  {
    path: '/',
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
      title: 'Test erstellen',
      requiresAuth: true
    }
  },
  {
    path: '/login-or-register',
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

// handling expired tokens
function isTokenExpired(token) {
  try {
    const payloadPart = token.split(".")[1];
    const payloadJson = atob(payloadPart.replace(/-/g, "+").replace(/_/g, "/"));
    const payload = JSON.parse(payloadJson);

    if (!payload.exp) return false; 
    const now = Math.floor(Date.now() / 1000);
    return payload.exp <= now;
  } catch (e) {
    return true;
  }
}

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  if (token && isTokenExpired(token)) {
    localStorage.removeItem("access_token");
    localStorage.removeItem("access_token_expires_at");
  }

  const hasToken = !!localStorage.getItem("access_token");

  if (to.matched.some(r => r.meta.requiresAuth) && !hasToken) {
    return next("/login");
  }

  next();
});

export default router
