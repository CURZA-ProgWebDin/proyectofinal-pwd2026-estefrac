<script setup>
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { MorphIcon } from 'morphicons/vue'
import { Pencil, Plus } from 'lucide'
import { useUsuariosStore } from '../stores/usuarios'
import { useRolesStore } from '../stores/roles'
import { useCrudModal } from '../composables/useCrudModal'
import usuarioModal from '../components/usuarios/usuarioModal.vue'

const usuariosStore = useUsuariosStore()
const { usuarios, cargando, errors } = storeToRefs(usuariosStore)

const rolesStore = useRolesStore()
const { roles } = storeToRefs(rolesStore)

const {
  modalAbierto,
  modoModal,
  registroSeleccionado,
  guardando,
  abrirCrear,
  abrirEditar,
  guardar,
} = useCrudModal(usuariosStore, () => usuariosStore.usuarioActual, {
  crear: 'Usuario creado exitosamente',
  modificar: 'Usuario actualizado exitosamente',
})

onMounted(() => {
  usuariosStore.listar()
  rolesStore.listar()
})
</script>

<template>
  <div class="d-flex justify-content-end mb-3">
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
      <p v-if="errors[0] && !usuarios.length" class="text-danger small mb-0">
        {{ errors[0].message }}
      </p>
      <p v-else-if="cargando" class="mb-0">Cargando...</p>
      <p v-else-if="!usuarios.length" class="text-light text-opacity-50 mb-0">
        No hay Usuarios cargados
      </p>
      <div v-else class="table-responsive">
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
                <button class="btn btn-sm boton-verde-outline" @click="abrirEditar(usuario)">
                  <MorphIcon :icon="Pencil" :size="14" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <usuarioModal
    v-if="modalAbierto"
    :modo="modoModal"
    :usuario="registroSeleccionado"
    :roles="roles"
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
