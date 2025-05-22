<template>
  <div class="page-bg">
    <div class="main-card">
      <div class="header-bar">
        <h2>ใบเสร็จรับเงิน</h2>
        <button class="btn btn-success">สร้างใบเสร็จใหม่</button>
      </div>
      <div class="table-container">
        <table class="table table-bordered align-middle">
          <thead>
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

<style scoped>
.page-bg {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem;
}

.main-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.header-bar h2 {
  margin: 0;
  color: #2c3e50;
  font-weight: 600;
}

.table-container {
  overflow-x: auto;
}

.table {
  margin-bottom: 0;
}

.table thead th {
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
  color: #495057;
  font-weight: 600;
  padding: 1rem;
}

.table tbody td {
  padding: 1rem;
  vertical-align: middle;
}

.btn-success {
  background-color: #28a745;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-success:hover {
  background-color: #218838;
  transform: translateY(-1px);
}

.btn-light {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  transition: all 0.2s;
}

.btn-light:hover {
  background-color: #e9ecef;
  transform: translateY(-1px);
}

.gap-2 {
  gap: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-bg {
    padding: 1rem;
  }

  .main-card {
    padding: 1rem;
  }

  .header-bar {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>
