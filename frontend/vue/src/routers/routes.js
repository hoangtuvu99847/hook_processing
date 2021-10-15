import Dashboard from "@/pages/dashboard/Dashboard";
import Detail from "@/pages/detail/Detail";

export const routes = [
    { path: '/', component: Dashboard, name: '' },
    { path: '/detail/:id', component: Detail, name: 'detail', props: true }
]
