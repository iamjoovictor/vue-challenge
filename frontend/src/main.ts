import './assets/main.scss';

import axios from 'axios';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { PrimeVue } from '@primevue/core';
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify';

const clearSessionAndRedirect = () => {
    localStorage.removeItem('token');
    router.push('/login');
};

axios.interceptors.response.use(
    (response) => response,
    (error) => {
        const status = error?.response?.status;

        if (status === 401 || status === 403) {
            clearSessionAndRedirect();
        }

        return Promise.reject(error);
    }
);

const app = createApp(App)

app.use(router)
app.use(PrimeVue, {
    ripple: true,
    unstyled: true
})
app.use(Vue3Toastify, {
    autoClose: 3000,
} as ToastContainerOptions);

app.mount('#app');
