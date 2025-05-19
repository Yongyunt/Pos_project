<template>
  <div class="bg-white rounded shadow-sm p-5">
    <div class="mb-4 d-flex justify-content-between align-items-center">
      <h2 class="fs-4 fw-semibold mb-0">ใบเสนอราคา</h2>
      <button class="btn btn-primary fs-5 px-4 py-2">สร้างใบเสนอราคาใหม่</button>
    </div>
    <div class="table-responsive">
      <table class="table table-bordered align-middle fs-5">
        <thead class="table-light">
          <tr>
            <th>เลขที่</th>
            <th>วันที่</th>
            <th>ลูกค้า</th>
            <th>ยอดรวม</th>
            <th>สถานะ</th>
            <th>การจัดการ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="quote in quotations" :key="quote.id">
            <td>{{ quote.id }}</td>
            <td>{{ quote.date }}</td>
            <td>{{ quote.customer }}</td>
            <td>฿{{ quote.total.toFixed(2) }}</td>
            <td>
              <span :class="['badge fs-6',
                quote.status === 'รอดำเนินการ' ? 'bg-warning text-dark' :
                quote.status === 'อนุมัติแล้ว' ? 'bg-success' :
                'bg-secondary']">
                {{ quote.status }}
              </span>
            </td>
            <td>
              <button class="btn btn-light btn-sm fs-5"><i class="fas fa-ellipsis-h"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
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
  status: 'รอดำเนินการ' | 'อนุมัติแล้ว' | 'ยกเลิก'
}

const quotations = ref<Quotation[]>([
  {
    id: 'QT001',
    date: '2024-03-20',
    customer: 'บริษัท ตัวอย่าง จำกัด',
    total: 15000,
    status: 'รอดำเนินการ'
  },
  {
    id: 'QT002',
    date: '2024-03-19',
    customer: 'บริษัท ทดสอบ จำกัด',
    total: 25000,
    status: 'อนุมัติแล้ว'
  },
  // Add more sample data as needed
])
</script>
