<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['submit'])

const user = reactive({
  nombre: '',
  password: '',
})

function handleSubmit() {
  emit('submit', { ...user })
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="login-nombre" class="visually-hidden">Nombre de usuario</label>
      <input
        id="login-nombre"
        v-model="user.nombre"
        type="text"
        name="nombre"
        autocomplete="username"
        placeholder="Nombre de usuario"
        class="form-control form-control-dark"
        required
      />
    </div>

    <div class="mb-3">
      <label for="login-password" class="visually-hidden">Contraseña</label>
      <input
        id="login-password"
        v-model="user.password"
        type="password"
        name="password"
        autocomplete="current-password"
        placeholder="Contraseña"
        class="form-control form-control-dark"
        required
      />
    </div>

    <button type="submit" class="btn btn-login w-100">Iniciar sesión</button>
  </form>
</template>
<style scoped>
.form-control-dark {
  height: 52px;
  padding: 0 16px;
  font-size: 15px;
  color: #fff;
  background-color: #202124;
  border: 1px solid transparent;
  border-radius: 5px;
  box-shadow: none;
}

.form-control-dark::placeholder {
  color: #727272;
}

.form-control-dark:hover,
.form-control-dark:focus {
  color: #fff;
  background-color: #2a2b2e;
  border-color: var(--verde);
  box-shadow: none;
}

.btn-login {
  height: 52px;
  background: var(--verde);
  color: #111216;
  font-weight: 600;
  border: none;
  border-radius: 5px;
  transition:
    opacity 0.3s ease,
    transform 0.2s ease;
}

.btn-login:hover {
  opacity: 0.92;
  transform: translateY(-1px);
}

.btn-login:active {
  transform: translateY(0);
}
</style>
