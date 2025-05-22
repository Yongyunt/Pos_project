import { defineStore } from 'pinia'
import axios from 'axios'

export const useContactFormStore = defineStore('contactForm', {
  state: () => ({
    customers: [],
    form: {}
  }),
  actions: {
    async submitForm(value) {
      try {
        console.log(value)
        await axios.post('http://localhost:8000/pos_api/customers/', value)
        alert('บันทึกข้อมูลสำเร็จ')
      } catch (error) {
        alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล')
        console.error(error)
      }
    },
    async getCustomer() {
      try {
        const response = await axios.get('http://localhost:8000/pos_api/customers/')
        this.customers = response.data
        return response.data
      } catch (error) {
        console.error(error)
        return []
      }
    },
    async deleteCustomer(id) {
      try {
        await axios.delete(`http://localhost:8000/pos_api/customers/${id}/`)
        this.customers = this.customers.filter(customer => customer.id !== id)
        return true
      } catch (error) {
        console.error(error)
        return false
      }
    }
  },
})
