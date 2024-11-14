import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/page/main.vue';
import Belbin from '@/page/belbin.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Main,
    },
    {
        path: '/belbin_test',
        name: 'Belbin',
        component: Belbin,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;