<template>
    <div class="password-field gap-3">
        <label :for="inputId" class="password-label">{{ label }}</label>

        <div class="input-wrapper">
            <input 
                :id="inputId"
                :type="inputType"
                :value="value"
                @input="$emit('input', $event.target.value)"
                v-model="password"
                class="w-100" />

            <button type="button"
                    class="toggle-button"
                    @click="showPassword = !showPassword"
                    :aria-label="showPassword ? 'Passwort verbergen' : 'Passwort anzeigen'">
                <!-- visible -->
                <EyeIcon role="img" 
                         v-if="showPassword && value" 
                         class="icon"
                         alt="Passwort ausblenden"/>
                <!-- hidden -->
                <EyeOffIcon role="img" 
                            v-if="!showPassword && value" 
                            class="icon" 
                            alt="Passwort anzeigen"/>

            </button>
        </div>
    </div>
</template>

<script>
    import EyeIcon from '@/../public/assets/images/eye-on.svg';
    import EyeOffIcon from '@/../public/assets/images/eye-off.svg';

    export default {
        name: 'PasswordInput',
        props: {
            label: { type: String, required: true },
            value: { type: String, default: ""},
        },
        components: {
            EyeIcon,
            EyeOffIcon
        },
        data() {
            return {
                inputId: 'pw-' + Math.random().toString(36).substr(2, 9),
                password: '',
                showPassword: false
            }
        },
        computed: {
            inputType() {
                if (this.showPassword) return 'text';
                if (!this.value) return 'text';
                return 'password';
            }
        }
    };
</script>

<style scoped>
    .toggle-button {
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        padding: 0;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 30px;
        min-height: 30px;
    }

    .input-wrapper {
        position: relative;
        width: 100%;
    }

    input {
        padding-right: 3rem;
    }
</style>