/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>
  export default component
}

declare module '@heroicons/vue/24/outline' {
  import type { Component } from 'vue'
  export const UserIcon: Component
  export const PackageIcon: Component
  export const TrashIcon: Component
  export const EyeIcon: Component
  export const PencilIcon: Component
  export const PrinterIcon: Component
  export const ShoppingCartIcon: Component
  export const DocumentTextIcon: Component
  export const DocumentIcon: Component
  export const ReceiptIcon: Component
  export const CubeIcon: Component
  export const UserGroupIcon: Component
  export const ChartBarIcon: Component
  export const CogIcon: Component
}
