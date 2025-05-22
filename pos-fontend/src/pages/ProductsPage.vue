<template>
  <div class="container my-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>จัดการสินค้า</h2>
      <div>
        <button class="btn btn-success" @click="openProductForm()">เพิ่มสินค้าใหม่</button>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="mb-3">
      <div class="input-group" style="max-width: 300px;">
        <input type="text" v-model="searchQuery" class="form-control" placeholder="ค้นหาสินค้า..." />
        <button class="btn btn-primary">
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <!-- Loading and Error Messages -->
    <div v-if="loading" class="alert alert-info">กำลังโหลดข้อมูลสินค้า...</div>
    <div v-if="error" class="alert alert-danger">เกิดข้อผิดพลาด: {{ error }}</div>

    <!-- Products Table -->
    <div class="table-responsive" v-if="!loading && !error && products.length > 0">
      <table class="table table-bordered align-middle">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>ชื่อสินค้า</th>
            <th>รายละเอียด</th>
            <th class="text-end">ราคา (บาท)</th>
            <th class="text-center">สต็อก</th>
            <th class="text-center">การดำเนินการ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.description || '-' }}</td>
            <td class="text-end">{{ formatNumber(product.unit_price) }}</td>
            <td class="text-center">{{ product.stock_quantity !== undefined ? product.stock_quantity : '-' }}</td>
            <td class="text-center">
              <button class="btn btn-sm btn-outline-primary me-2" @click="editProduct(product)">
                <font-awesome-icon icon="edit" /> แก้ไข
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteProduct(product.id)">
                <font-awesome-icon icon="trash" /> ลบ
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="!loading && products.length === 0 && !error" class="alert alert-secondary">
      ยังไม่มีข้อมูลสินค้า
    </div>

    <!-- Pagination (Placeholder) -->
    <div class="d-flex justify-content-between align-items-center mt-3" v-if="products.length > 0">
      <div>
        รายการต่อหน้า:
        <select v-model="itemsPerPage" class="form-select d-inline-block w-auto ms-2">
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="50">50</option>
        </select>
      </div>
      <div>
        <!-- Pagination components will go here -->
      </div>
    </div>

    <!-- Product Form Modal -->
    <div v-if="showProductForm" class="modal-backdrop-custom">
      <div class="modal-custom">
        <h3>{{ editingProduct ? 'แก้ไขสินค้า' : 'เพิ่มสินค้าใหม่' }}</h3>
        <form @submit.prevent="saveProduct">
          <div class="mb-3">
            <label for="productName" class="form-label">ชื่อสินค้า:</label>
            <input type="text" class="form-control" id="productName" v-model="currentProduct.name" required />
          </div>
          <div class="mb-3">
            <label for="productDescription" class="form-label">รายละเอียด (ไม่บังคับ):</label>
            <textarea class="form-control" id="productDescription" v-model="currentProduct.description"></textarea>
          </div>
          <div class="mb-3">
            <label for="productPrice" class="form-label">ราคาขาย (หน่วย):</label>
            <input type="text" class="form-control" id="productPrice" v-model="currentProduct.unit_price" required pattern="^\d*\.?\d*$"/>
          </div>
          <div class="mb-3">
            <label for="productCostPrice" class="form-label">ราคาต้นทุน (หน่วย):</label>
            <input type="text" class="form-control" id="productCostPrice" v-model="currentProduct.cost_price" pattern="^\d*\.?\d*$"/>
          </div>
          <div class="mb-3">
            <label for="productStock" class="form-label">สต็อก:</label>
            <input type="number" class="form-control" id="productStock" v-model.number="currentProduct.stock_quantity" required min="0"/>
          </div>
          <div class="mb-3">
            <label for="productCategory" class="form-label">หมวดหมู่ (ID):</label>
            <input type="number" class="form-control" id="productCategory" v-model.number="currentProduct.category" required min="0"/>
          </div>

          <div class="d-flex justify-content-end">
            <button type="button" class="btn btn-outline-secondary me-2" @click="closeProductForm">ยกเลิก</button>
            <button type="submit" class="btn btn-success">{{ editingProduct ? 'บันทึกการเปลี่ยนแปลง' : 'เพิ่มสินค้า' }}</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useProductStore } from '../stores/Product' // No .ts extension
import type { Product } from '../stores/Product' // Type-only import for Product
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Assuming you have FontAwesome icons set up, e.g., edit, trash
// If not, you might need to install and configure:
// npm install @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/vue-fontawesome@next-major

// Define an interface for the Product (can be removed if imported from store)
// interface Product { ... } // This can be removed

