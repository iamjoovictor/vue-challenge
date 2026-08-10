<style lang="scss">
@import '../forgot-password/ForgotPasswordComponent.scss';
</style>

<script lang="ts">
import ToastMessageService from '@/middleware/components/toastMessage.service';
import UserService from '@/services/user/user.service';
import type { ForgotPasswordResponse } from '@/middleware/inteface/user';

const userService = new UserService();
const toastMessageService = new ToastMessageService();

export default {
    data() {
        return {
            form: {
                email: '' as string,
            },
            isLoading: false as boolean,
            submitted: false as boolean,
            // In development the reset token is returned by the API; remove this in production
            devResetToken: '' as string,
        }
    },
    methods: {
        async handleForgotPassword() {
            if (!this.form.email.trim()) {
                toastMessageService.error("Enter your email address");
                return;
            }

            this.isLoading = true;

            userService.forgotPassword({ email: this.form.email })
                .then((response) => {
                    const data: ForgotPasswordResponse = response.data;
                    this.devResetToken = data.reset_token;
                    this.submitted = true;
                    this.isLoading = false;
                })
                .catch(() => {
                    this.isLoading = false;
                    toastMessageService.error("Server error. Please try again.");
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

            <template v-if="!submitted">
                <div class="auth-header">
                    <h1>Forgot password?</h1>
                    <p>Enter your email and we'll send a reset link</p>
                </div>
                <form class="auth-form" @submit.prevent="handleForgotPassword">
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
                                placeholder="Enter your registered email"
                                :disabled="isLoading"
                            />
                        </div>
                    </div>
                    <button type="submit" class="auth-btn" :disabled="isLoading">
                        <span class="btn-inner" v-if="!isLoading">
                            <i class="pi pi-send"></i>
                            Send reset link
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
                            Sending...
                        </span>
                    </button>
                </form>
            </template>

            <template v-else>
                <div class="auth-header">
                    <h1>Check your email</h1>
                    <p>A reset link has been sent if that address is registered.</p>
                </div>
                <!-- DEV ONLY: show token directly. Remove in production when email is configured. -->
                <div v-if="devResetToken" class="dev-token-box">
                    <p class="dev-token-label">Dev — reset token:</p>
                    <RouterLink :to="`/reset-password?token=${devResetToken}`" class="auth-link auth-link--accent">
                        Click here to reset password
                    </RouterLink>
                </div>
            </template>

            <div class="auth-footer">
                <RouterLink to="/login" class="auth-link auth-link--accent">
                    <i class="pi pi-arrow-left" style="font-size: 0.7rem;"></i>
                    Back to sign in
                </RouterLink>
            </div>
        </div>
    </div>
</template>
