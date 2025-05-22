<template>
  <div class="quotation-form-page">
    <div class="header-bar">
      <h2>{{ isEditMode ? 'แก้ไขใบเสนอราคา' : 'สร้างใบเสนอราคา' }} <span class="doc-id">{{ formData.id ? `#${formData.id}` : '' }}</span></h2>
      <div class="header-actions">
        <button class="btn btn-outline-secondary me-2" @click="printQuotation">
          <font-awesome-icon icon="print" class="me-1" />
          พิมพ์
        </button>
        <button class="btn btn-outline-secondary" @click="$router.back()">ปิดหน้าต่าง</button>
        <button class="btn btn-success" @click="saveQuotation">บันทึกเอกสาร</button>
      </div>
    </div>
    <div class="main-form">
      <div class="form-section left">
        <div class="form-group">
          <label>ชื่อลูกค้า</label>
          <select class="form-control" v-model="formData.customer">
            <option value="0">เลือกลูกค้า</option>
            <option v-for="contact in customers"
                    :key="contact.id"
                    :value="contact.id">
              {{ contact.name_th }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>ข้อมูลลูกค้า</label>
          <textarea class="form-control" rows="3" placeholder="รายละเอียดที่อยู่"
                    :value="getCustomerAddress"
                    readonly></textarea>
        </div>
      </div>
      <div class="form-section right">
        <div class="form-group">
          <label>จำนวนเงินรวมทั้งสิ้น</label>
          <div class="total-amount">{{ totalAmount }}</div>
        </div>
        <div class="form-group">
          <label>วันที่:</label>
          <input type="date" class="form-control" v-model="formData.quotation_date" />
        </div>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>รายละเอียด:</label>
        <input class="form-control" />
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
            <td> </td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in items" :key="index">
            <td>{{ index + 1 }}</td>
            <td>
              <select class="form-control" v-model="item.product">
                <option value="0">เลือกสินค้า</option>
                <!-- Add product options here -->
              </select>
            </td>
            <td>
              <input class="form-control" type="number" v-model="item.quantity" min="1" />
            </td>
            <td>ชิ้น</td>
            <td>
              <input class="form-control" type="number" v-model="item.price_per_unit" min="0" step="0.01" />
            </td>
            <td>{{ (item.quantity * parseFloat(item.price_per_unit)).toFixed(2) }}</td>
            <td>
              <button class="btn btn-danger btn-sm me-1" @click="deleteRow(index)">
                <font-awesome-icon icon="trash" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="btn btn-outline-primary" @click="addRow">+ เพิ่มแถวรายการ</button>
    </div>

    <!-- Hidden print template -->
    <div id="printTemplate" class="print-template" style="display: none;">
      <div class="print-header">
        <div class="orange-corner"></div>
        <h1>ใบเสนอราคา</h1>
        <div class="quotation-info">
          <div class="info-row">
            <span class="label">เลขที่</span>
            <span class="value">{{ formData.id || '' }}</span>
          </div>
          <div class="info-row">
            <span class="label">วันที่</span>
            <span class="value">{{ formatDate(formData.quotation_date) }}</span>
          </div>
          <div class="info-row">
            <span class="label">ผู้ขาย</span>
            <span class="value">{{ selectedCustomer?.name_th || '' }}</span>
          </div>
        </div>
      </div>

      <div class="print-customer-info">
        <div class="company-info">
          <div>เช็คดีมาได้</div>
          <div>โทร. 0987952658</div>
        </div>
        <div class="customer-details">
          <div class="label">ลูกค้า</div>
          <div>{{ selectedCustomer?.name_th || '' }}</div>
          <div>{{ selectedCustomer?.address || '' }}</div>
        </div>
      </div>

      <table class="print-table">
        <thead>
          <tr>
            <th>#</th>
            <th>รายละเอียด</th>
            <th>จำนวน</th>
            <th>ราคาต่อหน่วย</th>
            <th>ยอดรวม</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in items" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ item.product }}</td>
            <td>{{ item.quantity }} ชิ้น</td>
            <td>{{ formatNumber(parseFloat(item.price_per_unit)) }}</td>
            <td>{{ formatNumber(item.quantity * parseFloat(item.price_per_unit)) }}</td>
          </tr>
        </tbody>
      </table>

      <div class="print-footer">
        <div class="total-section">
          <div class="total-row">
            <span>รวมเป็นเงิน</span>
            <span>{{ formatNumber(parseFloat(totalAmount)) }} บาท</span>
          </div>
          <div class="total-row">
            <span>จำนวนเงินรวมทั้งสิ้น</span>
            <span>{{ formatNumber(parseFloat(totalAmount)) }} บาท</span>
          </div>
          <div class="amount-text">({{ convertToThaiBaht(parseFloat(totalAmount)) }})</div>
        </div>
        <div class="signature-section">
          <div class="signature-box">
            <div>ในนาม {{ selectedCustomer?.name_th || '' }}</div>
            <div class="signature-line">____________________</div>
            <div class="signature-date">วันที่ ____________________</div>
          </div>
          <div class="signature-box">
            <div>ในนาม เช็คดีมาได้</div>
            <div class="signature-line">____________________</div>
            <div class="signature-date">วันที่ ____________________</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuotationStore } from '../stores/quotation'
