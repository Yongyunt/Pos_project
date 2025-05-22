import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [],
    loading: false,
    error: null
  }),

  getters: {
    getProductById: (state) => (id) => {
      return state.products.find(product => product.id === id)
    }
  },

  actions: {
    // Create a new product
    async createProduct(productData) {
      try {
        this.loading = true
        const response = await axios.post('http://localhost:8000/pos_api/products/', productData)
        this.products.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Error creating product'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Get all products
    async fetchProducts() {
      try {
        this.loading = true
        const response = await axios.get('http://localhost:8000/pos_api/products/')
        this.products = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Error fetching products'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Get a single product by ID
    async getProduct(id) {
      try {
        this.loading = true
        const response = await axios.get(`http://localhost:8000/pos_api/products/${id}/`)
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Error fetching product'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Update a product
    async updateProduct(id, productData) {
      try {
        this.loading = true
        const response = await axios.put(`http://localhost:8000/pos_api/products/${id}/`, productData)
        const index = this.products.findIndex(p => p.id === id)
        if (index !== -1) {
          this.products[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data || 'Error updating product'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Delete a product
    async deleteProduct(id) {
      try {
        this.loading = true
        await axios.delete(`http://localhost:8000/pos_api/products/${id}/`)
        this.products = this.products.filter(product => product.id !== id)
        return true
      } catch (error) {
        this.error = error.response?.data || 'Error deleting product'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Clear error state
    clearError() {
      this.error = null
    }
  }
})

