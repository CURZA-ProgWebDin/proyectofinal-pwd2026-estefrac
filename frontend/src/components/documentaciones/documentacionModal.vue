<script setup>
import { computed, reactive, ref } from 'vue'
import { MorphIcon } from 'morphicons/vue'
import { AlertCircle } from 'lucide'

const props = defineProps({
  modo: {
    type: String,
    required: true,
    validator: (valor) => ['crear', 'editar'].includes(valor),
  },
  documentacion: {
    type: Object,
    default: null,
  },
  vehiculos: {
    type: Array,
    default: () => [],
  },
  tiposDocumentacion: {
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

const titulo = props.modo === 'crear' ? 'Nueva documentación' : 'Editar documentación'

const vehiculosActivos = computed(() => props.vehiculos.filter((v) => v.activo === 'S'))

const formulario = reactive({
  vehiculo_id: props.documentacion?.vehiculo_id ?? '',
  tipo_documentacion_id: props.documentacion?.tipo_documentacion_id ?? '',
  numero: props.documentacion?.numero ?? '',
  fecha_emision: props.documentacion?.fecha_emision ?? '',
  fecha_vencimiento: props.documentacion?.fecha_vencimiento ?? '',
  activo: props.documentacion?.activo ?? 'S',
})

const errorValidacion = ref('')

const emit = defineEmits(['cerrar', 'guardar'])

function guardar() {
  errorValidacion.value = ''

  if (!formulario.vehiculo_id) {
    errorValidacion.value = 'El vehículo es requerido'
    return
  }

  if (!formulario.tipo_documentacion_id) {
    errorValidacion.value = 'El tipo de documentación es requerido'
    return
  }

  if (!formulario.fecha_vencimiento) {
    errorValidacion.value = 'La fecha de vencimiento es requerida'
    return
  }

  if (formulario.fecha_emision && formulario.fecha_emision > formulario.fecha_vencimiento) {
    errorValidacion.value = 'La fecha de emisión no puede ser posterior al vencimiento'
    return
  }

  emit('guardar', {
    ...formulario,
    vehiculo_id: Number(formulario.vehiculo_id),
    tipo_documentacion_id: Number(formulario.tipo_documentacion_id),
    numero: formulario.numero || null,
    fecha_emision: formulario.fecha_emision || null,
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
              <label for="vehiculo" class="form-label">Vehículo</label>
              <select id="vehiculo" v-model="formulario.vehiculo_id" class="form-select">
                <option value="" disabled>Seleccionar vehículo</option>
                <option v-for="vehiculo in vehiculosActivos" :key="vehiculo.id" :value="vehiculo.id">
                  {{ vehiculo.patente }} — {{ vehiculo.marca }} {{ vehiculo.modelo }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label for="tipo-documentacion" class="form-label">Tipo de documentación</label>
              <select id="tipo-documentacion" v-model="formulario.tipo_documentacion_id" class="form-select">
                <option value="" disabled>Seleccionar tipo</option>
                <option v-for="tipo in tiposDocumentacion" :key="tipo.id" :value="tipo.id">
                  {{ tipo.nombre }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label for="numero" class="form-label">Número</label>
              <input
                id="numero"
                v-model="formulario.numero"
                type="text"
                class="form-control"
                placeholder="Ej: 123456789"
              />
            </div>

            <div class="mb-3">
              <label for="fecha-emision" class="form-label">Fecha de emisión</label>
              <input
                id="fecha-emision"
                v-model="formulario.fecha_emision"
                type="date"
                class="form-control"
              />
            </div>

            <div class="mb-3">
              <label for="fecha-vencimiento" class="form-label">Fecha de vencimiento</label>
              <input
                id="fecha-vencimiento"
                v-model="formulario.fecha_vencimiento"
                type="date"
                class="form-control"
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
.tarjeta-modal .form-control[type='date']::-webkit-calendar-picker-indicator {
  filter: invert(1);
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
