import { createApp } from "vue"
// import "./style.css"
// import "@/assets/custom.scss"
import App from "./App.vue"
import router from "@/router/router"
import { createPinia } from "pinia"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "bootstrap-icons/font/bootstrap-icons.css"

const pinia = createPinia()

createApp(App)
    .use(router)
    .use(pinia)
    .mount("#app")
