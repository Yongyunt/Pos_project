import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'

// Define the Product interface to match the API structure
export interface Product {
  id?: number;
  category: number;
  name: string;
  unit_price: string;
  cost_price: string;
  description?: string;
  stock_quantity: number;
  created_at?: string;
  updated_at?: string;
}

// Interface for expected error structure from the backend
interface BackendError {
  message: string;
  // Add other properties if your backend sends more detailed errors
}

export const useProductStore = defineStore('product', {
  state: () => ({
    products: [] as Product[], // Use the Product interface
    loading: false,
    error: null as string | null // More specific error typing
  }),

  getters: {
    getProductById: (state) => (id: number): Product | undefined => {
      return state.products.find(product => product.id === id)
    }
  },

  actions: {
    // Helper to extract error message
    _getErrorMessage(error: unknown): string {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<BackendError>; // Assert to AxiosError with expected data
        if (axiosError.response && axiosError.response.data && axiosError.response.data.message) {
          return axiosError.response.data.message;
        }
        return axiosError.message;
      }
      if (error instanceof Error) {
        return error.message;
      }
      return 'An unknown error occurred';
    },

    // Create a new product
    async createProduct(productData: Omit<Product, 'id' | 'created_at' | 'updated_at'>): Promise<Product> {
      try {
        this.loading = true
        const response = await axios.post<Product>('http://localhost:8000/pos_api/products/', productData)
        this.products.push(response.data)
        return response.data
      } catch (error: unknown) {
        this.error = this._getErrorMessage(error) + ' (creating product)';
        return Promise.reject(new Error(this.error));
      } finally {
        this.loading = false
      }
    },

    // Get all products
    async fetchProducts(): Promise<Product[]> {
      try {
        this.loading = true
        const response = await axios.get<Product[]>('http://localhost:8000/pos_api/products/')
        this.products = response.data
        return response.data
      } catch (error: unknown) {
        this.error = this._getErrorMessage(error) + ' (fetching products)';
        return Promise.reject(new Error(this.error));
      } finally {
        this.loading = false
      }
    },

    // Get a single product by ID
    async getProduct(id: number): Promise<Product> {
      try {
        this.loading = true
        const response = await axios.get<Product>(`http://localhost:8000/pos_api/products/${id}/`)
        // Optionally update the local state if needed, or just return
        // const index = this.products.findIndex(p => p.id === id);
        // if (index !== -1) this.products[index] = response.data;
        // else this.products.push(response.data); // Or handle as a new addition if not found
        return response.data
      } catch (error: unknown) {
        this.error = this._getErrorMessage(error) + ' (fetching product)';
        return Promise.reject(new Error(this.error));
      } finally {
        this.loading = false
      }
    },

    // Update a product
    async updateProduct(id: number, productData: Partial<Product>): Promise<Product> {
      try {
        this.loading = true
        const response = await axios.put<Product>(`http://localhost:8000/pos_api/products/${id}/`, productData)
        const index = this.products.findIndex(p => p.id === id)
        if (index !== -1) {
          this.products[index] = response.data
        }
        return response.data
      } catch (error: unknown) {
        this.error = this._getErrorMessage(error) + ' (updating product)';
        return Promise.reject(new Error(this.error));
      } finally {
        this.loading = false
      }
    },

    // Delete a product
    async deleteProduct(id: number): Promise<boolean> {
      try {
        this.loading = true
        await axios.delete(`http://localhost:8000/pos_api/products/${id}/`)
        this.products = this.products.filter(product => product.id !== id)
        return true
      } catch (error: unknown) {
        this.error = this._getErrorMessage(error) + ' (deleting product)';
        return Promise.reject(new Error(this.error));
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
