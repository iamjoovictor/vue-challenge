<style lang="scss">
@import '../register/RegisterComponent.scss';
</style>

<script lang="ts">
import ToastMessageService from '@/middleware/components/toastMessage.service';
import router from '@/router';
import UserService from '@/services/user/user.service';

const userService = new UserService();
const toastMessageService = new ToastMessageService();

export default {
    data() {
        return {
            form: {
                username: '' as string,
                email: '' as string,
                password: '' as string,
                confirmPassword: '' as string,
            },
            isLoading: false as boolean
        }
    },
    methods: {
        async handleRegister() {
            const { username, email, password, confirmPassword } = this.form;

            if (!username.trim() || !email.trim() || !password.trim() || !confirmPassword.trim()) {
                toastMessageService.error("Fill in all fields");
                return;
            }

            if (password !== confirmPassword) {
                toastMessageService.error("Passwords do not match");
                return;
            }

            this.isLoading = true;

            userService.register({ username, email, password })
                .then(() => {
                    toastMessageService.sucess("Account created successfully. Please sign in.");
                    this.isLoading = false;
                    router.push('/login');
                })
                .catch((error) => {
                    this.isLoading = false;
                    const status = error.response?.status;
                    const detail = error.response?.data?.detail;

                    if (status === 409) toastMessageService.error(detail ?? "Username or email already taken");
                    else if (status === 422) toastMessageService.error(detail?.[0]?.msg ?? "Invalid data");
                    else toastMessageService.error("Server error");
                });
        }
    }
}
</script>

<template>
    <div class="auth-page">
        <div class="auth-card">
            <div class="auth-logo">
                <img src="../../assets/images/login/logo.svg" alt="logo" />
            </div>
            <div class="auth-header">
                <h1>Create an account</h1>
                <p>Fill in the details below to get started</p>
            </div>
            <form class="auth-form" @submit.prevent="handleRegister">
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
                            placeholder="Choose a username"
                            :disabled="isLoading"
                        />
                    </div>
                </div>
                <div class="form-field">
                    <label for="email">
                        <i class="pi pi-envelope"></i>
                        Email
                    </label>
                    <div class="input-wrapper">
                        <InputText
                            id="email"
                            v-model="form.email"
                            type="email"
                            autocomplete="email"
                            placeholder="Enter your email"
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
                            placeholder="At least 8 chars, 1 uppercase, 1 digit"
                            :disabled="isLoading"
                            toggleMask
                        />
                    </div>
                </div>
                <div class="form-field">
                    <label for="confirmPassword">
                        <i class="pi pi-lock"></i>
                        Confirm password
                    </label>
                    <div class="input-wrapper">
                        <Password
                            id="confirmPassword"
                            v-model="form.confirmPassword"
                            :feedback="false"
                            :inputProps="{ autocomplete: 'new-password' }"
                            placeholder="Repeat your password"
                            :disabled="isLoading"
                            toggleMask
                        />
                    </div>
                </div>
                <button type="submit" class="auth-btn" :disabled="isLoading">
                    <span class="btn-inner" v-if="!isLoading">
                        <i class="pi pi-user-plus"></i>
                        Create account
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
                        Creating account...
                    </span>
                </button>
            </form>
            <div class="auth-footer">
                <span>Already have an account?</span>
                <RouterLink to="/login" class="auth-link auth-link--accent">Sign in</RouterLink>
            </div>
        </div>
    </div>
</template>
