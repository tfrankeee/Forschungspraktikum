<template>
    <form 
    class="h-100 d-flex flex-column align-items-center justify-content-center"
    @submit.prevent="onSubmit"
    >
        <div class="d-flex flex-column gap-2">
            <label for="reg-username">Nutzername</label>
            <input type="text" id="reg-username" v-model="username" autocomplete="username" required/>

            <label for="reg-email" class="mt-3">E-Mail-Adresse</label>
            <input type="email" id="reg-email"  v-model="email" autocomplete="email" required/>

            <div class="mt-3">
                <PasswordInput label="Passwort" v-model="password"/>
            </div>

            <div class="mt-3">
                <PasswordInput label="Passwort wiederholen" v-model="password2" />
            </div>

            <p v-if="error" class="text-danger mt-2">{{ error }}</p>

        </div>

        <button class="primary mt-5" :disabled="loading">
            {{ loading ? "Registriere..." : "Registrieren" }}
        </button>
    </form>
</template>

<script>
    import PasswordInput from '@/components/PasswordInput.vue';
    import { register, login } from '../services/auth';

    export default {
        name: 'Registration',
        components: {
            PasswordInput
        },
        data(){
            return {
                username: "",
                email: "",
                password: "",
                password2: "",
                loading: false,
                error: "",
            };
        },
        methods: {
            async onSubmit() {

            console.log("Register data:", {
            username: this.username,
            email: this.email,
            password: this.password,
            });

            this.error = "";

            if (this.password !== this.password2) {
                this.error = "Die Passwörter stimmen nicht überein.";
                return;
            }

            this.loading = true;

            try {
                await register(this.username, this.email, this.password);

                await login(this.username, this.password);

                this.$router.push("/");
            } catch (err) {
                this.error =
                err?.response?.data?.detail?.[0]?.msg ||
                err?.response?.data?.detail ||
                err?.message ||
                "Registrierung fehlgeschlagen";


            } finally {
                this.loading = false;
            }
            },
        },
    };
</script>