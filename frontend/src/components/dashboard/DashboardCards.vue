<script setup>
import { storeToRefs } from 'pinia'
import { Car, ClipboardList, FileText, UserRound, Wrench } from 'lucide'
import DashboardCard from './DashboardCard.vue'
import { useDashboardStore } from '../../stores/dashboard'

const dashboardStore = useDashboardStore()
const { resumen, cargando, errors } = storeToRefs(dashboardStore)
</script>

<template>
  <div class="row mt-4">
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Vehículos activos"
        :icono="Car"
        :valor="resumen?.vehiculos_activos ?? 0"
        :cargando="cargando"
        :error="errors[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Conductores activos"
        :icono="UserRound"
        :valor="resumen?.conductores_activos ?? 0"
        :cargando="cargando"
        :error="errors[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Vehículos asignados"
        :icono="ClipboardList"
        :valor="resumen?.vehiculos_asignados ?? 0"
        :cargando="cargando"
        :error="errors[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Mantenimientos próximos"
        :icono="Wrench"
        :valor="resumen?.mantenimientos_programados ?? 0"
        :cargando="cargando"
        :error="errors[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Documentos por vencer"
        :icono="FileText"
        :valor="resumen?.documentos_por_vencer ?? 0"
        :cargando="cargando"
        :error="errors[0]?.message ?? ''"
      />
    </div>
  </div>
</template>
