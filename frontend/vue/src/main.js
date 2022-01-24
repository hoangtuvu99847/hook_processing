import Vue from 'vue'
import App from './App.vue'
import {router} from "@/routers";
import axios from "axios";
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';


Vue.config.productionTip = false
axios.defaults.baseURL = `http://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}`

console.log(process.env.VUE_APP_BACKEND_HOST)
console.log(process.env.VUE_APP_BACKEND_PORT)
Vue.use(VueSweetalert2);

new Vue({
    render: h => h(App), router
}).$mount('#app')
