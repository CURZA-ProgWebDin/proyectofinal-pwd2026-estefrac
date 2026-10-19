<script setup>
import { storeToRefs } from 'pinia'
import { computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { MorphIcon } from 'morphicons/vue'
import { Plus, Pencil } from 'lucide'
import { useTiposVehiculoStore } from '../stores/tipos_vehiculos'
import { useCrudModal } from '../composables/useCrudModal'
import TiposVehiculoModal from '../components/tipos_vehiculo/TiposVehiculoModal.vue'

const tiposVehiculoStore = useTiposVehiculoStore()
const { tiposVehiculo, cargando, errors } = storeToRefs(tiposVehiculoStore)

const {
  modalAbierto,
  modoModal,
  registroSeleccionado,
  guardando,
  abrirCrear,
  abrirEditar,
  guardar,
} = useCrudModal(tiposVehiculoStore, () => tiposVehiculoStore.tipoVehiculoActual, {
  crear: 'Tipo de vehículo creado exitosamente',
  modificar: 'Tipo de vehículo actualizado exitosamente',
})

const { rol_user } = storeToRefs(useAuthStore())
const esAdmin = computed(() => rol_user.value === 'admin')

onMounted(() => {
  tiposVehiculoStore.listar()
})
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
      <p v-if="errors[0] && !tiposVehiculo.length" class="text-danger small mb-0">
        {{ errors[0].message }}
      </p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!tiposVehiculo.length" class="text-light text-opacity-50 mb-0">
        Todavía no hay tipos cargados.
      </p>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-tipos">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Unidad de uso</th>
              <th>Estado</th>
              <th v-if="esAdmin" class="columna-acciones"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tipo in tiposVehiculo" :key="tipo.id">
              <td>{{ tipo.nombre }}</td>
              <td>{{ tipo.unidad_uso }}</td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="tipo.activo === 'S' ? 'estado-activo' : 'estado-inactivo'"
                >
                  {{ tipo.activo === 'S' ? 'activo' : 'inactivo' }}
                </span>
              </td>
              <td v-if="esAdmin" class="text-end">
                <button class="btn btn-sm boton-verde-outline" @click="abrirEditar(tipo)">
                  <MorphIcon :icon="Pencil" :size="14" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <TiposVehiculoModal
    v-if="modalAbierto"
    :modo="modoModal"
    :tipo-vehiculo="registroSeleccionado"
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
  min-width: 36rem;
}
.tabla-tipos thead th {
  color: var(--verde);
}
.tabla-tipos tbody td {
  color: rgb(255 255 255 / 72%);
  font-weight: 350;
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
.tabla-tipos .columna-acciones {
  width: 3rem;
}
</style>
