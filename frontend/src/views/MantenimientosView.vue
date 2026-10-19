<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { toast } from 'vue3-toastify'
import { MorphIcon } from 'morphicons/vue'
import { Ban, CheckCheck, Pencil, Plus } from 'lucide'
import { useMantenimientosStore } from '../stores/mantenimientos'
import { useVehiculosStore } from '../stores/vehiculos'
import { useCrudModal } from '../composables/useCrudModal'
import mantenimientoModal from '../components/mantenimientos/mantenimientoModal.vue'
import mantenimientoRealizarModal from '../components/mantenimientos/mantenimientoRealizarModal.vue'

const mantenimientosStore = useMantenimientosStore()
const { mantenimientos, cargando, errors } = storeToRefs(mantenimientosStore)

const vehiculosStore = useVehiculosStore()
const { vehiculos } = storeToRefs(vehiculosStore)

const { modalAbierto, modoModal, registroSeleccionado, guardando, abrirCrear, abrirEditar, guardar } =
  useCrudModal(mantenimientosStore, () => mantenimientosStore.mantenimientoActual, {
    crear: 'Mantenimiento creado exitosamente',
    modificar: 'Mantenimiento actualizado exitosamente',
  })

const realizarModalAbierto = ref(false)
const mantenimientoARealizar = ref(null)
const realizando = ref(false)

function abrirRealizar(mantenimiento) {
  mantenimientoARealizar.value = mantenimiento
  realizarModalAbierto.value = true
}

async function confirmarRealizar(datos) {
  realizando.value = true

  try {
    const ok = await mantenimientosStore.realizar(mantenimientoARealizar.value.id, datos.fecha_realizada)

    if (ok) {
      toast.success('Mantenimiento realizado exitosamente')
      realizarModalAbierto.value = false
      mantenimientosStore.listar()
    }
  } finally {
    realizando.value = false
  }
}

async function cancelarMantenimiento(mantenimiento) {
  const ok = await mantenimientosStore.cancelar(mantenimiento.id)

  if (ok) {
    toast.success('Mantenimiento cancelado exitosamente')
    mantenimientosStore.listar()
  } else if (errors.value[0]) {
    toast.error(errors.value[0].message)
  }
}

const { rol_user } = storeToRefs(useAuthStore())
const esAdmin = computed(() => rol_user.value === 'admin')

onMounted(() => {
  mantenimientosStore.listar()
  vehiculosStore.listar()
})

function patenteVehiculo(id) {
  return vehiculos.value.find((vehiculo) => vehiculo.id === id)?.patente ?? '—'
}

function formatearFecha(fecha) {
  return fecha ?? '—'
}
</script>

<template>
  <div v-if="esAdmin" class="d-flex justify-content-end mb-3">
    <button
      class="btn btn-sm boton-verde d-inline-flex align-items-center gap-1"
      @click="abrirCrear"
    >
      <MorphIcon :icon="Plus" :size="14" />
      Nuevo
    </button>
  </div>

  <div class="card tarjeta-tipos text-white mb-4">
    <div class="card-body">
      <p v-if="errors[0] && !mantenimientos.length" class="text-danger small mb-0">
        {{ errors[0].message }}
      </p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!mantenimientos.length" class="text-light text-opacity-50 mb-0">
        No hay mantenimientos cargados
      </p>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-tipos">
          <thead>
            <tr>
              <th>Vehículo</th>
              <th>Tipo</th>
              <th>Programado</th>
              <th>Realizado</th>
              <th>Costo</th>
              <th>Bloquea</th>
              <th>Estado</th>
              <th v-if="esAdmin" class="columna-acciones"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mantenimiento in mantenimientos" :key="mantenimiento.id">
              <td>{{ patenteVehiculo(mantenimiento.vehiculo_id) }}</td>
              <td>{{ mantenimiento.tipo }}</td>
              <td>{{ formatearFecha(mantenimiento.fecha_programada) }}</td>
              <td>{{ formatearFecha(mantenimiento.fecha_realizada) }}</td>
              <td>{{ mantenimiento.costo ?? '—' }}</td>
              <td>{{ mantenimiento.bloquea_uso ? 'Sí' : 'No' }}</td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="mantenimiento.estado === 'pendiente' ? 'estado-pendiente' : 'estado-inactivo'"
                >
                  {{ mantenimiento.estado }}
                </span>
              </td>
              <td v-if="esAdmin" class="text-end">
                <button
                  class="btn btn-sm boton-verde-outline me-1"
                  title="Editar"
                  @click="abrirEditar(mantenimiento)"
                >
                  <MorphIcon :icon="Pencil" :size="14" />
                </button>
                <template v-if="mantenimiento.estado === 'pendiente'">
                  <button
                    class="btn btn-sm boton-verde-outline me-1"
                    title="Marcar realizado"
                    @click="abrirRealizar(mantenimiento)"
                  >
                    <MorphIcon :icon="CheckCheck" :size="14" />
                  </button>
                  <button
                    class="btn btn-sm boton-verde-outline"
                    title="Cancelar mantenimiento"
                    @click="cancelarMantenimiento(mantenimiento)"
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

  <mantenimientoModal
    v-if="modalAbierto"
    :modo="modoModal"
    :mantenimiento="registroSeleccionado"
    :vehiculos="vehiculos"
    :errors="errors"
    :guardando="guardando"
    @guardar="guardar"
    @cerrar="modalAbierto = false"
  />

  <mantenimientoRealizarModal
    v-if="realizarModalAbierto"
    :mantenimiento="mantenimientoARealizar"
    :errors="errors"
    :guardando="realizando"
    @guardar="confirmarRealizar"
    @cerrar="realizarModalAbierto = false"
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
  min-width: 56rem;
}
.tabla-tipos thead th {
  color: var(--verde);
}
.tabla-tipos tbody td {
  color: rgb(255 255 255 / 72%);
  font-weight: 350;
}
.tabla-tipos .columna-acciones {
  width: 8rem;
}
.estado-pendiente {
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
