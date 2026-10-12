import { ref } from 'vue'
import { toast } from 'vue3-toastify'
import { useTiposVehiculoStore } from '../stores/tipos_vehiculos'

export function useTiposVehiculoCrud() {
  const tiposStore = useTiposVehiculoStore()

  const modalAbierto = ref(false)
  const modoModal = ref('crear')
  const tipoSeleccionado = ref(null)

  function abrirCrear() {
    tiposStore.errors = []
    modoModal.value = 'crear'
    tipoSeleccionado.value = null
    modalAbierto.value = true
  }

  async function abrirEditar(tipo) {
    tiposStore.errors = []
    await tiposStore.obtener(tipo.id)

    if (tiposStore.errors.length) {
      toast.error(tiposStore.errors[0].message)
      return
    }

    modoModal.value = 'editar'
    tipoSeleccionado.value = tiposStore.tipoVehiculoActual
    modalAbierto.value = true
  }

  async function guardar(datos) {
    const ok =
      modoModal.value === 'crear'
        ? await tiposStore.crear(datos)
        : await tiposStore.modificar(datos, tipoSeleccionado.value.id)

    if (ok) {
      toast.success(
        modoModal.value === 'crear'
          ? 'Tipo de vehículo creado exitosamente'
          : 'Tipo de vehículo actualizado exitosamente',
      )
      modalAbierto.value = false
      tiposStore.listar()
    }
  }

  return {
    modalAbierto,
    modoModal,
    tipoSeleccionado,
    abrirCrear,
    abrirEditar,
    guardar,
  }
}
