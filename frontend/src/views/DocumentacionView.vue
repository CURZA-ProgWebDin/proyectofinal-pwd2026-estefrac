<script setup>
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { MorphIcon } from 'morphicons/vue'
import { Pencil, Plus } from 'lucide'
import { useDocumentacionesStore } from '../stores/documentaciones'
import { useVehiculosStore } from '../stores/vehiculos'
import { useTiposDocumentacionStore } from '../stores/tipos_documentacion'
import { useCrudModal } from '../composables/useCrudModal'
import documentacionModal from '../components/documentaciones/documentacionModal.vue'

const documentacionesStore = useDocumentacionesStore()
const { documentaciones, cargando, errors } = storeToRefs(documentacionesStore)

const vehiculosStore = useVehiculosStore()
const { vehiculos } = storeToRefs(vehiculosStore)

const tiposDocumentacionStore = useTiposDocumentacionStore()
const { tiposDocumentacion } = storeToRefs(tiposDocumentacionStore)

const { modalAbierto, modoModal, registroSeleccionado, guardando, abrirCrear, abrirEditar, guardar } =
  useCrudModal(documentacionesStore, () => documentacionesStore.documentacionActual, {
    crear: 'Documentación vehicular creada exitosamente',
    modificar: 'Documentación vehicular actualizada exitosamente',
  })

const { rol_user } = storeToRefs(useAuthStore())
const esAdmin = computed(() => rol_user.value === 'admin')

onMounted(() => {
  documentacionesStore.listar()
  vehiculosStore.listar()
  tiposDocumentacionStore.listar()
})

function patenteVehiculo(id) {
  return vehiculos.value.find((vehiculo) => vehiculo.id === id)?.patente ?? '—'
}

function nombreTipo(id) {
  return tiposDocumentacion.value.find((tipo) => tipo.id === id)?.nombre ?? '—'
}
</script>

<template>
  <div v-if="esAdmin" class="d-flex justify-content-end mb-3">
    <button
      class="btn btn-sm boton-verde d-inline-flex align-items-center gap-1"
      @click="abrirCrear"
    >
      <MorphIcon :icon="Plus" :size="14" />
      Nueva
    </button>
  </div>

  <div class="card tarjeta-tipos text-white mb-4">
    <div class="card-body">
      <p v-if="errors[0] && !documentaciones.length" class="text-danger small mb-0">
        {{ errors[0].message }}
      </p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!documentaciones.length" class="text-light text-opacity-50 mb-0">
        No hay documentaciones cargadas
      </p>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-tipos">
          <thead>
            <tr>
              <th>Vehículo</th>
              <th>Tipo</th>
              <th>Número</th>
              <th>Emisión</th>
              <th>Vencimiento</th>
              <th>Estado</th>
              <th v-if="esAdmin" class="columna-acciones"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="documentacion in documentaciones" :key="documentacion.id">
              <td>{{ patenteVehiculo(documentacion.vehiculo_id) }}</td>
              <td>{{ nombreTipo(documentacion.tipo_documentacion_id) }}</td>
              <td>{{ documentacion.numero || '—' }}</td>
              <td>{{ documentacion.fecha_emision || '—' }}</td>
              <td>{{ documentacion.fecha_vencimiento }}</td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="documentacion.activo === 'S' ? 'estado-activo' : 'estado-inactivo'"
                >
                  {{ documentacion.activo === 'S' ? 'activo' : 'inactivo' }}
                </span>
              </td>
              <td v-if="esAdmin" class="text-end">
                <button class="btn btn-sm boton-verde-outline" @click="abrirEditar(documentacion)">
                  <MorphIcon :icon="Pencil" :size="14" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <documentacionModal
    v-if="modalAbierto"
    :modo="modoModal"
    :documentacion="registroSeleccionado"
    :vehiculos="vehiculos"
    :tipos-documentacion="tiposDocumentacion"
    :errors="errors"
    :guardando="guardando"
    @guardar="guardar"
    @cerrar="modalAbierto = false"
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
  min-width: 48rem;
}
.tabla-tipos thead th {
  color: var(--verde);
}
.tabla-tipos tbody td {
  color: rgb(255 255 255 / 72%);
  font-weight: 350;
}
.tabla-tipos .columna-acciones {
  width: 3rem;
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
