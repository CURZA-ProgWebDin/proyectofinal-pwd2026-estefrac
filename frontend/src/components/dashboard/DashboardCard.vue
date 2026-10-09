<script setup>
import { MorphIcon } from 'morphicons/vue'

defineProps({
  titulo: {
    type: String,
    required: true,
  },
  valor: {
    type: Number,
    default: 0,
  },
  icono: {
    required: true,
  },
  cargando: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <div class="card dashboard-card text-white h-100">
    <div class="card-body">
      <div class="dashboard-card-title d-flex align-items-start gap-2 mb-1">
        <MorphIcon class="flex-shrink-0" :icon="icono" :size="20" :stroke-width="1.5" />
        <h2 class="fs-6 fw-light mb-0">{{ titulo }}</h2>
      </div>
      <p v-if="error" class="text-danger text-center small mb-0">
        {{ error }}
      </p>
      <p v-else-if="cargando" class="text-center mb-0">Cargando...</p>
      <p v-else class="dashboard-card-value fw-bold text-center mb-0">
        {{ valor }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.dashboard-card {
  background-color: var(--app-bg);
  border: 1px solid var(--borde);
}
.dashboard-card-title {
  color: var(--verde);
  min-height: 2.4rem;
}
.dashboard-card:hover {
  border-color: var(--verde);
}
.dashboard-card-title h2 {
  line-height: 1.2rem;
}
.dashboard-card-value {
  font-size: 3rem;
}
</style>
