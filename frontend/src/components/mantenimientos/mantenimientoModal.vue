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
  mantenimiento: {
    type: Object,
    default: null,
  },
  vehiculos: {
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

const titulo = props.modo === 'crear' ? 'Nuevo mantenimiento' : 'Editar mantenimiento'

const vehiculosActivos = computed(() => props.vehiculos.filter((v) => v.activo === 'S'))

const formulario = reactive({
  vehiculo_id: props.mantenimiento?.vehiculo_id ?? '',
  tipo: props.mantenimiento?.tipo ?? '',
  descripcion: props.mantenimiento?.descripcion ?? '',
  fecha_programada: props.mantenimiento?.fecha_programada ?? '',
  uso_registrado: props.mantenimiento?.uso_registrado ?? '',
  costo: props.mantenimiento?.costo ?? '',
  bloquea_uso: props.mantenimiento?.bloquea_uso ?? false,
})

const errorValidacion = ref('')

const emit = defineEmits(['cerrar', 'guardar'])

function guardar() {
  errorValidacion.value = ''

  if (props.modo === 'crear' && !formulario.vehiculo_id) {
    errorValidacion.value = 'El vehículo es requerido'
    return
  }

  if (!formulario.tipo.trim()) {
    errorValidacion.value = 'El tipo de mantenimiento es requerido'
    return
  }

  if (formulario.uso_registrado !== '' && Number(formulario.uso_registrado) < 0) {
    errorValidacion.value = 'El uso registrado debe ser un entero no negativo'
    return
  }

  if (formulario.costo !== '' && Number(formulario.costo) < 0) {
    errorValidacion.value = 'El costo debe ser un número válido no negativo'
    return
  }

  const datos = {
    tipo: formulario.tipo,
    descripcion: formulario.descripcion || null,
    fecha_programada: formulario.fecha_programada || null,
    uso_registrado: formulario.uso_registrado === '' ? null : Number(formulario.uso_registrado),
    costo: formulario.costo === '' ? null : Number(formulario.costo),
    bloquea_uso: Boolean(formulario.bloquea_uso),
  }

  if (props.modo === 'crear') {
    datos.vehiculo_id = Number(formulario.vehiculo_id)
  }

  emit('guardar', datos)
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
            <div v-if="modo === 'crear'" class="mb-3">
              <label for="vehiculo" class="form-label">Vehículo</label>
              <select id="vehiculo" v-model="formulario.vehiculo_id" class="form-select">
                <option value="" disabled>Seleccionar vehículo</option>
                <option v-for="vehiculo in vehiculosActivos" :key="vehiculo.id" :value="vehiculo.id">
                  {{ vehiculo.patente }} — {{ vehiculo.marca }} {{ vehiculo.modelo }}
                </option>
              </select>
            </div>

            <div class="mb-3">
              <label for="tipo" class="form-label">Tipo</label>
              <input
                id="tipo"
                v-model="formulario.tipo"
                type="text"
                class="form-control"
                placeholder="Ej: Cambio de aceite"
              />
            </div>

            <div class="mb-3">
              <label for="descripcion" class="form-label">Descripción</label>
              <textarea
                id="descripcion"
                v-model="formulario.descripcion"
                class="form-control"
                rows="2"
                placeholder="Ej: Cambio de aceite y filtros"
              ></textarea>
            </div>

            <div class="mb-3">
              <label for="fecha-programada" class="form-label">Fecha programada</label>
              <input
                id="fecha-programada"
                v-model="formulario.fecha_programada"
                type="date"
                class="form-control"
              />
            </div>

            <div class="mb-3">
              <label for="uso-registrado" class="form-label">Uso registrado (km)</label>
              <input
                id="uso-registrado"
                v-model="formulario.uso_registrado"
                type="number"
                min="0"
                class="form-control"
                placeholder="Ej: 15000"
              />
            </div>

            <div class="mb-3">
              <label for="costo" class="form-label">Costo</label>
              <input
                id="costo"
                v-model="formulario.costo"
                type="number"
                min="0"
                step="0.01"
                class="form-control"
                placeholder="Ej: 85000.50"
              />
            </div>

            <div class="form-check form-switch mb-3">
              <input
                id="bloquea-uso"
                v-model="formulario.bloquea_uso"
                class="form-check-input"
                type="checkbox"
              />
              <label for="bloquea-uso" class="form-check-label">Bloquea uso del vehículo</label>
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
