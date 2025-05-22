import { defineStore } from 'pinia'
import axios from 'axios'

export const useQuotationStore = defineStore('quotation', {
  state: () => ({
    quotations: [],
    currentQuotation: null
  }),
  actions: {
    async getQuotations() {
      const response = await axios.get('http://localhost:8000/pos_api/quotations/')
      console.log('API Response:', response.data)
      this.quotations = response.data
      return response.data
    },
    async getQuotationById(id) {
      try {
        const response = await axios.get(`http://localhost:8000/pos_api/quotations/${id}/`)
        this.currentQuotation = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching quotation:', error)
        throw error
      }
    }
  }
})
