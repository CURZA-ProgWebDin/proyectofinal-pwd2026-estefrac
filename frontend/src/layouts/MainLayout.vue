<script setup>
import TopBar from '../components/layout/TopBar.vue'
import SidebarNav from '../components/layout/SidebarNav.vue'
import FooterBar from '../components/layout/FooterBar.vue'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const isSidebarOpen = ref(window.matchMedia('(min-width: 992px)').matches)

const route = useRoute()
</script>

<template>
  <div class="main-layout d-flex flex-column min-vh-100" :class="{ 'sidebar-open': isSidebarOpen }">
    <TopBar :is-sidebar-open="isSidebarOpen" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />

    <div class="layout-body d-flex flex-grow-1">
      <aside class="sidebar" :inert="!isSidebarOpen">
        <SidebarNav />
      </aside>

      <div class="content-column d-flex flex-column flex-grow-1">
        <main class="page-content flex-grow-1 p-4">
          <header class="page-header mb-2">
            <h1 class="page-titulo mb-0">{{ route.meta.titulo }}</h1>
          </header>

          <RouterView />
        </main>
      </div>
    </div>

    <FooterBar />
  </div>
</template>

<style scoped>
.sidebar {
  flex-basis: 225px;
  flex-shrink: 0;
  background-color: var(--app-bg);
  border-right: 1px solid var(--borde);
  margin-left: -225px;
  transition:
    margin-left 250ms ease-in-out,
    transform 250ms ease-in-out;
  position: sticky;
  top: 56px;
  align-self: flex-start;
  height: calc(100vh - 56px);
  overflow-y: auto;
}

.sidebar-open .sidebar {
  margin-left: 0;
  transform: translateX(0);
}

.main-layout {
  padding-top: 56px;
  background-color: var(--app-bg);
  color: #f1f3f5;
}

.layout-body {
  position: relative;
}

.content-column {
  min-width: 0;
}

.page-titulo {
  font-size: 2.25rem;
  font-weight: 600;
}

@media (max-width: 991.98px) {
  .sidebar {
    position: fixed;
    top: 56px;
    bottom: 0;
    left: 0;
    width: 225px;
    margin-left: 0;
    transform: translateX(-100%);
    overflow-y: auto;
    z-index: 2;
  }

  .layout-body::before {
    content: '';
    position: absolute;
    inset: 0;
    background-color: rgb(0 0 0 / 50%);
    opacity: 0;
    pointer-events: none;
    z-index: 1;
    transition: opacity 250ms ease-in-out;
  }

  .sidebar-open .layout-body::before {
    opacity: 1;
    pointer-events: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .sidebar,
  .layout-body::before {
    transition: none;
  }
}
</style>
