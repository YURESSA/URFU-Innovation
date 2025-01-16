import { createApp } from 'vue';
import '../public/assets/main.css';
import App from './App.vue';
import router from './routers/routes.js';
import { createPinia } from 'pinia';
import piniaPersist from 'pinia-plugin-persistedstate';
import VueApexCharts from 'vue3-apexcharts'

const pinia = createPinia();
pinia.use(piniaPersist);

const app = createApp(App);

app.use(router);
app.use(pinia);
app.component('apexchart', VueApexCharts)
app.mount('#app');
