<template>
  <div class="page-bg">
    <div class="main-card">
      <div class="header-bar">
        <div>
          <h2>สมุดรายชื่อ</h2>
          <div class="subtitle">สมุดรายชื่อ</div>
        </div>
        <div>
          <!-- <button class="btn btn-primary me-2" @click="importData">นำเข้าข้อมูล</button> -->
          <button class="btn btn-success" @click="openSaleForm">สร้างใหม่</button>
        </div>
      </div>

      <el-tabs v-model="activeTab" class="mb-2 pretty-tabs">
        <el-tab-pane label="แสดงทั้งหมด" name="all" />
        <el-tab-pane label="ลูกค้า" name="customer" />
        <el-tab-pane label="ผู้จำหน่าย" name="supplier" />
        <el-tab-pane label="ผู้จำหน่าย/ลูกค้า" name="both" />
      </el-tabs>

      <el-input
        v-model="search"
        placeholder="ค้นหารายชื่อ หรือรหัสผู้ติดต่อ"
        prefix-icon="el-icon-search"
        class="mb-4 pretty-search"
        clearable
      />

      <div class="table-container">
        <table class="customer-table">
          <thead>
            <tr>
              <th>รายชื่อ</th>
              <th>ชื่อผู้ติดต่อ</th>
              <th>เบอร์ติดต่อ</th>
              <th>อีเมล</th>
              <th>ประเภท</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr class="group-row">
              <td colspan="6"><b>Cash Sale / ขายเงินสด</b></td>
            </tr>
            <tr>
              <td>ขายยย</td>
              <td>แสน</td>
              <td></td>
              <td></td>
              <td>ลูกค้า</td>
              <td>
                <button class="btn btn-warning btn-sm me-1" @click="editCustomer('ขายยย')">แก้ไข</button>
                <el-button icon="el-icon-more" circle size="small" class="row-action"></el-button>
              </td>
            </tr>
            <tr>
              <td>นาย A<br><span class="subtext">สำนักงานใหญ่</span></td>
              <td></td>
              <td></td>
              <td></td>
              <td>ลูกค้า</td>
              <td>
                <button class="btn btn-warning btn-sm me-1" @click="editCustomer('นาย A')">แก้ไข</button>
                <el-button icon="el-icon-more" circle size="small" class="row-action"></el-button>
              </td>
            </tr>
            <tr>
              <td>บี<br><span class="subtext">สำนักงานใหญ่</span></td>
              <td></td>
              <td></td>
              <td></td>
              <td>ลูกค้า</td>
              <td>
                <button class="btn btn-warning btn-sm me-1" @click="editCustomer('บี')">แก้ไข</button>
                <el-button icon="el-icon-more" circle size="small" class="row-action"></el-button>
              </td>
            </tr>
            <tr>
              <td>แสน<br><span class="subtext">สำนักงานใหญ่</span></td>
              <td></td>
              <td></td>
              <td></td>
              <td>ลูกค้า</td>
              <td>
                <button class="btn btn-warning btn-sm me-1" @click="editCustomer('แสน')">แก้ไข</button>
                <el-button icon="el-icon-more" circle size="small" class="row-action"></el-button>
              </td>
            </tr>
            <tr>
              <td>เอ<br><span class="subtext">สำนักงานใหญ่</span></td>
              <td></td>
              <td></td>
              <td></td>
              <td>ลูกค้า</td>
              <td>
                <button class="btn btn-warning btn-sm me-1" @click="editCustomer('เอ')">แก้ไข</button>
                <el-button icon="el-icon-more" circle size="small" class="row-action"></el-button>
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
import { useRouter } from 'vue-router'
// import { ElIcon, ElButton, ElTable, ... } from 'element-plus'

const activeTab = ref('all')
const search = ref('')
const router = useRouter()

function openSaleForm() {
  router.push('/contactbook/new')
}
function editCustomer(name: string) {
  // TODO: implement edit logic for customer with the given name
  console.log('Editing customer:', name)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600&display=swap');

.page-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5fafd 0%, #e3f0ff 100%);
  padding: 32px 0;
  font-family: 'Prompt', sans-serif;
  letter-spacing: 0.3px;
}
.main-card {
  max-width: 950px;
  margin: 0 auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 6px 32px 0 rgba(80,120,200,0.10), 0 1.5px 6px 0 rgba(80,120,200,0.08);
  padding: 32px 32px 24px 32px;
  transition: box-shadow 0.2s;
}
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.subtitle {
  color: #8ca0b3;
  font-size: 15px;
  margin-top: 2px;
}
.create-btn {
  background: #8dc63f;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 2px 8px 0 #8dc63f33;
  transition: background 0.2s, box-shadow 0.2s;
}
.create-btn:hover {
  background: #7bbf36;
  box-shadow: 0 4px 16px 0 #8dc63f44;
}
.import-btn {
  border-radius: 8px;
  font-weight: 500;
  box-shadow: 0 2px 8px 0 #b3d8ff33;
  transition: background 0.2s, box-shadow 0.2s;
}
.import-btn:hover {
  background: #409eff;
  color: #fff;
  box-shadow: 0 4px 16px 0 #b3d8ff44;
}
.pretty-tabs {
  background: #f4f8fb;
  border-radius: 8px 8px 0 0;
  padding: 0 8px;
  margin-bottom: 0.5rem;
}
.pretty-search {
  border-radius: 8px;
  box-shadow: 0 1px 4px 0 #b3d8ff22;
  background: #fafdff;
  font-size: 16px;
  padding: 2px 0;
}
.table-container {
  background: #fafdff;
  border-radius: 12px;
  box-shadow: 0 1.5px 8px 0 #b3d8ff22;
  padding: 0;
  overflow-x: auto;
}
.customer-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  font-size: 15px;
  font-weight: 400;
}
.customer-table thead th {
  position: sticky;
  top: 0;
  background: #eaf6ff;
  color: #2b4a6d;
  font-weight: 500;
  padding: 12px 10px;
  border-bottom: 2px solid #d2e6fa;
  z-index: 2;
  letter-spacing: 0.4px;
}
.customer-table td {
  padding: 12px 10px;
  border-bottom: 1px solid #f0f4f8;
  background: #fff;
  transition: background 0.15s;
  color: #1a2533;
  font-weight: 400;
  opacity: 1;
}
.customer-table tr:hover td {
  background: #f4faff;
}
.group-row td {
  background: #eaf6ff;
  font-weight: 500;
  color: #1e4b7c;
  font-size: 16px;
  border-bottom: 1px solid #d2e6fa;
  letter-spacing: 0.4px;
}
.subtext {
  color: #6b7d8f;
  font-size: 13px;
  margin-left: 2px;
  font-weight: 300;
}
.row-action {
  background: #f4f8fb;
  border: none;
  color: #409eff;
  transition: background 0.2s, color 0.2s;
}
.row-action:hover {
  background: #eaf6ff;
  color: #1d7be4;
}
.mb-2 {
  margin-bottom: 0.5rem;
}
.mb-4 {
  margin-bottom: 1.2rem;
}
.mr-2 {
  margin-right: 0.5rem;
}
h2 {
  font-weight: 500;
  color: #1e4b7c;
  margin-bottom: 0;
  letter-spacing: 0.5px;
}
@media (max-width: 700px) {
  .main-card {
    padding: 16px 4px 12px 4px;
  }
  .header-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  .customer-table th, .customer-table td {
    font-size: 14px;
    padding: 8px 4px;
  }
}
</style>
