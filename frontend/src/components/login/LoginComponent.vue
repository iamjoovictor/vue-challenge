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
                loginService.login(this.form.username, this.form.password)
                    .then((response) => {
                        let data: token = response.data;

                        toastMessageService.sucess("Login successfully");

                        localStorage.setItem('token', data.access_token);

                        setTimeout(() => {
                            router.push('/registration');
                        });
                    })
                    .catch((error) => {
                        if (error.response.status == 401) {
                            toastMessageService.error("Incorrect login");
                        }

                        else {
                            toastMessageService.error("Server error");
                        }

                    });
            }

            else {
                toastMessageService.error("Fill in all fields");
            }
        }
    }
}
</script>

<template>
    <div class="loading" v-if="isLoading">
        <svg viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg" width="128" height="128" stroke="#007bff">
            <g fill="none" fill-rule="evenodd">
                <g transform="translate(1 1)" stroke-width="2">
                    <circle stroke-opacity=".25" cx="18" cy="18" r="18"></circle>
                    <path d="M36 18c0-9.94-8.06-18-18-18">
                        <animateTransform attributeName="transform" type="rotate" from="0 18 18" to="360 18 18"
                            dur="0.8s" repeatCount="indefinite"></animateTransform>
                    </path>
                </g>
            </g>
        </svg>
    </div>
    <form class="login-wrapper" :style="{ opacity: isLoading ? 0.3 : 1 }">
        <div class="login-form">
            <img src="../../assets/images/login/logo.svg">
            <div class="login-inputs">
                <div class="login-input margin-top-2rem">
                    <label for="username">Username</label>
                    <InputText id="username" v-model="form.username" autocomplete="off" />
                </div>
                <div class="login-input margin-top-1-5rem">
                    <label for="password">Password</label>
                    <Password id="password" v-model="form.password" :feedback="false" autocomplete="off" />
                </div>
            </div>

            <div class="login-button">
                <div class="margin-top-1-5rem margin-bottom-1-5rem">
                    <Button pButton pRipple class="col-12" label="Login" @click="handleLogin()">
                    </Button>
                </div>
            </div>
        </div>
    </form>
    <Toast />
</template>