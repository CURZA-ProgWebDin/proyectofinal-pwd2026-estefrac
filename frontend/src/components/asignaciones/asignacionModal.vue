<script setup>
import { computed, reactive, ref } from 'vue'
import { MorphIcon } from 'morphicons/vue'
import { AlertCircle } from 'lucide'

const props = defineProps({
  vehiculos: {
    type: Array,
    default: () => [],
  },
  conductores: {
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

const vehiculosDisponibles = computed(() =>
  props.vehiculos.filter((v) => v.activo === 'S' && v.estado === 'disponible'),
)

const conductoresActivos = computed(() => props.conductores.filter((c) => c.activo === 'S'))

const formulario = reactive({
  vehiculo_id: '',
  conductor_id: '',
  destino: '',
  motivo: '',
})

const errorValidacion = ref('')

const emit = defineEmits(['cerrar', 'guardar'])

function guardar() {
  errorValidacion.value = ''

  if (!formulario.vehiculo_id) {
    errorValidacion.value = 'El vehículo es requerido'
    return
  }

  if (!formulario.conductor_id) {
    errorValidacion.value = 'El conductor es requerido'
    return
  }

  emit('guardar', { ...formulario, vehiculo_id: Number(formulario.vehiculo_id), conductor_id: Number(formulario.conductor_id) })
}
</script>

<template>
  <div class="modal fade show d-block" tabindex="-1" @click.self="emit('cerrar')">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content tarjeta-modal text-white">
        <div class="modal-header">
          <h5 class="modal-title">Nueva asignación</h5>
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
              <label for="vehiculo" class="form-label">Vehículo</label>
              <select id="vehiculo" v-model="formulario.vehiculo_id" class="form-select">
                <option value="" disabled>Seleccionar vehículo</option>
                <option v-for="vehiculo in vehiculosDisponibles" :key="vehiculo.id" :value="vehiculo.id">
                  {{ vehiculo.patente }} — {{ vehiculo.marca }} {{ vehiculo.modelo }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label for="conductor" class="form-label">Conductor</label>
              <select id="conductor" v-model="formulario.conductor_id" class="form-select">
                <option value="" disabled>Seleccionar conductor</option>
                <option v-for="conductor in conductoresActivos" :key="conductor.id" :value="conductor.id">
                  {{ conductor.nombre }} {{ conductor.apellido }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label for="destino" class="form-label">Destino</label>
              <input
                id="destino"
                v-model="formulario.destino"
                type="text"
                class="form-control"
                placeholder="Ej: Viedma"
              />
            </div>

            <div class="mb-3">
              <label for="motivo" class="form-label">Motivo</label>
              <textarea
                id="motivo"
                v-model="formulario.motivo"
                class="form-control"
                rows="2"
                placeholder="Ej: Entrega de materiales"
              ></textarea>
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
