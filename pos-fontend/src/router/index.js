import { createRouter, createWebHistory } from 'vue-router'
import CashSalePage from '../pages/CashSalePage.vue'
import Dashboard from '../pages/Dashboard.vue'
import CustomersPage from '../pages/CustomersPage.vue'
import CustomerFormPage from '../pages/CustomerFormPage.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/cash-sale',
    name: 'CashSale',
    component: CashSalePage,
  },
  {
    path: '/customers',
    name: 'Customers',
    component: CustomersPage,
  },
  {
    path: '/customers/new',
    name: 'CustomerForm',
    component: CustomerFormPage,
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
