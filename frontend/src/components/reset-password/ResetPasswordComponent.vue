<style lang="scss">
@import '../reset-password/ResetPasswordComponent.scss';
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
                password: '' as string,
                confirmPassword: '' as string,
            },
            token: '' as string,
            isLoading: false as boolean,
            invalidToken: false as boolean,
        }
    },
    mounted() {
        const params = new URLSearchParams(window.location.search);
        const token = params.get('token');
        if (!token) {
            this.invalidToken = true;
        } else {
            this.token = token;
        }
    },
    methods: {
        async handleReset() {
            const { password, confirmPassword } = this.form;

            if (!password.trim() || !confirmPassword.trim()) {
                toastMessageService.error("Fill in all fields");
                return;
            }

            if (password !== confirmPassword) {
                toastMessageService.error("Passwords do not match");
                return;
            }

            this.isLoading = true;

            userService.resetPassword({ token: this.token, new_password: password })
                .then(() => {
                    toastMessageService.sucess("Password reset successfully. Please sign in.");
                    this.isLoading = false;
                    router.push('/login');
                })
                .catch((error) => {
                    this.isLoading = false;
                    const status = error.response?.status;
                    const detail = error.response?.data?.detail;

                    if (status === 400) toastMessageService.error(detail ?? "Invalid or expired reset link");
                    else if (status === 422) toastMessageService.error(detail?.[0]?.msg ?? "Password does not meet requirements");
                    else toastMessageService.error("Server error. Please try again.");
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

            <template v-if="invalidToken">
                <div class="auth-header">
                    <h1>Invalid link</h1>
                    <p>This password reset link is missing or malformed.</p>
                </div>
            </template>

            <template v-else>
                <div class="auth-header">
                    <h1>Reset password</h1>
                    <p>Enter your new password below</p>
                </div>
                <form class="auth-form" @submit.prevent="handleReset">
                    <div class="form-field">
                        <label for="password">
                            <i class="pi pi-lock"></i>
                            New password
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
                            Confirm new password
                        </label>
                        <div class="input-wrapper">
                            <Password
                                id="confirmPassword"
                                v-model="form.confirmPassword"
                                :feedback="false"
                                :inputProps="{ autocomplete: 'new-password' }"
                                placeholder="Repeat your new password"
                                :disabled="isLoading"
                                toggleMask
                            />
                        </div>
                    </div>
                    <button type="submit" class="auth-btn" :disabled="isLoading">
                        <span class="btn-inner" v-if="!isLoading">
                            <i class="pi pi-check"></i>
                            Set new password
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
                            Saving...
                        </span>
                    </button>
                </form>
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
