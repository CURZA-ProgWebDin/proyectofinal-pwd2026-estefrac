<script setup>
import { storeToRefs } from 'pinia'
import { MorphIcon } from 'morphicons/vue'
import { History } from 'lucide'
import { useDashboardStore } from '../../stores/dashboard'

const dashboardStore = useDashboardStore()
const { resumen, cargando, errors } = storeToRefs(dashboardStore)

// No usa Date a propósito: evita el corrimiento a UTC.
const fechaBonita = (iso) => {
  if (!iso) {
    return ''
  }

  const [fecha, hora] = iso.split('T')
  const [anio, mes, dia] = fecha.split('-')

  return `${dia}/${mes}/${anio} ${(hora ?? '').slice(0, 5)}`
}
</script>

<template>
  <div class="card tarjeta-actividad text-white mb-4">
    <div class="card-header d-flex align-items-center justify-content-between">
      <div class="d-flex align-items-center gap-2">
        <MorphIcon :icon="History" :size="20" :stroke-width="1.5" />
        <span>Actividad reciente</span>
      </div>
      <RouterLink class="small text-decoration-none enlace" :to="{ name: 'Asignaciones' }">
        Ver todas
      </RouterLink>
    </div>
    <div class="card-body">
      <p v-if="errors[0]" class="text-danger small mb-0">{{ errors[0].message }}</p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!resumen?.actividad_reciente?.length" class="text-light text-opacity-50 mb-0">
        Todavía no hay movimientos.
      </p>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-actividad">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Vehículo</th>
              <th>Conductor</th>
              <th>Destino</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fila in resumen.actividad_reciente" :key="fila.id">
              <td>{{ fechaBonita(fila.fecha_salida) }}</td>
              <td class="fw-semibold">{{ fila.vehiculo.patente }}</td>
              <td>{{ fila.conductor.apellido }}, {{ fila.conductor.nombre }}</td>
              <td>{{ fila.destino ?? '—' }}</td>
              <td>
                <span class="badge rounded-pill" :class="`estado-${fila.estado}`">
                  {{ fila.estado }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tarjeta-actividad {
  background-color: #1e2023;
}
.tarjeta-actividad:hover {
  border-color: #08c39a;
}
.enlace {
  color: #08c39a;
}
.tabla-actividad {
  --bs-table-color: #fff;
  --bs-table-bg: transparent;
  --bs-table-border-color: rgb(255 255 255 / 12%);
  --bs-table-hover-color: #fff;
  --bs-table-hover-bg: rgb(255 255 255 / 4%);
}
.estado-abierta {
  background-color: #08c39a;
  color: #0a0a0a;
}
.estado-cerrada {
  background-color: #4b5057;
  color: #fff;
}
</style>
