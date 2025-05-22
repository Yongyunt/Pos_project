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
import QuotationsForm from '../pages/QuotationsForm.vue'
import QuotationDetail from '../pages/QuotationDetail.vue'

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
      path: '/quotations/new',
      name: 'quotations-new',
      component: () => import('../pages/QuotationsForm.vue')
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
    },
    {
      path: '/quotations/:id',
      name: 'quotation-detail',
      component: QuotationDetail
    },
    {
      path: '/quotations/:id/edit',
      name: 'quotation-edit',
      component: QuotationsForm
    }
  ]
})

export default router
