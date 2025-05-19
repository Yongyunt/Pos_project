<template>
  <div class="row g-4 h-100">
    <!-- Product List -->
    <div class="col-12 col-md-8">
      <div class="bg-white rounded shadow-sm p-5 h-100 d-flex flex-column">
        <div class="mb-4">
          <input
            type="text"
            placeholder="ค้นหาสินค้า..."
            class="form-control form-control-lg"
            v-model="searchQuery"
          />
        </div>
        <div class="row g-4 flex-grow-1 overflow-auto">
          <div
            v-for="product in filteredProducts"
            :key="product.id"
            @click="addToCart(product)"
            class="col-6 col-sm-4 col-md-3"
          >
            <div class="bg-light rounded p-4 mb-3 text-center border h-100 d-flex flex-column justify-content-center align-items-center product-card fs-5" style="cursor:pointer;">
              <package-icon style="width: 48px; height: 48px; color: #6c757d;" />
              <div class="fw-bold mt-3 text-dark">{{ product.name }}</div>
              <div class="text-dark">฿{{ product.price.toFixed(2) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Cart -->
    <div class="col-12 col-md-4">
      <div class="bg-white rounded shadow-sm p-5 h-100 d-flex flex-column">
        <h2 class="fs-4 fw-bold mb-4 text-dark">รายการสินค้า</h2>
        <div class="flex-grow-1 overflow-auto mb-4">
          <div v-if="cart.length === 0" class="text-center text-dark py-5 fs-5">
            ยังไม่มีสินค้าในตะกร้า
          </div>
          <div v-else class="vstack gap-3">
            <div
              v-for="(item, index) in cart"
              :key="index"
              class="d-flex justify-content-between align-items-center border-bottom pb-3"
            >
              <div>
                <div class="fw-medium fs-5 text-dark">{{ item.name }}</div>
                <div class="text-dark small">฿{{ item.price.toFixed(2) }} x {{ item.quantity }}</div>
              </div>
              <div class="d-flex align-items-center">
                <div class="fw-medium me-3 fs-5">฿{{ (item.price * item.quantity).toFixed(2) }}</div>
                <button @click="removeFromCart(index)" class="btn btn-link text-danger p-0 fs-5">
                  <trash-icon style="width: 20px; height: 20px;" />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-3 border-top pt-4 fs-5">
          <div class="d-flex justify-content-between">
            <span class="fw-bold text-dark">ยอดรวม</span>
            <span class="fw-bold text-dark">฿{{ totalAmount.toFixed(2) }}</span>
          </div>
          <div class="d-flex justify-content-between">
            <span class="fw-bold text-dark">ภาษี (7%)</span>
            <span class="fw-bold text-dark">฿{{ tax.toFixed(2) }}</span>
          </div>
          <div class="d-flex justify-content-between fw-bold fs-4">
            <span class="fw-bold text-dark">ยอดสุทธิ</span>
            <span class="fw-bold text-dark">฿{{ grandTotal.toFixed(2) }}</span>
          </div>
        </div>
        <div class="mt-4 row g-3">
          <div class="col-6">
            <button class="btn btn-secondary w-100 py-3 fs-5" @click="clearCart">ยกเลิก</button>
          </div>
          <div class="col-6">
            <button class="btn btn-primary w-100 py-3 fs-5" @click="checkout" :disabled="cart.length === 0">ชำระเงิน</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { PackageIcon, TrashIcon } from '@heroicons/vue/24/outline'

interface Product {
  id: number
  name: string
  price: number
}

interface CartItem extends Product {
  quantity: number
}

const searchQuery = ref('')
const cart = ref<CartItem[]>([])

// Sample products data - replace with your actual data source
const products = ref<Product[]>([
  { id: 1, name: 'สินค้า 1', price: 100 },
  { id: 2, name: 'สินค้า 2', price: 200 },
  { id: 3, name: 'สินค้า 3', price: 300 },
  // Add more products as needed
])

const filteredProducts = computed(() => {
  return products.value.filter(product =>
    product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const totalAmount = computed(() => {
  return cart.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const tax = computed(() => {
  return totalAmount.value * 0.07
})

const grandTotal = computed(() => {
  return totalAmount.value + tax.value
})

const addToCart = (product: Product) => {
  const existingItem = cart.value.find(item => item.id === product.id)
  if (existingItem) {
    existingItem.quantity++
  } else {
    cart.value.push({ ...product, quantity: 1 })
  }
}

const removeFromCart = (index: number) => {
  cart.value.splice(index, 1)
}

const clearCart = () => {
  cart.value = []
}

const checkout = () => {
  // Implement checkout logic here
  console.log('Checkout:', cart.value)
  clearCart()
}
</script>
