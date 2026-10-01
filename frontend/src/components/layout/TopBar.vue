<script setup>
import { MorphIcon } from 'morphicons/vue'
import { Menu, ArrowLeft } from 'lucide'

defineProps({
  isSidebarOpen: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['toggle-sidebar'])
</script>

<template>
  <nav class="topbar navbar navbar-expand fixed-top">
    <RouterLink :to="{ name: 'Inicio' }" class="navbar-brand ms-3">
      <img src="/logo-topbar.svg" alt="FleetHub — Inicio" height="20" />
    </RouterLink>
    <button
      type="button"
      class="sidebar-toggle btn btn-link btn-sm text-white ms-3"
      aria-label="Alternar menú lateral"
      @click="emit('toggle-sidebar')"
    >
      <MorphIcon
        :icon="isSidebarOpen ? ArrowLeft : Menu"
        :size="24"
        spring="bouncy"
        reduced-motion="user"
      />
    </button>
  </nav>
</template>

<style scoped>
.topbar {
  height: 56px;
  background-color: #151618;
  border-bottom: 1px solid rgb(255 255 255 / 12%);
}
</style>
