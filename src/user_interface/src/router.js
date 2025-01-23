import { createRouter, createWebHistory } from 'vue-router';
import BrowseLibrary from './components/BrowseLibraryComponent.vue';
import SignIn from './components/SignInComponent.vue';
import WatchlistComponent from './components/WatchlistComponent.vue';

const routes = [
    { path: '/', name: 'BrowseLibrary', component: BrowseLibrary },
    { path: '/signin', name: 'SignIn', component: SignIn },
    { path: '/watchlist', name: 'Watchlist', component: WatchlistComponent },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;