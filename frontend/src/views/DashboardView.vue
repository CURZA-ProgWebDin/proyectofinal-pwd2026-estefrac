<script setup>
import { onMounted } from 'vue'
import DashboardCards from '../components/dashboard/DashboardCards.vue'
import { useDashboardStore } from '../stores/dashboard'

const dashboardStore = useDashboardStore()

onMounted(() => {
  dashboardStore.listar()
})
</script>

<template>
  <section>
    <h1>Inicio</h1>
    <p class="fs-5 text-light text-opacity-50">Resumen general de la gestión de vehículos.</p>
    <DashboardCards />
  </section>
</template>
