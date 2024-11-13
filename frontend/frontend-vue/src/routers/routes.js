import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/page/main.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Main,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;