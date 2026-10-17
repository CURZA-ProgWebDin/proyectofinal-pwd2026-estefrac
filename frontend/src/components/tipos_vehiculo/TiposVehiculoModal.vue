<script setup>
import { reactive, ref } from 'vue'
import { MorphIcon } from 'morphicons/vue'
import { AlertCircle } from 'lucide'

const props = defineProps({
  modo: {
    type: String,
    required: true,
    validator: (valor) => ['crear', 'editar'].includes(valor),
  },
  tipoVehiculo: {
    type: Object,
    default: null,
  },
  errors: {
    type: Array,
    default: () => [],
  },
  guardando: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['guardar', 'cerrar'])

const formulario = reactive({
  nombre: props.tipoVehiculo?.nombre ?? '',
  unidad_uso: props.tipoVehiculo?.unidad_uso ?? '',
  activo: props.tipoVehiculo?.activo ?? 'S',
})

const titulo = props.modo === 'crear' ? 'Nuevo tipo de vehículo' : 'Editar tipo de vehículo'

const errorValidacion = ref('')

function guardar() {
  errorValidacion.value = ''

  if (!formulario.nombre || !formulario.unidad_uso) {
    errorValidacion.value = 'El nombre y la unidad de uso son requeridos'
    return
  }

  emit('guardar', { ...formulario })
}
</script>

<template>
  <div class="modal fade show d-block" tabindex="-1" @click.self="emit('cerrar')">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content tarjeta-modal text-white">
        <div class="modal-header">
          <h5 class="modal-title">{{ titulo }}</h5>
          <button type="button" class="btn-close btn-close-white" @click="emit('cerrar')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardar" novalidate>
            <div class="mb-3">
              <label for="nombre" class="form-label">Nombre</label>
              <input
                id="nombre"
                v-model="formulario.nombre"
                type="text"
                class="form-control"
                maxlength="50"
                placeholder="Ej: Camioneta"
              />
            </div>
            <div class="mb-3">
              <label for="unidad-uso" class="form-label">Unidad de uso</label>
              <select id="unidad-uso" v-model="formulario.unidad_uso" class="form-select">
                <option value="" disabled>Seleccionar...</option>
                <option value="kilometros">kilómetros</option>
                <option value="horas">horas</option>
              </select>
            </div>
            <div v-if="modo === 'editar'" class="form-check form-switch mb-3">
              <input
                id="activo"
                v-model="formulario.activo"
                class="form-check-input"
                type="checkbox"
                true-value="S"
                false-value="N"
              />
              <label for="activo" class="form-check-label">Activo</label>
            </div>
            <div
              v-if="errorValidacion || errors.length"
              class="alerta-error d-flex align-items-center gap-2 mt-3 mb-3"
              role="alert"
            >
              <MorphIcon :icon="AlertCircle" :size="16" />
              <span>{{ errorValidacion || errors[0].message }}</span>
            </div>
            <div class="d-flex gap-2 justify-content-end">
              <button type="button" class="btn btn-outline-light" @click="emit('cerrar')">
                Cancelar
              </button>
              <button type="submit" class="btn boton-verde" :disabled="guardando">
                {{ guardando ? 'Guardando…' : 'Guardar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show"></div>
</template>

<style scoped>
.tarjeta-modal {
  background-color: var(--app-bg);
  border: 1px solid rgb(8 195 154 / 45%);
  border-radius: 0.5rem;
}
.tarjeta-modal .modal-header {
  border-bottom: 0;
}
.tarjeta-modal .form-check-input:checked {
  background-color: var(--verde);
  border-color: var(--verde);
}
.alerta-error {
  background-color: rgb(220 53 69 / 12%);
  border: 1px solid rgb(220 53 69 / 45%);
  color: #ff8a94;
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
}
.tarjeta-modal .form-control,
.tarjeta-modal .form-select {
  background-color: var(--app-bg);
  border-color: rgb(8 195 154 / 35%);
  color: #fff;
}
.tarjeta-modal .form-control::placeholder {
  color: rgb(255 255 255 / 50%);
}
.tarjeta-modal .form-control:focus,
.tarjeta-modal .form-select:focus {
  background-color: var(--app-bg);
  border-color: var(--verde);
  color: #fff;
  outline: 0;
  box-shadow: none;
}
.tarjeta-modal .modal-title {
  text-decoration: none;
  font-weight: 600;
}
.modal-backdrop {
  --bs-backdrop-opacity: 0.8;
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
</style>
