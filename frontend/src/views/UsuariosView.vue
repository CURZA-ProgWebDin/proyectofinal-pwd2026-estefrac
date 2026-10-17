<script setup>
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { MorphIcon } from 'morphicons/vue'
import { Pencil, Plus } from 'lucide'
import { useUsuariosStore } from '../stores/usuarios'

const usuariosStore = useUsuariosStore()
const { usuarios, cargando, errors } = storeToRefs(usuariosStore)

onMounted(() => {
  usuariosStore.listar()
})
</script>

<template>
  <div class="d-flex justify-content-end mb-3">
    <button class="btn btn-sm boton-verde d-inline-flex align-items-center gap-1">
      <MorphIcon :icon="Plus" :size="14" />
      Nuevo
    </button>
  </div>

  <div class="card tarjeta-tipos text-white mb-4">
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 tabla-tipos">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Email</th>
              <th>Rol</th>
              <th>Estado</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="usuario in usuarios" :key="usuario.id">
              <td>{{ usuario.nombre }}</td>
              <td>{{ usuario.email }}</td>
              <td>{{ usuario.rol.nombre }}</td>
              <td>
                <span
                  class="badge rounded-pill"
                  :class="usuario.activo === 'S' ? 'estado-activo' : 'estado-inactivo'"
                  >{{ usuario.activo === 'S' ? 'activo' : 'inactivo' }}</span
                >
              </td>
              <td class="text-end">
                <button class="btn btn-sm boton-verde-outline">
                  <MorphIcon :icon="Pencil" :size="14" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
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
  table-layout: fixed;
}
.tabla-tipos thead th {
  color: var(--verde);
}
.tabla-tipos tbody td {
  color: rgb(255 255 255 / 72%);
  font-weight: 350;
}
.tabla-tipos th:last-child {
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
