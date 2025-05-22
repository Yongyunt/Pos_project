<template>
  <div class="sale-form-container">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <div>
        <span class="doc-title">สร้างใบเสร็จรับเงิน (เงินสด)</span>
        <span class="doc-no ms-2">CA202505180001</span>
        <font-awesome-icon icon="pen" class="ms-2 text-secondary" />
      </div>
      <div>
        <button class="btn btn-outline-secondary me-2" @click="emit('close')">ปิดหน้าต่าง</button>
        <button class="btn btn-success">บันทึกเอกสาร</button>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <label class="form-label">ชื่อลูกค้า</label>
        <select class="form-select mb-2">
          <option>Cash Sale / ขายเงินสด</option>
        </select>
        <label class="form-label">ข้อมูลลูกค้า</label>
        <textarea class="form-control mb-2" rows="2" placeholder="รายละเอียดที่อยู่"></textarea>
        <!-- <input class="form-control mb-2" placeholder="รหัสโปรเจ็คย่อย" /> -->
        <!-- <input class="form-control mb-2" placeholder="เลขประจำตัวผู้เสียภาษี" /> -->
        <!-- <input class="form-control mb-2" placeholder="สำนักงาน/สถานที่ส่ง" /> -->
      </div>
      <div class="col-md-6">
        <div class="row mb-2">
          <div class="col-6">
            <label class="form-label">จำนวนเงินรวมทั้งสิ้น</label>
            <div class="h3 text-primary">0.00</div>
          </div>
          <div class="col-6">
            <label class="form-label">วันที่</label>
            <input type="date" class="form-control mb-2" />
            <label class="form-label">สกุลเงิน</label>
            <select class="form-select mb-2">
              <option>THB - ไทย</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <!-- <label class="form-label mt-2">โปรเจ็ค</label> -->
    <!-- <input class="form-control mb-2" /> -->
    <!-- <label class="form-label">รายละเอียด</label> -->
    <!-- <input class="form-control mb-2" /> -->
    <!-- <label class="form-label">คลังสินค้า</label>
    <select class="form-select mb-2">
      <option>คลังสินค้า</option>
    </select> -->
    <!-- ตารางสินค้า -->
    <div class="table-responsive mt-3">
      <table class="table table-bordered align-middle">
        <thead class="table-primary">
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
          <tr v-for="i in 3" :key="i">
            <td>{{ i }}</td>
            <td><input class="form-control" /></td>
            <td><input class="form-control" type="number" min="0" /></td>
            <td><input class="form-control" /></td>
            <td><input class="form-control" type="number" min="0" /></td>
            <td>0.00</td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-outline-primary mt-2">+ เพิ่มแถวรายการ</button>
    <div class="row mt-3">
      <div class="col-md-6">
        <label class="form-label">หมายเหตุ</label>
        <textarea class="form-control mb-2"></textarea>
        <!-- <label class="form-label">โน้ตภายในบริษัท</label>
        <textarea class="form-control mb-2"></textarea> -->
      </div>
      <div class="col-md-6">
        <div class="bg-light p-3 rounded">
          <div class="d-flex justify-content-between">
            <span>รวมเป็นเงิน</span>
            <span>0.00</span>
          </div>
          <div class="d-flex justify-content-between">
            <span>ส่วนลด</span>
            <span>0.00</span>
          </div>
          <div class="d-flex justify-content-between">
            <span>ราคาหลังหักส่วนลด</span>
            <span>0.00</span>
          </div>
          <div class="d-flex justify-content-between">
            <span>จำนวนเงินรวมทั้งสิ้น</span>
            <span>0.00</span>
          </div>
        </div>
        <div class="form-check mt-2">
          <input class="form-check-input" type="checkbox" id="adjust" />
          <label class="form-check-label" for="adjust">เพิ่มรายการปรับลด/ปรับเพิ่ม</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="payat" />
          <label class="form-check-label" for="payat">หักภาษี ณ ที่จ่าย</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineEmits } from 'vue'

const emit = defineEmits(['close'])
</script>

<style scoped>
.sale-form-container {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem auto;
  max-width: 1100px;
  box-shadow: 0 2px 8px #0001;
}
.doc-title {
  font-weight: 600;
  font-size: 1.2rem;
}
.doc-no {
  color: #2196f3;
  font-weight: 600;
  font-size: 1.1rem;
}
</style>
