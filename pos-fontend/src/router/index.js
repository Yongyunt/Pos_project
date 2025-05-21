import { createRouter, createWebHistory } from 'vue-router'
import CashSalePage from '../pages/CashSalePage.vue'
import Dashboard from '../pages/Dashboard.vue'
import Contactbook from '../pages/ContactBook.vue'
import ContactBookFormPage from '../pages/ContactBookFormPage.vue'

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
    path: '/contactbook',
    name: 'Contactbook',
    component: Contactbook,
  },
  {
    path: '/contactbook/new',
    name: 'ContactBookForm',
    component: ContactBookFormPage,
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