import { useContactFormStore } from '../stores/Contacts'
import axios from 'axios'

interface Customer {
  id: number
  name_th: string
  name_en: string
  nationality: 'TH' | 'MM'
  phone_number: string
  line_id: string
  viber_name: string
  address: string
}

interface QuotationItem {
  id?: number
  quotation?: number
  product: number
  quantity: number
  price_per_unit: string
  total_price: number
}

interface Quotation {
  id?: number
  customer: number
  quotation_date: string
  total_amount: string
  created_at?: string
  updated_at?: string
  items: QuotationItem[]
}

const route = useRoute()
const router = useRouter()
const quotationStore = useQuotationStore()
const contactStore = useContactFormStore()
const isEditMode = computed(() => route.params.id !== undefined)

const formData = ref<Quotation>({
  customer: 0,
  quotation_date: '',
  total_amount: '0',
  items: []
})

const customers = computed<Customer[]>(() => contactStore.customers)
const selectedCustomer = computed(() => {
  return customers.value.find(c => c.id === formData.value.customer)
})

const items = ref<QuotationItem[]>([])

// Computed property for total amount
const totalAmount = computed(() => {
  return items.value.reduce((sum, item) => {
    return sum + (item.quantity * parseFloat(item.price_per_unit))
  }, 0).toFixed(2)
})

// Watch for changes in items to update total
watch(items, () => {
  formData.value.total_amount = totalAmount.value
}, { deep: true })

// Add computed property for customer address
const getCustomerAddress = computed(() => {
  const customer = selectedCustomer.value
  return customer?.address || ''
})

