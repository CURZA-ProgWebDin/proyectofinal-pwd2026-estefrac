<script setup>
import { MorphIcon } from 'morphicons/vue'
import { Menu, ArrowLeft, UserRound, LogOut } from 'lucide'
import { useAuthStore } from '../../stores/auth'

defineProps({
  isSidebarOpen: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['toggle-sidebar'])
const authStore = useAuthStore()
</script>

<template>
  <nav class="topbar navbar navbar-expand fixed-top">
    <RouterLink :to="{ name: 'Inicio' }" class="navbar-brand ms-3">
      <img src="/logo-topbar.svg" alt="FleetHub — Inicio" height="20" />
    </RouterLink>

    <div class="user-actions d-flex align-items-center gap-2 ms-auto text-white">
      <MorphIcon :icon="UserRound" :size="20" aria-hidden="true" />

      <span class="user-name text-truncate">{{ authStore.auth_user }}</span>

      <button
        type="button"
        class="btn btn-link btn-sm text-white"
        aria-label="Cerrar sesión"
        title="Cerrar sesión"
        @click="authStore.logout()"
      >
        <MorphIcon :icon="LogOut" :size="20" aria-hidden="true" />
      </button>
    </div>

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

.user-actions {
  min-width: 0;
}

.user-name {
  max-width: 150px;
}

.sidebar-toggle {
  margin-right: 1rem;
}

@media (min-width: 992px) {
  .sidebar-toggle {
    order: 1;
  }

  .user-actions {
    order: 2;
    margin-right: 1rem;
  }
}

@media (max-width: 575.98px) {
  .user-name {
    max-width: 90px;
  }
}
</style>
