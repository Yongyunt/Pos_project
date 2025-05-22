<template>
  <div class="customer-form-container">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <span class="doc-title">สร้างรายชื่อผู้ติดต่อ</span>
      </div>
      <div>
        <button class="btn btn-outline-secondary me-2" @click="close">ปิดหน้าต่าง</button>
        <button class="btn btn-success" @click="submit">บันทึกแล้วปิด</button>
      </div>
    </div>
    <div class="row">
      <!-- Left Column -->
      <div class="col-md-6">
        <div class="section-title">ข้อมูลผู้ติดต่อ</div>
        <!-- <label class="form-label">ประเภทผู้ติดต่อ</label> -->
        <div class="mb-2">
          <!-- <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" v-model="form.contactType" value="individual" id="type1">
            <label class="form-check-label" for="type1">นิติบุคคล</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" v-model="form.contactType" value="person" id="type2">
            <label class="form-check-label" for="type2">บุคคลธรรมดา</label>
          </div> -->
        </div>
        <!-- <label class="form-label">ประเภท</label> -->
        <!-- <div class="mb-2">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" v-model="form.type" value="customer" id="customer">
            <label class="form-check-label" for="customer">ลูกค้าใหม่</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" v-model="form.type" value="supplier" id="supplier">
            <label class="form-check-label" for="supplier">ลูกค้าประจำ</label>
          </div>
        </div> -->
        <!-- <label class="form-label">รหัสผู้ติดต่อ</label>
        <input class="form-control mb-2" v-model="form.code" /> -->
        <label class="form-label">ชื่อลูกค้า(ภาษาไทย)</label>
        <input class="form-control mb-2" v-model="form.businessName" placeholder="ตัวอย่างการกรอก: แดง" />
        <label class="form-label">ชื่อลูกค้า(ภาษาอังกฤษ)</label>
        <input class="form-control mb-2" v-model="form.english_name" placeholder="ตัวอย่างการกรอก:  John " />
        <label class="form-label">สัญชาติ</label>
        <div class="mb-2">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" v-model="form.zone" value="thai" id="zone1">
            <label class="form-check-label" for="zone1">ไทย</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" v-model="form.zone" value="foreign" id="zone2">
            <label class="form-check-label" for="zone2">พม่า</label>
          </div>
        </div>
        <label class="form-label">เบอร์มือถือ</label>
        <input class="form-control mb-2" v-model="form.mobile" type="tel" maxlength="10" @input="form.mobile = form.mobile.replace(/\D/g, '')" />
        <label class="form-label">Line ID</label>
        <input class="form-control mb-2" v-model="form.lineId" />
        <label class="form-label">Viber Name </label>
        <input class="form-control mb-2" v-model="form.viberPhone" />
        <!-- <label class="form-label">เลขผู้เสียภาษี</label> -->
        <!-- <input class="form-control mb-2" v-model="form.taxId" placeholder="ระบุเลขผู้เสียภาษี 10 - 13 หลัก" /> -->
        <label class="form-label">ที่อยู่</label>
        <textarea class="form-control mb-2" v-model="form.address" rows="2"></textarea>
        <!-- <label class="form-label">รหัสไปรษณีย์</label>
        <input class="form-control mb-2" v-model="form.zip" />
        <label class="form-label">ที่อยู่สำหรับจัดส่ง</label>
        <textarea class="form-control mb-2" v-model="form.shippingAddress" rows="2"><textarea> -->
      </div>
      <!-- Right Column -->
      <!-- <div class="col-md-6">
        <div class="section-title">รายละเอียดผู้ติดต่อ</div>
        <label class="form-label">ชื่อผู้ติดต่อ</label>
        <input class="form-control mb-2" v-model="form.contactName" />
        <label class="form-label">อีเมล</label>
        <input class="form-control mb-2" v-model="form.email" />
        <label class="form-label">เบอร์มือถือ</label>
        <input class="form-control mb-2" v-model="form.mobile" />
        <div class="section-title mt-3">ข้อมูลธนาคาร</div>
        <label class="form-label">ธนาคาร</label>
        <select class="form-select mb-2" v-model="form.bank">
          <option value="">กรุณาเลือกธนาคาร</option>
          <option value="bbl">ธนาคารกรุงเทพ</option>
          <option value="kbank">ธนาคารกสิกรไทย</option>
          <option value="scb">ธนาคารไทยพาณิชย์</option>
        </select>
        <label class="form-label">เลขที่บัญชี</label>
        <input class="form-control mb-2" v-model="form.bankAccount" />
        <label class="form-label">สาขาธนาคาร</label>
        <input class="form-control mb-2" v-model="form.bankBranch" />
        <label class="form-label">ประเภทบัญชี</label>
        <div class="mb-2">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" v-model="form.bankType" value="saving" id="banktype1">
            <label class="form-check-label" for="banktype1">ออมทรัพย์</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" v-model="form.bankType" value="current" id="banktype2">
            <label class="form-check-label" for="banktype2">กระแสรายวัน</label>
          </div>
        </div>
        <label class="form-label">คิวอาร์ชำระเงิน</label>
        <input class="form-control mb-2" type="file" />
        <div class="form-check mb-2">
          <input class="form-check-input" type="checkbox" v-model="form.hasForeignBank" id="hasForeignBank">
          <label class="form-check-label" for="hasForeignBank">ข้อมูลเพิ่มเติมสำหรับธนาคารต่างประเทศ</label>
        </div>
        <div v-if="form.hasForeignBank">
          <label class="form-label">Swift Code</label>
          <input class="form-control mb-2" v-model="form.swiftCode" />
          <label class="form-label">ที่อยู่ธนาคาร</label>
          <input class="form-control mb-2" v-model="form.bankAddress" />
        </div>
        <div class="section-title mt-3">ข้อมูลเพิ่มเติม</div>
        <label class="form-label">แนบไฟล์</label>
        <input class="form-control mb-2" type="file" />
        <label class="form-label">โน้ต</label>
        <textarea class="form-control mb-2" v-model="form.note" rows="2"></textarea>
      </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useContactFormStore } from '../stores/Contacts'

