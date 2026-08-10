<style lang="scss">
@import '../login/LoginComponent.scss';
</style>

<script lang="ts">
import ToastMessageService from '@/middleware/components/toastMessage.service';
import type { token } from '@/middleware/inteface/login';
import router from '@/router';
import LoginService from '@/services/login/login.service';

const loginService = new LoginService();
const toastMessageService = new ToastMessageService();

localStorage.removeItem('token');

export default {
    data() {
        return {
            form: {
                username: '' as string,
                password: '' as string,
            },
            isLoading: false as boolean
        }
    },
    methods: {
        async handleLogin() {
            if (this.form.username.trim() && this.form.password.trim()) {
                this.isLoading = true;
                loginService.login(this.form.username, this.form.password)
                    .then((response) => {
                        let data: token = response.data;
                        localStorage.setItem('token', data.access_token);
                        toastMessageService.sucess("Login successfully");
                        this.isLoading = false;
                        router.push('/dashboard');
                    })
                    .catch((error) => {
                        this.isLoading = false;
                        if (error.response.status == 401) {
                            toastMessageService.error("Incorrect login");
                        } else {
                            toastMessageService.error("Server error");
                        }
                    });
            } else {
                toastMessageService.error("Fill in all fields");
            }
        }
    }
}
</script>

<template>
    <div class="login-page">
        <div class="login-card">
            <div class="login-logo">
                <img src="../../assets/images/login/logo.svg" alt="logo" />
            </div>
            <div class="login-header">
                <h1>Welcome back</h1>
                <p>Sign in to your account to continue</p>
            </div>
            <form class="login-form" @submit.prevent="handleLogin">
                <div class="form-field">
                    <label for="username">
                        <i class="pi pi-user"></i>
                        Username
                    </label>
                    <div class="input-wrapper">
                        <InputText
                            id="username"
                            v-model="form.username"
                            autocomplete="off"
                            placeholder="Enter your username"
                            :disabled="isLoading"
                        />
                    </div>
                </div>
                <div class="form-field">
                    <label for="password">
                        <i class="pi pi-lock"></i>
                        Password
                    </label>
                    <div class="input-wrapper">
                        <Password
                            id="password"
                            v-model="form.password"
                            :feedback="false"
                            :inputProps="{ autocomplete: 'new-password' }"
                            placeholder="Enter your password"
                            :disabled="isLoading"
                            toggleMask
                        />
                    </div>
                </div>
                <button type="submit" class="login-btn" :disabled="isLoading">
                    <span class="btn-inner" v-if="!isLoading">
                        <i class="pi pi-sign-in"></i>
                        Sign In
                    </span>
                    <span class="btn-inner" v-else>
                        <svg viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg" width="18" height="18" stroke="currentColor">
                            <g fill="none" fill-rule="evenodd">
                                <g transform="translate(1 1)" stroke-width="2">
                                    <circle stroke-opacity=".35" cx="18" cy="18" r="18"></circle>
                                    <path d="M36 18c0-9.94-8.06-18-18-18">
                                        <animateTransform attributeName="transform" type="rotate" from="0 18 18" to="360 18 18" dur="0.8s" repeatCount="indefinite"></animateTransform>
                                    </path>
                                </g>
                            </g>
                        </svg>
                        Signing in...
                    </span>
                </button>
                <div class="login-links">
                    <RouterLink to="/forgot-password" class="login-link">Forgot your password?</RouterLink>
                </div>
            </form>
            <div class="login-footer">
                <span>Don't have an account?</span>
                <RouterLink to="/register" class="login-link login-link--accent">Sign up</RouterLink>
            </div>
        </div>
    </div>
</template>
