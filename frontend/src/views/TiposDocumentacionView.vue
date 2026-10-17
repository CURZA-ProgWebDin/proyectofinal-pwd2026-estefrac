<script setup>
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { MorphIcon } from 'morphicons/vue'
import { Pencil, Check, Plus, Minus } from 'lucide'
import { useTiposDocumentacionStore } from '../stores/tipos_documentacion'
import { useCrudModal } from '../composables/useCrudModal'
import TiposDocumentacionModal from '../components/tipos_documentacion/TiposDocumentacionModal.vue'

const tiposDocumentacionStore = useTiposDocumentacionStore()
const { tiposDocumentacion, cargando, errors } = storeToRefs(tiposDocumentacionStore)

const {
  modalAbierto,
  modoModal,
  registroSeleccionado,
  guardando,
  abrirCrear,
  abrirEditar,
  guardar,
} = useCrudModal(tiposDocumentacionStore, () => tiposDocumentacionStore.tipoDocumentacionActual, {
  crear: 'Tipo de documentación creado exitosamente',
  modificar: 'Tipo de documentación actualizado exitosamente',
})

onMounted(() => {
  tiposDocumentacionStore.listar()
})
</script>
<template>
  <div class="d-flex justify-content-end mb-3">
    <button
      class="btn btn-sm boton-verde d-inline-flex align-items-center gap-1"
      @click="abrirCrear"
    >
      <MorphIcon :icon="Plus" :size="14" />Nuevo
    </button>
  </div>

  <div class="card tarjeta-tipos text-white mb-4">
    <div class="card-body">
      <p v-if="errors[0] && !tiposDocumentacion.length" class="text-danger small mb-0">
        {{ errors[0].message }}
      </p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!tiposDocumentacion.length" class="text-light text-opacity-50 mb-0">
        Todavía no hay tipos cargados.
      </p>
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-tipos">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Obligatorio</th>
              <th>Estado</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="tipo in tiposDocumentacion" :key="tipo.id">
              <td>{{ tipo.nombre }}</td>
              <td><MorphIcon :icon="tipo.obligatorio ? Check : Minus" :size="14" /></td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="tipo.activo === 'S' ? 'estado-activo' : 'estado-inactivo'"
                >
                  {{ tipo.activo === 'S' ? 'activo' : 'inactivo' }}
                </span>
              </td>
              <td class="text-end">
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
  <TiposDocumentacionModal
    v-if="modalAbierto"
    :modo="modoModal"
    :tipo-documentacion="registroSeleccionado"
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
</style>
