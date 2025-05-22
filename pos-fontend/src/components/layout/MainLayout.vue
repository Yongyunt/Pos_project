<template>
  <div class="main-layout">
    <!-- Mobile Menu Toggle -->
    <button class="mobile-menu-toggle" @click="toggleSidebar">
      <bars-3-icon v-if="!isSidebarOpen" class="menu-icon" />
      <x-mark-icon v-else class="menu-icon" />
    </button>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'sidebar-open': isSidebarOpen }">
      <div class="sidebar-header">Posify </div>
      <nav>
        <router-link
          v-for="(item, index) in menuItems"
          :key="index"
          :to="item.path"
          :class="['nav-link', $route.path === item.path ? 'active' : '']"
          @click="closeSidebarOnMobile"
        >
          <component :is="item.icon" class="me-2" />
          <span class="nav-label">{{ item.name }}</span>
        </router-link>
      </nav>
    </aside>

    <!-- Overlay for mobile -->
    <div v-if="isSidebarOpen" class="sidebar-overlay" @click="toggleSidebar"></div>

    <!-- Main Content -->
    <section class="main-content">
      <header class="main-header">
        <h1>{{ currentMenuTitle }}</h1>
        <div class="header-actions">
          <span class="current-date">{{ currentDate }}</span>
          <button class="user-btn">
            <user-icon style="width: 24px; height: 24px; color: #212529;" />
          </button>
        </div>
      </header>
      <main class="main-body">
        <router-view />
      </main>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { UserIcon, Bars3Icon, XMarkIcon } from '@heroicons/vue/24/solid'

const route = useRoute()
const isSidebarOpen = ref(false)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebarOnMobile = () => {
  if (window.innerWidth <= 600) {
    isSidebarOpen.value = false
  }
}

const menuItems = [
  { id: 'quotations', name: 'ใบเสนอราคา', path: '/quotations', icon: 'DocumentTextIcon' },
  { id: 'sales', name: 'การขาย', path: '/sales', icon: 'CubeIcon' },
  { id: 'receipts', name: 'ใบเสร็จรับเงิน', path: '/receipts', icon: 'ReceiptIcon' },
  { id: 'products', name: 'สินค้า', path: '/products', icon: 'CashIcon' },
  { id: 'contactbook', name: 'สมุดรายชื่อ', path: '/contactbook', icon: 'UserGroupIcon' },
  // { id: 'reports', name: 'รายงาน', path: '/reports', icon: 'ChartBarIcon' },
]

const currentDate = computed(() => {
  return new Date().toLocaleDateString('th-TH', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const currentMenuTitle = computed(() => {
  const currentItem = menuItems.find(item => item.path === route.path)
  return currentItem ? currentItem.name : ''
})
</script>

<script lang="ts">
export default {}
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  min-width: 100vw;
  height: 100vh;
  width: 100vw;
  background: #f8f9fa;
  position: relative;
}

.mobile-menu-toggle {
  display: none;
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1000;
  background: #212529;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
}

.menu-icon {
  width: 24px;
  height: 24px;
}

.sidebar {
  background: #212529;
  color: #fff;
  min-width: 250px;
  max-width: 250px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
  z-index: 100;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
}

.sidebar-header {
  padding: 2rem 1rem 1rem 2rem;
  font-weight: bold;
  font-size: 2rem;
  border-bottom: 1px solid #444;
}
.nav-link {
  display: flex;
  align-items: center;
  padding: 1rem;
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  border-left: 4px solid transparent;
  transition: background 0.2s, color 0.2s;
}
.nav-link.active {
  background: #fff;
  color: #212529;
  border-left: 4px solid #0d6efd;
}
.main-content {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}
.main-header {
  background: #fff;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.main-body {
  flex: 1 1 0;
  overflow: auto;
  padding: 2rem;
  background: #f8f9fa;
  min-height: 0;
}
.user-btn {
  background: none;
  border: none;
  border-radius: 50%;
  padding: 0.5rem;
}
@media (max-width: 991px) {
  .sidebar {
    min-width: 60px;
    max-width: 60px;
    padding: 0;
  }
  .sidebar-header {
    font-size: 1.2rem;
    padding: 1rem 0.5rem;
  }
  .nav-link {
    justify-content: center;
    font-size: 0.9rem;
    padding: 0.75rem 0.5rem;
  }
  .nav-label {
    display: none;
  }
}
@media (max-width: 600px) {
  .mobile-menu-toggle {
    display: block;
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    width: 250px;
    min-width: 250px;
    max-width: 250px;
    height: 100vh;
  }

  .sidebar-open {
    transform: translateX(0);
  }

  .sidebar-overlay {
    display: block;
  }

  .nav-label {
    display: block;
  }

  .main-layout {
    flex-direction: column;
  }

  .main-content {
    margin-left: 0;
  }

  .main-header {
    padding: 1rem;
  }

  .current-date {
    display: none;
  }

  .main-body {
    padding: 1rem;
  }
}
</style>