const store = useContactFormStore()

const form = ref({
  contactType: 'individual',
  type: [],
  zone: 'thai',
  code: '',
  businessName: '',
  english_name: '',
  taxId: '',
  officeType: 'main',
  address: '',
  zip: '',
  shippingAddress: '',
  officePhone: '',
  fax: '',
  website: '',
  contactName: '',
  email: '',
  mobile: '',
  lineId: '',
  viberPhone: '',
  bank: '',
  bankAccount: '',
  bankBranch: '',
  bankType: 'saving',
  hasForeignBank: false,
  swiftCode: '',
  bankAddress: '',
  note: ''
})
import { useRouter } from 'vue-router'

const router = useRouter()

const submit = () => {
  console.log("Submitting form:", form)
  store.submitForm()
}



function close() {
  router.push('/contactbook')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600&display=swap');

.customer-form-container {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem auto;
  max-width: 1100px;
  box-shadow: 0 2px 8px #0001;
  font-family: 'Prompt', sans-serif;
}
.doc-title {
  font-weight: 600;
  font-size: 1.2rem;
  color: #1a2533;
  letter-spacing: 0.2px;
}
.section-title {
  font-weight: 600;
  color: #1e4b7c;
  margin-bottom: 12px;
  margin-top: 8px;
  font-size: 18px;
  letter-spacing: 0.3px;
}
.form-label {
  color: #1a2533;
  font-weight: 500;
  letter-spacing: 0.2px;
}
input,
textarea,
select {
  color: #1a2533;
  font-weight: 400;
  letter-spacing: 0.1px;
  font-family: 'Prompt', sans-serif;
}
.mt-3 {
  margin-top: 24px;
}
select,
option {
  color: #1a2533;
  font-weight: 500;
  font-size: 16px;
  font-family: 'Prompt', sans-serif;
  letter-spacing: 0.1px;
}

.form-check-label {
  color: #1a2533;
  font-weight: 500;
  font-size: 15px;
  letter-spacing: 0.1px;
}

.form-check-input[type="radio"],
.form-check-input[type="checkbox"] {
  accent-color: #1e4b7c;
  width: 18px;
  height: 18px;
}
</style>
