<template>
    <form 
    @submit.prevent="onSubmit" 
    class="h-100 d-flex flex-column align-items-center justify-content-center"
    >
        <div class="d-flex flex-column gap-3">
            <label for="identifier">Nutzername/E-Mail-Adresse</label>
            <input type="text" id="identifier" v-model="identifier" class="w-100" />

            <div class="mt-3">
                <PasswordInput label="Passwort" v-model="password"/>
            </div>
        </div>
        <p v-if="error" class="text-danger">{{ error }}</p>
            
        <button class="mt-5 primary" :disabled="loading">
            {{loading ? "Einloggen ..." : "Einloggen"}}</button>
    </form>
</template>

<script>
    import PasswordInput from '@/components/PasswordInput.vue';
    import { login } from "@/services/auth";

    export default {
        name: 'Login',
        components: {
            PasswordInput
        },
        data(){
            return{
                identifier: "",
                password: "",
                loading: false,
                error: ""
            };
        },
        methods: {
            async onSubmit(){
                this.error = "";
                this.loading = true;

                try{
                    await login(this.identifier, this.password);
                    this.$router.push("/")
                } catch(err){
                    err?.response?.data?.detail ||
                    err?.message || 
                    "Login fehlgeschlagen";
                }finally{
                    this.loading = false;
                }
            },
        },
    };
</script>