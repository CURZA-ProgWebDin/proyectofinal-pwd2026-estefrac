<script setup>
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../../stores/auth'
import LoginForm from './LoginForm.vue'

const authStore = useAuthStore()

const { is_authenticated, errors } = storeToRefs(authStore)

async function handleLogin(credentials) {
  await authStore.login(credentials)

  if (is_authenticated.value) {
    authStore.goPanel()
  }
}
</script>
<template>
  <div class="login-page">
    <div class="background-layer" aria-hidden="true"></div>
    <div class="overlay" aria-hidden="true"></div>

    <main class="main-container d-flex w-100 overflow-hidden rounded-4">
      <section
        class="login-side d-flex flex-column align-items-center justify-content-center position-relative"
      >
        <div class="login-content w-100">
          <h1 class="login-title fw-bold text-white text-center">Iniciar sesión</h1>

          <LoginForm @submit="handleLogin" />

          <ul v-if="errors.length" role="alert">
            <li v-for="(error, index) in errors" :key="index">
              {{ error.message }}
            </li>
          </ul>
        </div>

        <div class="footer-text position-absolute start-0 end-0 text-center">FleetHub · v1.0</div>
      </section>

      <section class="image-side d-none d-md-flex align-items-center justify-content-center">
        <img src="/fleethub-logo.svg" alt="FleetHub" class="logo-white img-fluid" />
      </section>
    </main>
  </div>
</template>
<style scoped>
.login-page {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1rem;
  overflow: hidden;
}

.background-layer {
  position: fixed;
  inset: -100px;
  background: url('/img-login.webp') center / cover no-repeat;
  filter: blur(15px) brightness(0.7);
  z-index: 0;
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(17, 18, 22, 0.6);
  z-index: 1;
}

.main-container {
  position: relative;
  z-index: 2;
  max-width: 900px;
  min-height: 650px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
}
.login-side {
  width: 50%;
  background-color: #151618;
  padding: 48px 20px;
}

.image-side {
  width: 50%;
  background: url('/img-login.webp') center / cover no-repeat;
}
.login-content {
  max-width: 380px;
}

.login-title {
  font-size: 32px;
  margin-bottom: 48px;
}

.logo-white {
  max-width: 300px;
  max-height: 300px;
  filter: brightness(0) invert(1) drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
}

.footer-text {
  bottom: 24px;
  color: #727272;
  font-size: 13px;
  letter-spacing: 1px;
}

@media (max-width: 767.98px) {
  .main-container {
    min-height: 600px;
  }

  .login-side {
    width: 100%;
  }
}
</style>
