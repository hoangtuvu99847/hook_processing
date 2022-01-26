import Dashboard from "@/pages/dashboard/Dashboard";
import Detail from "@/pages/detail/Detail";
import Resouces from "@/pages/detail/Resources/Resources"
import Process from "@/pages/detail/Process/Process"

export const routes = [
    {path: '/', component: Dashboard, name: ''},
    {
        path: '/detail/:id',
        component: Detail,
        children: [
            {
                path: 'resources',
                component: Resouces,
                name: 'resources'
            },
            {
                path: 'process',
                component: Process,
                name: 'process'
            },
        ],
        name: 'detail', props: true
    }
]
