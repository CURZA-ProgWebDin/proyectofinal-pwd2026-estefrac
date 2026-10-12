import '@fontsource-variable/geist'
import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/main.css'
import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(Vue3Toastify, {
  autoClose: 5000,
  theme: 'light',
  position: 'bottom-right',
})
app.use(router)

app.mount('#app')
