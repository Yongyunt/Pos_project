import { createRouter, createWebHistory } from 'vue-router'
import SalesPage from '../pages/SalesPage.vue'
import QuotationsPage from '../pages/QuotationsPage.vue'
import InvoicesPage from '../pages/InvoicesPage.vue'
import ReceiptsPage from '../pages/ReceiptsPage.vue'
import CashSalePage from '../pages/CashSalePage.vue'

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
      path: '/cash-sale',
      name: 'cash-sale',
      component: CashSalePage
    },
  ]
})

export default router
