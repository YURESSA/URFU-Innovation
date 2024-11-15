import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/page/main.vue';
import Belbin from '@/page/belbin.vue';
import BelbinResult from '@/page/belbin-result.vue';

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
    },
    {
        path: '/belbin-result',
        name: 'BelbinResult',
        component: BelbinResult
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;