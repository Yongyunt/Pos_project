<template>
  <div class="quotation-form-page">
    <div class="header-bar">
      <h2>รายละเอียดใบเสนอราคา <span class="doc-id">{{ quotation?.id ? `#${quotation.id}` : '' }}</span></h2>
      <div class="header-actions">
        <button class="btn btn-outline-secondary" @click="$router.back()">ปิดหน้าต่าง</button>
        <button class="btn btn-primary" @click="editQuotation">แก้ไข</button>
      </div>
    </div>

    <div class="main-form" v-if="quotation">
      <div class="form-section left">
        <div class="form-group">
          <label>ชื่อลูกค้า</label>
          <div class="form-control-static">{{ quotation.customer }}</div>
        </div>
        <div class="form-group">
          <label>ข้อมูลลูกค้า</label>
          <div class="form-control-static">-</div>
        </div>
      </div>
      <div class="form-section right">
        <div class="form-group">
          <label>จำนวนเงินรวมทั้งสิ้น</label>
          <div class="total-amount">{{ formatNumber(parseFloat(quotation.total_amount)) }}</div>
        </div>
        <div class="form-group">
          <label>วันที่:</label>
          <div class="form-control-static">{{ formatDate(quotation.quotation_date) }}</div>
        </div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label>รายละเอียด:</label>
        <div class="form-control-static">-</div>
      </div>
    </div>

    <div class="table-section">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ลำดับ</th>
            <th>ชื่อสินค้า / รายละเอียด</th>
            <th>จำนวน</th>
            <th>หน่วย</th>
            <th>ราคาต่อหน่วย</th>
            <th>ราคารวม</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in quotation?.items" :key="item.id">
            <td>{{ index + 1 }}</td>
            <td>{{ item.product }}</td>
            <td>{{ item.quantity }}</td>
            <td>ชิ้น</td>
            <td>{{ formatNumber(parseFloat(item.price_per_unit)) }}</td>
            <td>{{ formatNumber(item.total_price) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!quotation" class="loading">
      กำลังโหลดข้อมูล...
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuotationStore } from '../stores/quotation'

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
}

const route = useRoute()
const router = useRouter()
const quotationStore = useQuotationStore()
const quotation = ref<Quotation | null>(null)

onMounted(async () => {
  try {
    const id = route.params.id
    const data = await quotationStore.getQuotationById(id)
    quotation.value = data
  } catch (error) {
    console.error('Error loading quotation:', error)
  }
})

function formatDate(date: string) {
  if (!date) return '-'
  try {
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

function editQuotation() {
  router.push(`/quotations/${route.params.id}/edit`)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');

.quotation-form-page {
  font-family: 'Sarabun', 'Prompt', 'Kanit', Arial, Tahoma, sans-serif;
  background: #f7fafd;
  padding: 2rem;
  border-radius: 12px;
  max-width: 1200px;
  margin: 2rem auto;
  box-shadow: 0 2px 12px #0001;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header-bar h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #222;
  margin: 0;
}

.doc-id {
  color: #12d8fa;
  font-size: 1.1rem;
  margin-left: 1rem;
}

.main-form {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.form-section.left, .form-section.right {
  flex: 1;
}

.form-group {
  margin-bottom: 1rem;
}

.form-control-static {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ddd;
  font-size: 1rem;
  background-color: #f8f9fa;
  color: #222;
}

.total-amount {
  font-size: 2rem;
  color: #12d8fa;
  font-weight: 700;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.table-section {
  margin-bottom: 1.5rem;
}

.table th, .table td {
  vertical-align: middle;
  text-align: center;
}

.table th {
  background: #f8f9fa;
  font-weight: 600;
}

label {
  font-weight: 600;
  color: #222;
  margin-bottom: 0.5rem;
  display: block;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.header-actions button {
  margin-left: 0.5rem;
}
</style>
