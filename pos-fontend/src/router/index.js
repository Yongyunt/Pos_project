import { createRouter, createWebHistory } from 'vue-router'
import CashSalePage from '../pages/CashSalePage.vue' // ✅ ใช้ path ปกติ (ไม่ใช่ '@/')


const routes = [
  {
    path: '/cash-sale',
    name: 'CashSale',
    component: CashSalePage,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
