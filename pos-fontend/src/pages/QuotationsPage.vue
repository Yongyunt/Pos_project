<template>
  <div class="page-bg">
    <div class="main-card">
      <div class="header-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h2 style="margin-bottom: 0; font-size: 2.2rem; font-weight: 700; color: #222; letter-spacing: 1px;">ใบเสนอราคา</h2>
        <button class="btn btn-success" style="font-weight: 600; border-radius: 8px; padding: 0.5rem 1.5rem; font-size: 1.05rem;">สร้างใหม่</button>
      </div>
      <div class="table-container">
        <table class="table table-bordered align-middle">
          <thead>
            <tr>
              <th style="width: 40px"><input type="checkbox" v-model="selectAll" @change="toggleAll" /></th>
              <th>วันที่</th>
              <th>เลขที่เอกสาร</th>
              <th>ชื่อลูกค้า/ชื่อโปรเจ็ค</th>
              <th>ยอดรวมสุทธิ</th>
              <th>สถานะ</th>
              <th style="width: 60px"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quote in quotations" :key="quote.id">
              <td><input type="checkbox" v-model="selected" :value="quote.id" /></td>
              <td>{{ formatDate(quote.date) }}</td>
              <td>{{ quote.id }}</td>
              <td>{{ quote.customer }}</td>
              <td>{{ formatNumber(quote.total) }}</td>
              <td>
                <select v-model="quote.status" class="form-select form-select-sm" style="min-width: 120px">
                  <option value="รออนุมัติ">รออนุมัติ</option>
                  <option value="ดำเนินการแล้ว">ดำเนินการแล้ว</option>
                </select>
              </td>
              <td>
                <button class="btn btn-light btn-sm fs-5"><i class="fas fa-ellipsis-h"></i></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Quotation {
  id: string
  date: string
  customer: string
  total: number
  status: string
}

const quotations = ref<Quotation[]>([
  {
    id: 'QT202505020002',
    date: '2025-05-02',
    customer: 'บี',
    total: 100.00,
    status: 'รออนุมัติ'
  },
  {
    id: 'QT202505020001',
    date: '2025-05-02',
    customer: 'แสน',
    total: 1400.00,
    status: 'ดำเนินการแล้ว'
  },
  {
    id: 'QT202504090001',
    date: '2025-04-09',
    customer: 'นาย A',
    total: 990.00,
    status: 'ดำเนินการแล้ว'
  }
])

const selected = ref<string[]>([])
const selectAll = ref(false)

function toggleAll() {
  if (selectAll.value) {
    selected.value = quotations.value.map(q => q.id)
  } else {
    selected.value = []
  }
}

function formatDate(date: string) {
  // Format YYYY-MM-DD to DD-MM-YYYY
  const [y, m, d] = date.split('-')
  return `${d}-${m}-${y}`
}

function formatNumber(num: number) {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
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
