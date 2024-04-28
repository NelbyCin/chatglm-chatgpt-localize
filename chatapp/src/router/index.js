import { createRouter, createWebHistory } from 'vue-router'

const routes = [

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
}) // history模式启动，不需刷新即可变化

export default router
