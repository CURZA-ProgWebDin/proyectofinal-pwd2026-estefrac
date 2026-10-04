<script setup>
import { useAuthStore } from '../../stores/auth'
import { storeToRefs } from 'pinia'
import {
  inicioRoutes,
  gestionRoutes,
  administracionRoutes,
  parametrosRoutes,
} from '../../router/configs/navigation.js'
import { MorphIcon } from 'morphicons/vue'
import { Settings, ChevronRight } from 'lucide'

const authStore = useAuthStore()
const { rol_user } = storeToRefs(authStore)
</script>

<template>
  <nav class="d-flex flex-column gap-2 p-3 text-light text-opacity-50">
    <RouterLink
      class="text-light text-opacity-50 text-decoration-none d-flex align-items-center gap-2"
      v-for="route in inicioRoutes"
      :key="route.name"
      :to="{ name: route.name }"
    >
      <MorphIcon :icon="route.meta.icono" :size="18" class="flex-shrink-0" aria-hidden="true" />
      <span>{{ route.meta.titulo }}</span></RouterLink
    >

    <section
      class="mt-3"
      v-if="
        gestionRoutes.some(
          (route) => route.meta.rol_access && route.meta.rol_access.includes(rol_user),
        )
      "
    >
      <h2 class="fs-6 text-uppercase">Gestión</h2>

      <div class="d-flex flex-column gap-2">
        <template v-for="route in gestionRoutes" :key="route.name">
          <RouterLink
            v-if="route.meta.rol_access?.includes(rol_user)"
            class="text-light text-opacity-50 text-decoration-none d-flex align-items-center gap-2"
            :to="{ name: route.name }"
          >
            <MorphIcon
              :icon="route.meta.icono"
              :size="18"
              class="flex-shrink-0"
              aria-hidden="true"
            />
            <span>{{ route.meta.titulo }}</span>
          </RouterLink>
        </template>
      </div>
    </section>

    <section
      class="mt-3"
      v-if="
        administracionRoutes.some((route) => route.meta.rol_access?.includes(rol_user)) ||
        parametrosRoutes.some((route) => route.meta.rol_access?.includes(rol_user))
      "
    >
      <h2 class="fs-6 text-uppercase">Administración</h2>
      <div class="d-flex flex-column gap-2">
        <template v-for="route in administracionRoutes" :key="route.name">
          <RouterLink
            v-if="route.meta.rol_access?.includes(rol_user)"
            class="text-light text-opacity-50 text-decoration-none d-flex align-items-center gap-2"
            :to="{ name: route.name }"
          >
            <MorphIcon
              :icon="route.meta.icono"
              :size="18"
              class="flex-shrink-0"
              aria-hidden="true"
            />
            <span>{{ route.meta.titulo }}</span>
          </RouterLink>
        </template>
        <details v-if="parametrosRoutes.some((route) => route.meta.rol_access?.includes(rol_user))">
          <summary class="d-flex align-items-center gap-2 text-light text-opacity-50">
            <MorphIcon :icon="Settings" :size="18" class="flex-shrink-0" aria-hidden="true" />

            <span>Parámetros</span>

            <MorphIcon
              :icon="ChevronRight"
              :size="16"
              class="parameters-chevron flex-shrink-0"
              aria-hidden="true"
            />
          </summary>
          <div class="d-flex flex-column gap-2 mt-2">
            <template v-for="route in parametrosRoutes" :key="route.name">
              <RouterLink
                v-if="route.meta.rol_access?.includes(rol_user)"
                class="text-light text-opacity-50 text-decoration-none d-flex align-items-center gap-2 parameter-link"
                :to="{ name: route.name }"
              >
                <MorphIcon
                  :icon="ChevronRight"
                  :size="14"
                  class="parameters-chevron flex-shrink-0"
                  aria-hidden="true"
                />
                <span class="small">{{ route.meta.titulo }}</span>
              </RouterLink>
            </template>
          </div>
        </details>
      </div>
    </section>
  </nav>
</template>

<style scoped>
summary {
  list-style: none;
  cursor: pointer;
}

summary::-webkit-details-marker {
  display: none;
}

details[open] > summary .parameters-chevron {
  transform: rotate(90deg);
}

nav a:hover,
summary:hover {
  --bs-text-opacity: 0.75;
}

nav a,
summary {
  padding: 6px 8px;
  border-radius: 5px;
  font-weight: 300;
}

nav a.router-link-exact-active:not(.parameter-link),
details:has(a.router-link-exact-active) > summary {
  background: linear-gradient(90deg, #08c39a, #f4df63);
  color: #111216 !important;
  font-weight: 600;
}

nav a.parameter-link.router-link-exact-active {
  --bs-text-opacity: 0.75;
}
</style>
