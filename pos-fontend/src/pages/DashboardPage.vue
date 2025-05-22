<script setup lang="ts">
import { ref, computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

defineOptions({
  name: 'DashboardPage'
})

// Mock data - Replace with actual data from your API
const salesData = ref({
  dailySales: 25000,
  monthlySales: 750000,
  dailyBills: 45,
  dailyProfit: 5000,
  monthlyProfit: 150000
})

const productSales = ref([
  { name: 'เตาโล่', value: 2450 },
  { name: 'ไม้กวาด', value: 520 }
])

const productSalesTotal = computed(() =>
  productSales.value.reduce((sum, item) => sum + item.value, 0)
)

const doughnutData = computed(() => ({
  labels: productSales.value.map(item => item.name),
  datasets: [
    {
      data: productSales.value.map(item => item.value),
      backgroundColor: ['#4A90E2', '#357ABD'],
      borderWidth: 2
    }
  ]
}))

const doughnutOptions = {
  cutout: '70%',
  plugins: {
    legend: { display: false },
    tooltip: { enabled: true }
  }
}
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Daily Sales Card -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">ยอดขายวันนี้</p>
            <h2 class="card-amount">฿{{ salesData.dailySales.toLocaleString() }}</h2>
          </div>
          <div class="text-3xl">💰</div>
        </div>
      </div>

      <!-- Monthly Sales Card -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">ยอดขายเดือนนี้</p>
            <h2 class="card-amount">฿{{ salesData.monthlySales.toLocaleString() }}</h2>
          </div>
          <div class="text-3xl">📈</div>
        </div>
      </div>

      <!-- Daily Bills Card -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">จำนวนบิลวันนี้</p>
            <h2 class="card-amount">{{ salesData.dailyBills }} บิล</h2>
          </div>
          <div class="text-3xl">🧾</div>
        </div>
      </div>

      <!-- Daily Profit Card -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">กำไรวันนี้</p>
            <h2 class="card-amount">฿{{ salesData.dailyProfit.toLocaleString() }}</h2>
          </div>
          <div class="text-3xl">💰</div>
        </div>
      </div>

      <!-- Monthly Profit Card -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">กำไรเดือนนี้</p>
            <h2 class="card-amount">฿{{ salesData.monthlyProfit.toLocaleString() }}</h2>
          </div>
          <div class="text-3xl">📈</div>
        </div>
      </div>
    </div>

    <!-- กราฟยอดขายตามสินค้า -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
        <div class="flex items-center gap-2 mb-2 md:mb-0">
          <span class="text-lg font-semibold text-blue-700">ยอดขายตามสินค้า</span>
          <span class="text-blue-400 cursor-pointer" title="ดูยอดขายแยกตามสินค้า">ℹ️</span>
        </div>
        <div class="flex items-center gap-2">
          <select class="border rounded px-2 py-1 text-sm">
            <option>3 เดือน</option>
            <option>6 เดือน</option>
            <option>12 เดือน</option>
          </select>
          <button class="border rounded px-2 py-1 text-sm"><i class="fas fa-list"></i></button>
        </div>
      </div>
      <div class="flex flex-col md:flex-row md:items-center gap-8">
        <div class="w-full md:w-1/2 chart-container">
          <Doughnut :data="doughnutData" :options="doughnutOptions" style="max-width: 300px;" />
        </div>
        <div class="w-full md:w-1/2 flex flex-col justify-center items-center md:items-start">
          <div class="mb-2 flex items-center gap-2">
            <span class="inline-block w-3 h-3 rounded-full bg-blue-500"></span>
            <span class="font-semibold">รายได้รวม:</span>
            <span class="text-blue-600 font-bold text-lg">{{ productSalesTotal.toLocaleString(undefined, { minimumFractionDigits: 2 }) }}</span>
          </div>
          <div v-for="item in productSales" :key="item.name" class="flex items-center gap-2 mb-1">
            <span class="inline-block w-3 h-3 rounded-full" :style="{ backgroundColor: item.name === 'เตาโล่' ? '#4A90E2' : '#357ABD' }"></span>
            <span>{{ item.name }}</span>
            <span class="ml-4 text-blue-600">{{ item.value.toLocaleString(undefined, { minimumFractionDigits: 2 }) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@700&family=Sarabun:wght@400;600&display=swap');

.bg-white {
  background-color: #fff;
}
.p-6 {
  padding: 2rem;
}

h1 {
  font-family: 'Kanit', 'Sarabun', Arial, sans-serif;
  color: #2c3e50;
  letter-spacing: 1px;
}

.grid > div {
  transition: box-shadow 0.2s, transform 0.2s;
}
.grid > div:hover {
  box-shadow: 0 6px 24px 0 #4a90e233, 0 1.5px 6px 0 #4a90e222;
  transform: translateY(-2px) scale(1.02);
}

.bg-white.rounded-lg.shadow-md {
  border-radius: 18px;
  box-shadow: 0 2px 16px #0001;
  border: 1px solid #f0f4fa;
}

.text-gray-500 {
  color: #8ca0b3;
  font-family: 'Sarabun', Arial, sans-serif;
}
.text-blue-700 {
  color: #2563eb;
}
.text-blue-400 {
  color: #60a5fa;
}
.text-blue-600 {
  color: #2563eb;
}
.font-bold {
  font-weight: 700;
  font-family: 'Kanit', 'Sarabun', Arial, sans-serif;
}
.font-semibold {
  font-weight: 600;
  font-family: 'Kanit', 'Sarabun', Arial, sans-serif;
}

select, button {
  outline: none;
  border: 1px solid #e3e8f0;
  background: #f8fafc;
  transition: border 0.2s, box-shadow 0.2s;
  font-family: 'Sarabun', Arial, sans-serif;
}
select:focus, button:focus {
  border: 1.5px solid #4a90e2;
  box-shadow: 0 0 0 2px #4a90e222;
}

button {
  cursor: pointer;
}

/* Card icon style */
.text-3xl {
  font-size: 2.2rem;
  color: #4a90e2;
  background: #f4f8fb;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px #4a90e211;
}

/* Donut chart section */
.bg-white.rounded-lg.shadow-md.p-6.mb-8 {
  border-radius: 18px;
  box-shadow: 0 2px 16px #4a90e211;
  border: 1px solid #e3e8f0;
}

.flex.items-center.gap-2.mb-2.md\:mb-0 span[title] {
  font-size: 1.1rem;
}

select {
  min-width: 100px;
  border-radius: 8px;
  padding: 0.25rem 0.75rem;
  font-size: 1rem;
}

button {
  border-radius: 8px;
  padding: 0.25rem 0.75rem;
  font-size: 1rem;
  background: #f4f8fb;
  color: #2563eb;
}
button:hover {
  background: #e3f0ff;
}

/* Chart container for symmetry and centering */
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 320px;
  min-width: 220px;
  margin: 0 auto;
  height: 320px;
}

/* Responsive tweaks */
@media (max-width: 768px) {
  .p-6 {
    padding: 1rem;
  }
  .grid {
    gap: 1rem;
  }
  .bg-white.rounded-lg.shadow-md.p-6.mb-8 {
    padding: 1rem;
  }
  .chart-container {
    max-width: 220px;
    height: 220px;
  }
}

.card-amount {
  color: #222;
  font-size: 2.6rem;
  font-weight: 800;
  font-family: 'Kanit', 'Sarabun', Arial, sans-serif;
  letter-spacing: 1px;
  text-shadow: 0 2px 8px #0001;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
