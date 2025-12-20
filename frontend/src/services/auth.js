import {api} from "./api";

export async function register({email, username, password}){
    await api.post("users/register", {
        email,
        username,
        password
    })
}

// Login (OAuth2PasswordRequestForm!)
export async function login(identifier, password){
    const body = new URLSearchParams();
    body.append("username", identifier);
    body.append("password", password);

    const response = await api.post("users/login", body, {
        headers:  { "Content-Type": "application/x-www-form-urlencoded" },
    });

    localStorage.setItem("access_token", response.data.access_token);
    return response.data;
}

export function logout(){
    localStorage.removeItem("access_token");
}