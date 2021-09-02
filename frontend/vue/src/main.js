import Vue from 'vue'
import App from './App.vue'
import {router} from "@/routers";
import axios from "axios";


Vue.config.productionTip = false
axios.defaults.baseURL = `http://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}`

new Vue({
    render: h => h(App),
    router
}).$mount('#app')
