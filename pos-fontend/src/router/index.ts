import { createRouter, createWebHistory } from 'vue-router'
import QuotationsPage from '../pages/QuotationsPage.vue'
import InvoicesPage from '../pages/InvoicesPage.vue'
import ReceiptsPage from '../pages/ReceiptsPage.vue'
import SalesPage from '../pages/SalesPage.vue'
import Dashboard from '../pages/DashboardPage.vue'
import ProductsPage from '../pages/ProductsPage.vue'
import ContactBook from '../pages/ContactBook.vue'
import ContactBookFormPage from '../pages/ContactBookFormPage.vue'
import ReportsPage from '../pages/ReportsPage.vue'


const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/sales',
      name: 'sales',
      component: SalesPage
    },
    {
      path: '/quotations',
      name: 'quotations',
      component: QuotationsPage
    },
    {
      path: '/invoices',
      name: 'invoices',
      component: InvoicesPage
    },
    {
      path: '/receipts',
      name: 'receipts',
      component: ReceiptsPage
    },
    {
      path: '/products',
      name: 'products',
      component: ProductsPage
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/contactbook',
      name: 'contactbook',
      component: ContactBook
    },
    {
      path: '/contactbook/form',
      name: 'contactbook-form',
      component: ContactBookFormPage
    },
    {
      path: '/reports',
      name: 'reports',
      component: ReportsPage
    }
  ]
})

export default router
