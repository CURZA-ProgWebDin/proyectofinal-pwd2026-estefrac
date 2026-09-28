<script setup>
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const { auth_user, rol_user } = storeToRefs(authStore)
</script>

<template>
  <main>
    <h1>Ingresaste correctamente</h1>
    <p>Usuario: {{ auth_user }}</p>
    <p>Rol: {{ rol_user }}</p>
    <button type="button" @click="authStore.logout()">Cerrar sesión</button>
  </main>
</template>
