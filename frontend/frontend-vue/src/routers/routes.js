import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/page/main.vue';
import Belbin from '@/page/belbin.vue';
import BelbinResult from '@/page/belbin-result.vue';
import Admin from '@/page/admin-login.vue';
import AdminMain from '@/page/admin-main.vue';
import Profile from '@/page/profile.vue';
import Disc from '@/page/disc.vue';
import DiscResult from '@/page/disc-result.vue';

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
        path: '/disc_test',
        name: 'Disc',
        component: Disc,
    },
    {
        path: '/belbin-result',
        name: 'BelbinResult',
        component: BelbinResult
    },
    {
        path: '/disc-result',
        name: 'DiscResult',
        component: DiscResult
    },
    {
        path: '/admin',
        name: 'AdminLogin',
        component: Admin 
    },
    {
        path: '/admin/database',
        name: 'AdminMain',
        component: AdminMain
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile 
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;