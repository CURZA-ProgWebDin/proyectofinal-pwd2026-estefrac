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
  vehiculo: {
    type: Object,
    default: null,
  },
  tiposVehiculo: {
    type: Array,
    default: () => [],
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

const titulo = props.modo === 'crear' ? 'Nuevo vehículo' : 'Editar vehículo'

const formulario = reactive({
  patente: props.vehiculo?.patente ?? '',
  marca: props.vehiculo?.marca ?? '',
  modelo: props.vehiculo?.modelo ?? '',
  anio: props.vehiculo?.anio ?? '',
  tipo_vehiculo_id: props.vehiculo?.tipo_vehiculo_id ?? '',
  uso_actual: props.vehiculo?.uso_actual ?? 0,
  estado: props.vehiculo?.estado ?? 'disponible',
  activo: props.vehiculo?.activo ?? 'S',
})

const errorValidacion = ref('')

const emit = defineEmits(['cerrar', 'guardar'])

function guardar() {
  errorValidacion.value = ''

  if (!formulario.patente.trim()) {
    errorValidacion.value = 'La patente es requerida'
    return
  }

  if (!formulario.marca.trim()) {
    errorValidacion.value = 'La marca es requerida'
    return
  }

  if (!formulario.modelo.trim()) {
    errorValidacion.value = 'El modelo es requerido'
    return
  }

  if (!formulario.anio) {
    errorValidacion.value = 'El año es requerido'
    return
  }

  if (!formulario.tipo_vehiculo_id) {
    errorValidacion.value = 'El tipo de vehículo es requerido'
    return
  }

  if (formulario.uso_actual === '' || Number(formulario.uso_actual) < 0) {
    errorValidacion.value = 'El uso actual no puede ser negativo'
    return
  }

  emit('guardar', {
    ...formulario,
    anio: Number(formulario.anio),
    uso_actual: Number(formulario.uso_actual),
  })
}
</script>

<template>
  <div class="modal fade show d-block" tabindex="-1" @click.self="emit('cerrar')">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content tarjeta-modal text-white">
        <div class="modal-header">
          <h5 class="modal-title">{{ titulo }}</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            aria-label="Cerrar"
            @click="emit('cerrar')"
          ></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="guardar" novalidate>
            <div class="mb-3">
              <label for="patente" class="form-label">Patente</label>
              <input
                id="patente"
                v-model="formulario.patente"
                type="text"
                class="form-control"
                placeholder="Ej: AB123CD"
              />
            </div>

            <div class="mb-3">
              <label for="marca" class="form-label">Marca</label>
              <input
                id="marca"
                v-model="formulario.marca"
                type="text"
                class="form-control"
                placeholder="Ej: Toyota"
              />
            </div>

            <div class="mb-3">
              <label for="modelo" class="form-label">Modelo</label>
              <input
                id="modelo"
                v-model="formulario.modelo"
                type="text"
                class="form-control"
                placeholder="Ej: Hilux"
              />
            </div>

            <div class="mb-3">
              <label for="anio" class="form-label">Año</label>
              <input
                id="anio"
                v-model="formulario.anio"
                type="number"
                min="1900"
                max="2100"
                class="form-control"
                placeholder="Ej: 2020"
              />
            </div>

            <div class="mb-3">
              <label for="tipo-vehiculo" class="form-label">Tipo de vehículo</label>
              <select id="tipo-vehiculo" v-model="formulario.tipo_vehiculo_id" class="form-select">
                <option value="" disabled>Seleccionar tipo</option>
                <option v-for="tipo in tiposVehiculo" :key="tipo.id" :value="tipo.id">
                  {{ tipo.nombre }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label for="uso-actual" class="form-label">Uso actual (km)</label>
              <input
                id="uso-actual"
                v-model="formulario.uso_actual"
                type="number"
                min="0"
                class="form-control"
                placeholder="Ej: 15000"
              />
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
