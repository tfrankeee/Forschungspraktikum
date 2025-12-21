import {api} from "./api";

export async function register(username, email, password) {
  const payload = { username, email, password };
  console.log("REGISTER payload ->", payload);
  await api.post("/users/register", payload);
}

export async function login(identifier, password) {
    const body = new URLSearchParams();
    body.append("username", identifier);
    body.append("password", password);

    const response = await api.post("/users/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    const expiresInMs = response.data.expires_in_minutes * 60 * 1000;
    const expiresAt = Date.now() + expiresInMs;

    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("access_token_expires_at", expiresAt.toString());

    return response.data;
}

export function logout(){
    localStorage.removeItem("access_token");
    localStorage.removeItem("access_token_expires_at");
}