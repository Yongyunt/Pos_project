<template>
  <div class="container my-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>ใบเสร็จรับเงิน (เงินสด)</h2>
      <div>
        <button class="btn btn-primary me-2" @click="importData">นำเข้าข้อมูล</button>
        <button class="btn btn-success" @click="openSaleForm">สร้างใหม่</button>
      </div>
    </div>
    <div class="mb-3">
      <div class="input-group" style="max-width: 300px;">
        <input type="text" v-model="searchQuery" class="form-control" placeholder="แสดงทั้งหมด" />
        <button class="btn btn-primary">
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-bordered align-middle">
        <thead class="table-light">
          <tr>
            <th><input type="checkbox" v-model="selectAll" @change="toggleSelectAll"></th>
            <th>วันที่</th>
            <th>เลขที่เอกสาร</th>
            <th>ชื่อลูกค้า/ชื่อโปรเจ็ค</th>
            <th class="text-end">ยอดรวมสุทธิ</th>
            <th>สถานะ</th>
            <th>การดำเนินการ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in transactions" :key="item.id">
            <td><input type="checkbox" v-model="item.selected"></td>
            <td>{{ item.date }}</td>
            <td>
              {{ item.documentNo }}
              <i v-if="item.hasAttachment" class="fas fa-paperclip"></i>
            </td>
            <td>{{ item.customerName }}</td>
            <td class="text-end">{{ formatNumber(item.total) }}</td>
            <td>
              <select v-model="item.status" class="form-select">
                <option value="pending">รอดำเนินการ</option>
                <option value="completed">เสร็จสิ้น</option>
              </select>
            </td>
            <td>
              <button class="btn btn-light me-2">
                <i class="fas fa-ellipsis-h"></i>
              </button>
              <button class="btn btn-danger" @click="deleteTransaction(item.id)">
                <font-awesome-icon icon="trash" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="d-flex justify-content-between align-items-center mt-3">
      <div>
        รายการต่อหน้า:
        <select v-model="itemsPerPage" class="form-select d-inline-block w-auto ms-2">
          <option value="20">20</option>
          <option value="50">50</option>
          <option value="100">100</option>
        </select>
      </div>
      <div>
        <!-- Pagination components will go here -->
      </div>
    </div>
    <!-- SaleForm Modal -->
    <div v-if="showSaleForm" class="modal-backdrop-custom">
      <div class="modal-custom">
        <SaleForm @close="closeSaleForm" />
        <button class="btn btn-outline-secondary mt-3 w-100" @click="closeSaleForm">ปิดหน้าต่าง</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import  SaleForm  from '../components/sale/SaleForm.vue'

interface Transaction {
  id: number;
  date: string;
  documentNo: string;
  customerName: string;
  total: number;
  status: 'pending' | 'completed';
  hasAttachment: boolean;
  selected: boolean;
}

export default defineComponent({
  name: 'CashSalePage',
  components: { SaleForm },
  setup() {
    const showSaleForm = ref(false)
    const openSaleForm = () => { showSaleForm.value = true }
    const closeSaleForm = () => { showSaleForm.value = false }
    return { showSaleForm, openSaleForm, closeSaleForm }
  },
  data() {
    return {
      searchQuery: '',
      selectAll: false,
      itemsPerPage: 20,
      transactions: [
        {
          id: 1,
          date: '02-05-2025',
          documentNo: 'CA20250502002',
          customerName: 'แสน',
          total: 1400.00,
          status: 'pending',
          hasAttachment: true,
          selected: false
        },
        {
          id: 2,
          date: '02-05-2025',
          documentNo: 'CA20250502001',
          customerName: 'นาย A',
          total: 990.00,
          status: 'pending',
          hasAttachment: true,
          selected: false
        },
        // Add more sample data as needed
      ] as Transaction[]
    }
  },
  methods: {
    toggleSelectAll(): void {
      this.transactions.forEach(item => {
        item.selected = this.selectAll
      })
    },
    formatNumber(num: number): string {
      return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    },
    importData(): void {
      // Implement import functionality
    },
    createNew(): void {
      // Implement create new functionality
    },
    deleteTransaction(id: number): void {
      if (window.confirm('คุณต้องการลบรายการนี้หรือไม่?')) {
        this.transactions = this.transactions.filter(item => item.id !== id)
      }
    }
  }
})
</script>

<style scoped>
.container {
  font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h2 {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 0;
}

.table {
  font-size: 0.95rem;
}

.table th {
  font-weight: 600;
  color: #2c3e50;
  background-color: #f8f9fa !important;
}

.table td {
  color: #2c3e50;
  vertical-align: middle;
}

.form-control, .form-select {
  font-size: 0.95rem;
}

.btn {
  font-weight: 500;
}

/* Improve number formatting clarity */
.text-end {
  font-family: 'Sarabun', monospace;
  font-weight: 500;
}

/* Improve status select clarity */
.form-select {
  min-width: 120px;
  font-weight: 500;
}

/* Improve search input clarity */
.input-group .form-control {
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
}

/* Improve pagination text clarity */
select.form-select {
  font-size: 0.9rem;
  padding: 0.25rem 2rem 0.25rem 0.5rem;
}

/* Improve table header alignment */
.table thead th {
  white-space: nowrap;
  padding: 0.75rem 1rem;
}

/* Improve table cell padding */
.table td {
  padding: 0.75rem 1rem;
}

/* Improve document number clarity */
td:nth-child(3) {
  font-family: 'Sarabun', monospace;
  font-weight: 500;
}

/* Improve customer name clarity */
td:nth-child(4) {
  font-weight: 500;
}

/* Improve action button clarity */
.btn-light {
  padding: 0.375rem 0.75rem;
}

/* Improve checkbox alignment */
input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  margin-top: 0.2rem;
}

.modal-backdrop-custom {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.25);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-custom {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px #0002;
  padding: 2rem;
  max-width: 1100px;
  width: 95vw;
  max-height: 95vh;
  overflow-y: auto;
}
</style>
