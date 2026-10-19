<script setup>
import { reactive, ref } from 'vue'
import { MorphIcon } from 'morphicons/vue'
import { AlertCircle } from 'lucide'

const props = defineProps({
  asignacion: {
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

const formulario = reactive({
  uso_regreso: props.asignacion?.uso_salida ?? '',
})

const errorValidacion = ref('')

const emit = defineEmits(['cerrar', 'guardar'])

function guardar() {
  errorValidacion.value = ''

  if (formulario.uso_regreso === '' || formulario.uso_regreso === null) {
    errorValidacion.value = 'El uso de regreso es requerido'
    return
  }

  if (Number(formulario.uso_regreso) < props.asignacion.uso_salida) {
    errorValidacion.value = 'El uso de regreso no puede ser menor al de salida'
    return
  }

  emit('guardar', { uso_regreso: Number(formulario.uso_regreso) })
}
</script>

<template>
  <div class="modal fade show d-block" tabindex="-1" @click.self="emit('cerrar')">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content tarjeta-modal text-white">
        <div class="modal-header">
          <h5 class="modal-title">Cerrar asignación</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            aria-label="Cerrar"
            @click="emit('cerrar')"
          ></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="guardar" novalidate>
            <p class="mb-3 small">
              {{ asignacion?.vehiculo?.patente }} — salida con {{ asignacion?.uso_salida }} km
            </p>

            <div class="mb-3">
              <label for="uso-regreso" class="form-label">Uso de regreso (km)</label>
              <input
                id="uso-regreso"
                v-model="formulario.uso_regreso"
                type="number"
                :min="asignacion?.uso_salida"
                class="form-control"
                placeholder="Ej: 15300"
              />
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
                {{ guardando ? 'Cerrando…' : 'Cerrar asignación' }}
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
.tarjeta-modal .form-control {
  background-color: var(--app-bg);
  border-color: rgb(8 195 154 / 35%);
  color: #fff;
}
.tarjeta-modal .form-control::placeholder {
  color: rgb(255 255 255 / 50%);
}
.tarjeta-modal .form-control:focus {
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
