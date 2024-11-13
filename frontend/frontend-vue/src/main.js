import { createApp } from 'vue';
import './assets/main.css';
import App from './App.vue';
import router from './routers/routes.js';
import { createPinia } from 'pinia';

const app = createApp(App);

app.use(router);
app.use(createPinia());
app.mount('#app');
