import './assets/main.scss';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { PrimeVue } from '@primevue/core';
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify';

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
