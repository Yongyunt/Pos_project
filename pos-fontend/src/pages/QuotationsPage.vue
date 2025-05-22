<template>
  <div class="page-bg">
    <div class="main-card">
      <div class="header-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h2 style="margin-bottom: 0; font-size: 2.2rem; font-weight: 700; color: #222; letter-spacing: 1px;">ใบเสนอราคา</h2>
        <router-link to="/quotations/new" class="btn btn-success" style="font-weight: 600; border-radius: 8px; padding: 0.5rem 1.5rem; font-size: 1.05rem;">สร้างใหม่</router-link>
      </div>
      <div class="table-container">
        <table class="table table-bordered align-middle">
          <thead>
            <tr>
              <th style="width: 40px"><input type="checkbox" v-model="selectAll" @change="toggleAll" /></th>
              <th>วันที่</th>
              <th>เลขที่เอกสาร</th>
              <th>ชื่อลูกค้า</th>
              <th>ยอดรวมสุทธิ</th>
              <th>สถานะ</th>
              <th style="width: 60px"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quote in quotations" :key="quote.id">
              <td><input type="checkbox" v-model="selected" :value="quote.id" /></td>
              <td>{{ formatDate(quote.quotation_date) }}</td>
              <td>
                <a href="#" @click.prevent="viewQuotationDetail(quote.id)" class="text-primary">
                  {{ quote.id }}
                </a>
              </td>
              <td>{{ quote.customer }}</td>
              <td>{{ formatNumber(parseFloat(quote.total_amount)) }}</td>
              <td>
                <select v-model="quote.status" class="form-select form-select-sm" style="min-width: 120px">
                  <option value="รออนุมัติ">รออนุมัติ</option>
                  <option value="ดำเนินการแล้ว">ดำเนินการแล้ว</option>
                </select>
              </td>
              <td>
                <button class="btn btn-danger btn-sm me-1" @click="deleteQuotation(quote.id)">
                    <font-awesome-icon icon="trash" />
                  </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuotationStore } from '../stores/quotation'
import { useRouter } from 'vue-router'

interface QuotationItem {
  id: number
  quotation: number
  product: number
  quantity: number
  price_per_unit: string
  total_price: number
}

interface Quotation {
  id: number
  customer: number
  quotation_date: string
  total_amount: string
  created_at: string
  updated_at: string
  items: QuotationItem[]
  status?: string  // Optional status field
}

const quotationStore = useQuotationStore()
const router = useRouter()
const quotations = ref<Quotation[]>([])
const selected = ref<number[]>([])  // Changed to number[] since id is number
const selectAll = ref(false)

onMounted(async () => {
  await quotationStore.getQuotations()
  quotations.value = quotationStore.quotations.map((quote: Quotation) => ({
    ...quote,
    status: 'รออนุมัติ'  // Set default status
  }))
})

function toggleAll() {
  if (selectAll.value) {
    selected.value = quotations.value.map(q => q.id)
  } else {
    selected.value = []
  }
}

function formatDate(date: string) {
  if (!date) return '-'
  try {
    // Format YYYY-MM-DD to DD-MM-YYYY
    const [y, m, d] = date.split('-')
    if (!y || !m || !d) return '-'
    return `${d}-${m}-${y}`
  } catch (error) {
    console.error('Error formatting date:', error)
    return '-'
  }
}

function formatNumber(num: number) {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function deleteQuotation(id: number) {
  if (confirm('คุณต้องการลบรายการนี้ใช่หรือไม่?')) {
    quotations.value = quotations.value.filter(quote => quote.id !== id)
  }
}

function viewQuotationDetail(id: number) {
  router.push(`/quotations/${id}`)
}
</script>

<style scoped>
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.header-bar h2 {
  margin-bottom: 0;
  font-size: 2.2rem;
  font-weight: 700;
  color: #222;
  letter-spacing: 1px;
}
.btn-success {
  font-weight: 600;
  border-radius: 8px;
  padding: 0.5rem 1.5rem;
  font-size: 1.05rem;
  box-shadow: 0 2px 8px #12d8fa22;
  transition: background 0.2s;
}
.btn-success:hover {
  background: #12d8fa;
  color: #fff;
}
.table-container {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 6px #0001;
  background: #fff;
}
.table th, .table td {
  vertical-align: middle;
}
.table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #222;
  font-size: 1.05rem;
}
.table td {
  color: #222;
  font-size: 1rem;
}
input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: #12d8fa;
  margin-top: 0.2rem;
}
select.form-select-sm {
  min-width: 120px;
  font-size: 1rem;
  border-radius: 6px;
  padding: 0.25rem 0.75rem;
}
.btn-light.btn-sm.fs-5 {
  border-radius: 6px;
  font-size: 1.1rem;
  color: #555;
  transition: background 0.2s;
}
.btn-light.btn-sm.fs-5:hover {
  background: #e3f6ff;
  color: #12d8fa;
}
</style>
