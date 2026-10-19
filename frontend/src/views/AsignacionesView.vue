<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import { MorphIcon } from 'morphicons/vue'
import { Ban, CheckCheck, Plus } from 'lucide'
import { useAsignacionesStore } from '../stores/asignaciones'
import { useVehiculosStore } from '../stores/vehiculos'
import { useConductoresStore } from '../stores/conductores'
import { useCrudModal } from '../composables/useCrudModal'
import asignacionModal from '../components/asignaciones/asignacionModal.vue'
import asignacionCerrarModal from '../components/asignaciones/asignacionCerrarModal.vue'

const asignacionesStore = useAsignacionesStore()
const { asignaciones, cargando, errors } = storeToRefs(asignacionesStore)

const vehiculosStore = useVehiculosStore()
const { vehiculos } = storeToRefs(vehiculosStore)

const conductoresStore = useConductoresStore()
const { conductores } = storeToRefs(conductoresStore)

const { modalAbierto, guardando, abrirCrear, guardar } = useCrudModal(
  asignacionesStore,
  () => asignacionesStore.asignacionActual,
  { crear: 'Asignación creada exitosamente', modificar: '' },
)

const cerrarModalAbierto = ref(false)
const asignacionACerrar = ref(null)
const cerrando = ref(false)

function abrirNuevaAsignacion() {
  vehiculosStore.listar()
  abrirCrear()
}

function abrirCerrar(asignacion) {
  asignacionACerrar.value = asignacion
  cerrarModalAbierto.value = true
}

async function confirmarCerrar(datos) {
  cerrando.value = true

  try {
    const ok = await asignacionesStore.cerrar(asignacionACerrar.value.id, datos.uso_regreso)

    if (ok) {
      toast.success('Asignación cerrada exitosamente')
      cerrarModalAbierto.value = false
      asignacionesStore.listar()
      vehiculosStore.listar()
    }
  } finally {
    cerrando.value = false
  }
}

async function cancelarAsignacion(asignacion) {
  const ok = await asignacionesStore.cancelar(asignacion.id)

  if (ok) {
    toast.success('Asignación cancelada exitosamente')
    asignacionesStore.listar()
    vehiculosStore.listar()
  } else if (errors.value[0]) {
    toast.error(errors.value[0].message)
  }
}

onMounted(() => {
  asignacionesStore.listar()
  vehiculosStore.listar()
  conductoresStore.listar()
})

function formatearFecha(fecha) {
  return fecha ? fecha.replace('T', ' ').slice(0, 16) : '—'
}
</script>

<template>
  <div class="d-flex justify-content-end mb-3">
    <button
      class="btn btn-sm boton-verde d-inline-flex align-items-center gap-1"
      @click="abrirNuevaAsignacion"
    >
      <MorphIcon :icon="Plus" :size="14" />
      Nueva asignación
    </button>
  </div>

  <div class="card tarjeta-tipos text-white mb-4">
    <div class="card-body">
      <p v-if="errors[0] && !asignaciones.length" class="text-danger small mb-0">
        {{ errors[0].message }}
      </p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!asignaciones.length" class="text-light text-opacity-50 mb-0">
        No hay asignaciones cargadas
      </p>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-tipos">
          <thead>
            <tr>
              <th>Vehículo</th>
              <th>Conductor</th>
              <th>Destino</th>
              <th>Salida</th>
              <th>Regreso</th>
              <th>Estado</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="asignacion in asignaciones" :key="asignacion.id">
              <td>{{ asignacion.vehiculo?.patente }}</td>
              <td>{{ asignacion.conductor?.nombre }} {{ asignacion.conductor?.apellido }}</td>
              <td>{{ asignacion.destino || '—' }}</td>
              <td>{{ formatearFecha(asignacion.fecha_salida) }}</td>
              <td>{{ formatearFecha(asignacion.fecha_regreso) }}</td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="asignacion.estado === 'abierta' ? 'estado-activo' : 'estado-inactivo'"
                >
                  {{ asignacion.estado }}
                </span>
              </td>
              <td class="text-end">
                <template v-if="asignacion.estado === 'abierta'">
                  <button
                    class="btn btn-sm boton-verde-outline me-1"
                    title="Cerrar asignación"
                    @click="abrirCerrar(asignacion)"
                  >
                    <MorphIcon :icon="CheckCheck" :size="14" />
                  </button>
                  <button
                    class="btn btn-sm boton-verde-outline"
                    title="Cancelar asignación"
                    @click="cancelarAsignacion(asignacion)"
                  >
                    <MorphIcon :icon="Ban" :size="14" />
                  </button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <asignacionModal
    v-if="modalAbierto"
    :vehiculos="vehiculos"
    :conductores="conductores"
    :errors="errors"
    :guardando="guardando"
    @guardar="guardar"
    @cerrar="modalAbierto = false"
  />

  <asignacionCerrarModal
    v-if="cerrarModalAbierto"
    :asignacion="asignacionACerrar"
    :errors="errors"
    :guardando="cerrando"
    @guardar="confirmarCerrar"
    @cerrar="cerrarModalAbierto = false"
  />
</template>

<style scoped>
.tarjeta-tipos {
  background-color: var(--app-bg);
  border: 1px solid var(--borde);
}
.tabla-tipos {
  --bs-table-color: #fff;
  --bs-table-bg: transparent;
  --bs-table-border-color: var(--borde);
  --bs-table-hover-color: #fff;
  --bs-table-hover-bg: rgb(255 255 255 / 4%);
  min-width: 52rem;
}
.tabla-tipos thead th {
  color: var(--verde);
}
.tabla-tipos tbody td {
  color: rgb(255 255 255 / 72%);
  font-weight: 350;
}
.tabla-tipos .columna-acciones {
  width: 6rem;
}
.estado-activo {
  background-color: var(--verde);
  color: #0a0a0a;
}
.estado-inactivo {
  background-color: #4b5057;
  color: #fff;
}
.boton-verde {
  background-color: var(--verde);
  border-color: var(--verde);
  color: #0a0a0a;
  font-weight: 600;
}
.boton-verde:hover {
  background-color: var(--verde-hover);
  border-color: var(--verde-hover);
  color: #0a0a0a;
}
.boton-verde-outline {
  border-color: var(--verde);
  color: var(--verde);
  background-color: transparent;
}
.boton-verde-outline:hover {
  background-color: var(--verde);
  color: #0a0a0a;
}
</style>
