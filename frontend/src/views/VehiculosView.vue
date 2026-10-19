<script setup>
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { MorphIcon } from 'morphicons/vue'
import { Pencil, Plus } from 'lucide'
import { useVehiculosStore } from '../stores/vehiculos'
import { useTiposVehiculoStore } from '../stores/tipos_vehiculos'
import { useCrudModal } from '../composables/useCrudModal'
import vehiculoModal from '../components/vehiculos/vehiculoModal.vue'

const vehiculosStore = useVehiculosStore()
const { vehiculos, cargando, errors } = storeToRefs(vehiculosStore)

const tiposVehiculoStore = useTiposVehiculoStore()
const { tiposVehiculo } = storeToRefs(tiposVehiculoStore)

const { modalAbierto, modoModal, registroSeleccionado, guardando, abrirCrear, abrirEditar, guardar } =
  useCrudModal(vehiculosStore, () => vehiculosStore.vehiculoActual, {
    crear: 'Vehículo creado exitosamente',
    modificar: 'Vehículo actualizado exitosamente',
  })

const { rol_user } = storeToRefs(useAuthStore())
const esAdmin = computed(() => rol_user.value === 'admin')

onMounted(() => {
  vehiculosStore.listar()
  tiposVehiculoStore.listar()
})

function nombreTipo(id) {
  return tiposVehiculo.value.find((tipo) => tipo.id === id)?.nombre ?? '—'
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
      <p v-if="errors[0] && !vehiculos.length" class="text-danger small mb-0">
        {{ errors[0].message }}
      </p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!vehiculos.length" class="text-light text-opacity-50 mb-0">
        No hay vehículos cargados
      </p>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-tipos">
          <thead>
            <tr>
              <th>Patente</th>
              <th>Marca</th>
              <th>Modelo</th>
              <th>Año</th>
              <th>Tipo</th>
              <th>Uso (km)</th>
              <th>Estado</th>
              <th v-if="esAdmin" class="columna-acciones"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vehiculo in vehiculos" :key="vehiculo.id">
              <td>{{ vehiculo.patente }}</td>
              <td>{{ vehiculo.marca }}</td>
              <td>{{ vehiculo.modelo }}</td>
              <td>{{ vehiculo.anio }}</td>
              <td>{{ nombreTipo(vehiculo.tipo_vehiculo_id) }}</td>
              <td>{{ vehiculo.uso_actual }}</td>
              <td>
                <span class="badge rounded-pill badge-estado">
                  {{ vehiculo.estado.replace('_', ' ') }}
                </span>
              </td>
              <td v-if="esAdmin" class="text-end">
                <button class="btn btn-sm boton-verde-outline" @click="abrirEditar(vehiculo)">
                  <MorphIcon :icon="Pencil" :size="14" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <vehiculoModal
    v-if="modalAbierto"
    :modo="modoModal"
    :vehiculo="registroSeleccionado"
    :tipos-vehiculo="tiposVehiculo"
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
  min-width: 42rem;
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
.badge-estado {
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
