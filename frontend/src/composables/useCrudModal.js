import { ref } from 'vue'
import { toast } from 'vue3-toastify'

export function useCrudModal(store, obtenerRegistroActual, mensajes) {
  const modalAbierto = ref(false)
  const modoModal = ref('crear')
  const registroSeleccionado = ref(null)
  const guardando = ref(false)

  function abrirCrear() {
    store.errors = []
    modoModal.value = 'crear'
    registroSeleccionado.value = null
    modalAbierto.value = true
  }

  async function abrirEditar(registro) {
    store.errors = []
    await store.obtener(registro.id)

    if (store.errors.length) {
      toast.error(store.errors[0].message)
      return
    }

    modoModal.value = 'editar'
    registroSeleccionado.value = obtenerRegistroActual()
    modalAbierto.value = true
  }

  async function guardar(datos) {
    if (guardando.value) return

    guardando.value = true

    try {
      const ok =
        modoModal.value === 'crear'
          ? await store.crear(datos)
          : await store.modificar(datos, registroSeleccionado.value.id)

      if (ok) {
        toast.success(modoModal.value === 'crear' ? mensajes.crear : mensajes.modificar)
        modalAbierto.value = false
        store.listar()
      }
    } finally {
      guardando.value = false
    }
  }

  return {
    modalAbierto,
    modoModal,
    registroSeleccionado,
    guardando,
    abrirCrear,
    abrirEditar,
    guardar,
  }
}
