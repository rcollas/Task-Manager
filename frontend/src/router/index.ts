import { createRouter, createWebHistory } from 'vue-router'
import Tasks from '@/components/TasksComponent.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/tasks',
            name: 'tasks',
            component: Tasks
        }
    ]
})

export default router
