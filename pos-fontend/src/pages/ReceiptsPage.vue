<template>
  <div class="bg-white rounded shadow-sm p-5">
    <div class="mb-4 d-flex justify-content-between align-items-center">
      <h2 class="fs-4 fw-semibold mb-0">ใบเสร็จรับเงิน</h2>
      <button class="btn btn-primary fs-5 px-4 py-2">สร้างใบเสร็จใหม่</button>
    </div>
    <div class="table-responsive">
      <table class="table table-bordered align-middle fs-5">
        <thead class="table-light">
          <tr>
            <th>เลขที่</th>
            <th>วันที่</th>
            <th>ลูกค้า</th>
            <th>ยอดรวม</th>
            <th>วิธีชำระเงิน</th>
            <th>การจัดการ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="receipt in receipts" :key="receipt.id">
            <td>{{ receipt.id }}</td>
            <td>{{ receipt.date }}</td>
            <td>{{ receipt.customer }}</td>
            <td>฿{{ receipt.total.toFixed(2) }}</td>
            <td>{{ receipt.paymentMethod }}</td>
            <td>
              <div class="d-flex gap-2">
                <button class="btn btn-light btn-sm">
                  <eye-icon style="width: 16px; height: 16px;" />
                </button>
                <button class="btn btn-light btn-sm">
                  <printer-icon style="width: 16px; height: 16px;" />
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
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { EyeIcon, PrinterIcon, TrashIcon } from '@heroicons/vue/24/outline'

interface Receipt {
  id: string
  date: string
  customer: string
  total: number
  paymentMethod: string
}

const receipts = ref<Receipt[]>([
  {
    id: 'RCP001',
    date: '2024-03-20',
    customer: 'บริษัท ตัวอย่าง จำกัด',
    total: 15000,
    paymentMethod: 'โอนเงิน'
  },
  {
    id: 'RCP002',
    date: '2024-03-19',
    customer: 'บริษัท ทดสอบ จำกัด',
    total: 25000,
    paymentMethod: 'เงินสด'
  },
  // Add more sample data as needed
])
</script>
