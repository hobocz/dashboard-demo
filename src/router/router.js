import { createRouter, createWebHistory } from "vue-router"

const Dashboard = () => import("@/components/Dashboard.vue")
const Players = () => import("@/components/Players.vue")
const PlayerBatting = () => import("@/components/PlayerBatting.vue")
const PlayerPitching = () => import("@/components/TopYoungPitchersChart.vue")

const routes = [
    { path: "/", name: "home", component: Dashboard },
    { path: "/players", name: "players", component: Players },
    { path: "/batting", name: "batting", component: PlayerBatting },
    { path: "/pitching", name: "pitching", component: PlayerPitching },
]

const router = createRouter({
    // Note: when using createWebHistory() in production, a catch-all 
    // fallback route should exist, serving 'index.html'
    history: createWebHistory(),
    routes,
})

export default router
