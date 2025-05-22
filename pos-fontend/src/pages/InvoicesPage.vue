<template>
  <div class="page-bg">
    <div class="main-card">
      <div class="header-bar">
        <h2>ใบแจ้งหนี้</h2>
        <button class="btn btn-success">สร้างใบแจ้งหนี้ใหม่</button>
      </div>
      <div class="table-container">
        <table class="table table-bordered align-middle">
          <thead>
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
            <tr v-for="invoice in invoices" :key="invoice.id">
              <td>{{ invoice.id }}</td>
              <td>{{ invoice.date }}</td>
              <td>{{ invoice.customer }}</td>
              <td>฿{{ invoice.total.toFixed(2) }}</td>
              <td>
                <span :class="['badge fs-6',
                  invoice.status === 'รอชำระ' ? 'bg-warning text-dark' :
                  invoice.status === 'ชำระแล้ว' ? 'bg-success' :
                  'bg-danger']">
                  {{ invoice.status }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-2">
                  <button class="btn btn-light btn-sm">
                    <eye-icon style="width: 16px; height: 16px;" />
                  </button>
                  <button class="btn btn-light btn-sm">
                    <pencil-icon style="width: 16px; height: 16px;" />
                  </button>
                  <button class="btn btn-light btn-sm">
                    <trash-icon style="width: 16px; height: 16px;" />
                  </button>
                </div>
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
import { EyeIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline'

interface Invoice {
  id: string
  date: string
  customer: string
  total: number
  status: 'รอชำระ' | 'ชำระแล้ว' | 'ค้างชำระ'
}

const invoices = ref<Invoice[]>([
  {
    id: 'INV001',
    date: '2024-03-20',
    customer: 'บริษัท ตัวอย่าง จำกัด',
    total: 15000,
    status: 'รอชำระ'
  },
  {
    id: 'INV002',
    date: '2024-03-19',
    customer: 'บริษัท ทดสอบ จำกัด',
    total: 25000,
    status: 'ชำระแล้ว'
  },
  // Add more sample data as needed
])
</script>
