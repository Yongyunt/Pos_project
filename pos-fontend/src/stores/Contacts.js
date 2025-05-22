import { defineStore } from 'pinia'
import axios from 'axios'

export const useContactFormStore = defineStore('contactForm', {
  state: () => ({
    form: {
      thai_name: '',
      english_name: '',
      nationality: 'ไทย',
      phone: '',
      line_id: '',
      viber_Name: '',
      address: '',
    },
  }),
  actions: {
    async submitForm() {
      try {
        await axios.post('http://localhost:8000/api/contacts/', this.form)
        alert('บันทึกข้อมูลสำเร็จ')
      } catch (error) {
        alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล')
        console.error(error)
      }
    },
  },
})