// Load customers when component mounts
onMounted(async () => {
  try {
    await contactStore.getCustomer()
    if (isEditMode.value) {
      const id = route.params.id
      const data = await quotationStore.getQuotationById(id)
      formData.value = data
      items.value = data.items
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
})

function deleteRow(index: number) {
  items.value.splice(index, 1)
}

function addRow() {
  items.value.push({
    product: 0,
    quantity: 1,
    price_per_unit: '0.00',
    total_price: 0
  })
}

async function saveQuotation() {
  try {
    const data = {
      ...formData.value,
      items: items.value
    }

    if (isEditMode.value) {
      await axios.put(`http://localhost:8000/pos_api/quotations/${route.params.id}/`, data)
    } else {
      await axios.post('http://localhost:8000/pos_api/quotations/', data)
    }
    router.push('/quotations')
  } catch (error) {
    console.error('Error saving quotation:', error)
  }
}

function formatNumber(num: number): string {
  return num.toLocaleString('th-TH', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function formatDate(date: string): string {
  if (!date) return ''
  const [year, month, day] = date.split('-')
  return `${day}/${month}/${year}`
}

// Simple function to convert number to text (basic implementation)
function convertToThaiBaht(amount: number): string {
  const formatter = new Intl.NumberFormat('th-TH', {
    style: 'currency',
    currency: 'THB',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
  return `(${formatter.format(amount)})`
}

async function printQuotation() {
  const printWindow = window.open('', '_blank')
  if (!printWindow) return

  const printContent = document.getElementById('printTemplate')?.innerHTML
  if (!printContent) return

  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>ใบเสนอราคา #${formData.value.id || ''}</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');

        body {
          font-family: 'Sarabun', sans-serif;
          margin: 0;
          padding: 20px;
        }

        .print-template {
          max-width: 210mm;
          margin: 0 auto;
          padding: 20px;
          position: relative;
        }

        .orange-corner {
          position: absolute;
          top: 0;
          right: 0;
          width: 100px;
          height: 100px;
          background: #ff9800;
          clip-path: polygon(100% 0, 0 0, 100% 100%);
        }

        .print-header {
          position: relative;
          margin-bottom: 30px;
        }

        .print-header h1 {
          font-size: 24px;
          margin: 0;
          padding-top: 20px;
        }

        .quotation-info {
          margin-top: 20px;
        }

        .info-row {
          display: flex;
          margin-bottom: 5px;
        }

        .info-row .label {
          width: 80px;
          color: #666;
        }

        .print-customer-info {
          margin-bottom: 30px;
        }

        .company-info {
          margin-bottom: 20px;
        }

        .customer-details .label {
          color: #666;
          margin-bottom: 5px;
        }

        .print-table {
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 30px;
        }

        .print-table th,
        .print-table td {
          border: 1px solid #ddd;
          padding: 8px;
          text-align: center;
        }

        .print-table th {
          background: #f5f5f5;
        }

        .total-section {
          margin-bottom: 40px;
        }

        .total-row {
          display: flex;
          justify-content: space-between;
          margin-bottom: 5px;
        }

        .amount-text {
          text-align: right;
          color: #666;
          font-style: italic;
          margin-top: 5px;
        }

        .signature-section {
          display: flex;
          justify-content: space-between;
          margin-top: 60px;
        }

        .signature-box {
          text-align: center;
          width: 45%;
        }

        .signature-line {
          margin: 40px 0 10px;
        }

        .signature-date {
          margin-top: 20px;
        }

        @media print {
          @page {
            size: A4;
            margin: 10mm;
          }

          body {
            padding: 0;
          }
        }
      </style>
    </head>
    <body>
      <div class="print-template">
        ${printContent}
      </div>
    </body>
    </html>
  `

  printWindow.document.write(htmlContent)
  printWindow.document.close()

  // Wait for fonts and images to load
  setTimeout(() => {
    printWindow.print()
  }, 500)
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
}
.header-bar .doc-id {
  color: #12d8fa;
  font-size: 1.1rem;
  margin-left: 1rem;
}
.header-actions button {
  margin-left: 0.5rem;
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
.form-control {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ddd;
  font-size: 1rem;
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
.btn-outline-primary {
  margin-top: 0.5rem;
}
.footer-section {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  margin-top: 2rem;
}
.footer-left, .footer-right {
  flex: 1;
}
.footer-right {
  text-align: right;
  font-size: 1.1rem;
}

label,
input,
select,
textarea {
  font-family: 'Sarabun', 'Prompt', 'Kanit', Arial, Tahoma, sans-serif !important;
  font-size: 1.08rem;
}

label {
  font-weight: 600;
  color: #222;
}

input,
select,
textarea {
  font-weight: 500;
  color: #222;
}

.print-template {
  display: none;
}

.me-1 {
  margin-right: 0.25rem;
}

.me-2 {
  margin-right: 0.5rem;
}
</style>