export default defineComponent({
  name: 'ProductsPage',
  components: { FontAwesomeIcon },
  setup() {
    const productStore = useProductStore()
    const searchQuery = ref('')
    const itemsPerPage = ref(10) // Default items per page
    const showProductForm = ref(false)
    const editingProduct = ref<Product | null>(null)
    const currentProduct = ref<Product>({
      category: 0,
      name: '',
      unit_price: '0.00',
      cost_price: '0.00',
      description: '',
      stock_quantity: 0
    })

    const products = computed(() => productStore.products) // No need for 'as Product[]' if store is typed
    const loading = computed(() => productStore.loading)
    const error = computed(() => productStore.error)

    onMounted(async () => {
      try {
        await productStore.fetchProducts()
      } catch (fetchError) {
        console.error("Failed to fetch products on mount:", fetchError)
        // The error should already be set in the store,
        // but you could add additional local handling if needed.
      }
    })

    const filteredProducts = computed(() => {
      if (!searchQuery.value) {
        return products.value
      }
      return products.value.filter(product =>
        product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        (product.description && product.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
      )
    })

    const formatNumber = (numStr: string | number): string => {
      const num = parseFloat(typeof numStr === 'string' ? numStr : String(numStr));
      if (isNaN(num)) return 'N/A'
      return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    }

    const openProductForm = (product: Product | null = null) => {
      if (product) {
        editingProduct.value = { ...product } // Clone to avoid direct state mutation
        currentProduct.value = { ...product }
      } else {
        editingProduct.value = null
        currentProduct.value = {
          category: 0,
          name: '',
          unit_price: '0.00',
          cost_price: '0.00',
          description: '',
          stock_quantity: 0
        }
      }
      showProductForm.value = true
    }

    const closeProductForm = () => {
      showProductForm.value = false
      editingProduct.value = null
      currentProduct.value = { // Reset form
        category: 0,
        name: '',
        unit_price: '0.00',
        cost_price: '0.00',
        description: '',
        stock_quantity: 0
      }
    }

    const saveProduct = async () => {
      try {
        if (editingProduct.value && editingProduct.value.id) {
          // Update existing product
          await productStore.updateProduct(editingProduct.value.id, currentProduct.value)
        } else {
          // Create new product
          await productStore.createProduct(currentProduct.value)
        }
        await productStore.fetchProducts() // Refresh list
        closeProductForm()
      } catch (err) {
        console.error('Failed to save product:', err)
        // Optionally, display a user-friendly error message here
      }
    }

    const editProduct = (product: Product) => {
      openProductForm(product)
    }

    const confirmDeleteProduct = async (id?: number) => {
      if (id === undefined) return;
      if (window.confirm('คุณแน่ใจหรือไม่ว่าต้องการลบสินค้านี้?')) {
        try {
          await productStore.deleteProduct(id)
          await productStore.fetchProducts() // Refresh list
        } catch (err) {
          console.error('Failed to delete product:', err)
          // Optionally, display a user-friendly error message here
        }
      }
    }

    return {
      searchQuery,
      itemsPerPage,
      products,
      loading,
      error,
      filteredProducts,
      formatNumber,
      showProductForm,
      openProductForm,
      closeProductForm,
      editingProduct,
      currentProduct,
      saveProduct,
      editProduct,
      confirmDeleteProduct
    }
  },
  // data() and methods() are not needed when using setup() fully like this
})
</script>

<style scoped>
/* Styles from the original file are kept, they seem generic enough */
.container {
  font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h2 {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 0;
}

.table {
  font-size: 0.95rem;
}

.table th {
  font-weight: 600;
  color: #2c3e50;
  background-color: #f8f9fa !important; /* Ensure this overrides other styles */
}

.table td {
  color: #2c3e50;
  vertical-align: middle;
}

.form-control, .form-select {
  font-size: 0.95rem;
}

.btn {
  font-weight: 500;
}

.text-end {
  font-family: 'Sarabun', monospace; /* Keep or change if not desired for price */
  font-weight: 500;
}

.form-select {
  min-width: 120px; /* Or adjust as needed */
  font-weight: 500;
}

.input-group .form-control {
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
}

select.form-select { /* For itemsPerPage */
  font-size: 0.9rem;
  padding: 0.25rem 2rem 0.25rem 0.5rem;
}

.table thead th {
  white-space: nowrap;
  padding: 0.75rem 1rem;
}

.table td {
  padding: 0.75rem 1rem;
}

td:last-child { /* Actions column */
  text-align: center;
}

.modal-backdrop-custom {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.25);
  z-index: 2000; /* Ensure it's above other content */
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-custom {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px #0002;
  padding: 2rem;
  max-width: 700px; /* Adjusted for product form */
  width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}
</style>

