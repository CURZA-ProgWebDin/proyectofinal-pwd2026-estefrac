<script setup>
import DashboardCard from './DashboardCard.vue'
import { Car, UserRound, ClipboardList, Wrench, FileText } from 'lucide'
import { onMounted, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useVehiculosStore } from '../../stores/vehiculos'
import { useConductoresStore } from '../../stores/conductores'
import { useAsignacionesStore } from '../../stores/asignaciones'
import { useMantenimientosStore } from '../../stores/mantenimientos'
import { useDocumentacionesStore } from '../../stores/documentaciones'

const vehiculosStore = useVehiculosStore()
const {
  vehiculos,
  cargando: cargandoVehiculos,
  errors: errorsVehiculos,
} = storeToRefs(vehiculosStore)
const totalVehiculosActivos = computed(() => {
  return vehiculos.value.filter((vehiculo) => vehiculo.activo === 'S').length
})

const conductoresStore = useConductoresStore()
const {
  conductores,
  cargando: cargandoConductores,
  errors: errorsConductores,
} = storeToRefs(conductoresStore)
const totalConductoresActivos = computed(() => {
  return conductores.value.filter((conductor) => conductor.activo === 'S').length
})

const asignacionesStore = useAsignacionesStore()
const {
  asignaciones,
  cargando: cargandoAsignaciones,
  errors: errorsAsignaciones,
} = storeToRefs(asignacionesStore)
const totalVehiculosAsignados = computed(() => {
  return asignaciones.value.filter((asignacion) => asignacion.estado === 'abierta').length
})

const hoy = new Date()
const limite = new Date(hoy)
limite.setDate(limite.getDate() + 30)
const fechaLocal = (fecha) => {
  return `${fecha.getFullYear()}-${String(fecha.getMonth() + 1).padStart(2, '0')}-${String(fecha.getDate()).padStart(2, '0')}`
}
const fechaHoy = fechaLocal(hoy)
const fechaLimite = fechaLocal(limite)

const mantenimientosStore = useMantenimientosStore()
const {
  mantenimientos,
  cargando: cargandoMantenimientos,
  errors: errorsMantenimientos,
} = storeToRefs(mantenimientosStore)
const totalMantenimientosPendientes = computed(() => {
  return mantenimientos.value.filter(
    (mantenimiento) =>
      mantenimiento.activo === 'S' &&
      mantenimiento.estado === 'pendiente' &&
      mantenimiento.fecha_programada >= fechaHoy &&
      mantenimiento.fecha_programada <= fechaLimite,
  ).length
})

const documentacionesStore = useDocumentacionesStore()
const {
  documentaciones,
  cargando: cargandoDocumentaciones,
  errors: errorsDocumentaciones,
} = storeToRefs(documentacionesStore)
const totalDocumentosPorVencer = computed(() => {
  return documentaciones.value.filter(
    (documentacion) =>
      documentacion.activo === 'S' &&
      documentacion.fecha_vencimiento >= fechaHoy &&
      documentacion.fecha_vencimiento <= fechaLimite,
  ).length
})

onMounted(() => {
  vehiculosStore.listar()
  conductoresStore.listar()
  asignacionesStore.listar()
  mantenimientosStore.listar()
  documentacionesStore.listar()
})
</script>
<template>
  <div class="row mt-4">
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Vehículos activos"
        :icono="Car"
        :valor="totalVehiculosActivos"
        :cargando="cargandoVehiculos"
        :error="errorsVehiculos[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Conductores activos"
        :icono="UserRound"
        :valor="totalConductoresActivos"
        :cargando="cargandoConductores"
        :error="errorsConductores[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Vehículos asignados"
        :icono="ClipboardList"
        :valor="totalVehiculosAsignados"
        :cargando="cargandoAsignaciones"
        :error="errorsAsignaciones[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Mantenimientos próximos"
        :icono="Wrench"
        :valor="totalMantenimientosPendientes"
        :cargando="cargandoMantenimientos"
        :error="errorsMantenimientos[0]?.message ?? ''"
      />
    </div>
    <div class="col-xl col-md-6 mb-4">
      <DashboardCard
        titulo="Documentos por vencer"
        :icono="FileText"
        :valor="totalDocumentosPorVencer"
        :cargando="cargandoDocumentaciones"
        :error="errorsDocumentaciones[0]?.message ?? ''"
      />
    </div>
  </div>
</template>
