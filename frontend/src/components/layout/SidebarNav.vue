<script setup>
import { menuRoutes } from '../../router/configs/navigation.js'
</script>

<template>
  <nav aria-label="Menú principal" class="d-flex flex-column gap-2 p-3">
    <RouterLink v-for="route in menuRoutes" :key="route.name" :to="{ name: route.name }">{{
      route.meta.titulo
    }}</RouterLink>
  </nav>
</template>
