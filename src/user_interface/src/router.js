import { createRouter, createWebHistory } from 'vue-router';
import BrowseLibrary from './components/BrowseLibrary.vue';
import LoginRegister from './components/LoginRegister.vue';

const routes = [
    { path: '/', name: 'BrowseLibrary', component: BrowseLibrary },
    { path: '/login-register', name: 'LoginRegister', component: LoginRegister }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;