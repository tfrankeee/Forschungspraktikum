import axios from "axios";

export const api = axios.create({
    // TODO: adjust the link to the correct server link 
    baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err?.response?.status === 401) {
      localStorage.removeItem("access_token");
      // redirect to login-page
      if (window.location.pathname !== "/login-or-register") {
        window.location.href = "/login-or-register";
      }
    }
    return Promise.reject(err);
  }
);
