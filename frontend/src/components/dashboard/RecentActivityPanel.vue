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
              <td :data-label="'Fecha'">{{ fechaBonita(fila.fecha_salida) }}</td>
              <td :data-label="'Vehículo'">{{ fila.vehiculo.patente }}</td>
              <td :data-label="'Conductor'">
                {{ fila.conductor.apellido }}, {{ fila.conductor.nombre }}
              </td>
              <td :data-label="'Destino'">{{ fila.destino ?? '—' }}</td>
              <td :data-label="'Estado'">
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
  background-color: var(--app-bg);
  border: 1px solid var(--borde);
}
.enlace {
  color: var(--verde);
}
.tabla-actividad {
  --bs-table-color: #fff;
  --bs-table-bg: transparent;
  --bs-table-border-color: var(--borde);
  --bs-table-hover-color: #fff;
  --bs-table-hover-bg: rgb(255 255 255 / 4%);
}
.tabla-actividad thead th {
  color: var(--verde);
}
.tabla-actividad tbody td {
  color: rgb(255 255 255 / 72%);
  font-weight: 350;
}
.estado-abierta {
  background-color: var(--verde);
  color: #0a0a0a;
}
.estado-cerrada {
  background-color: #4b5057;
  color: #fff;
}

@media (max-width: 767.98px) {
  .tabla-actividad {
    --bs-table-hover-bg: transparent;
  }

  .tabla-actividad thead {
    display: none;
  }
  .tabla-actividad,
  .tabla-actividad tbody,
  .tabla-actividad tr,
  .tabla-actividad td {
    display: block;
    width: 100%;
  }
  .tabla-actividad tr {
    border: 1px solid var(--borde);
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.75rem;
    background-color: rgb(255 255 255 / 3%);
  }
  .tabla-actividad td {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    border: 0;
    padding: 0.15rem 0;
  }
  .tabla-actividad td::before {
    content: attr(data-label);
    color: var(--verde);
  }
}
</style>
