import { createRouter, createWebHistory } from "vue-router"

const Dashboard = () => import("./views/Dashboard.vue")
const PlayerBatting = () => import("./components/PlayerBatting.vue")
const PlayerPitching = () => import("./components/TopYoungPitchersChart.vue")

const routes = [
    { path: "/", component: Dashboard },
    { path: "/dashboard", component: Dashboard },
    { path: "/batting", component: PlayerBatting },
    { path: "/pitching", component: PlayerPitching },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
