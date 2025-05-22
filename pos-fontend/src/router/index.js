import { createRouter, createWebHistory } from 'vue-router'
import ProductsPage from '../pages/ProductsPage.vue'
import Contactbook from '../pages/ContactBook.vue'
import ContactBookFormPage from '../pages/ContactBookFormPage.vue'
import QuotationsPage from '../pages/QuotationsPage.vue'
import ReceiptsPage from '../pages/ReceiptsPage.vue'
import SalesPage from '../pages/SalesPage.vue'
import Dashboard from '../pages/DashboardPage.vue'



const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/products',
    name: 'Products',
    component: ProductsPage,
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
  {
    path: '/quotations',
    name: 'Quotations',
    component: QuotationsPage,
  },
  {
    path: '/receipts',
    name: 'Receipts',
    component: ReceiptsPage,
  },
  {
    path: '/sales',
    name: 'Sales',
    component: SalesPage,
  },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
