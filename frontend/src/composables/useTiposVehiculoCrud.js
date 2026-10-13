import { ref } from 'vue'
import { toast } from 'vue3-toastify'
import { useTiposVehiculoStore } from '../stores/tipos_vehiculos'

export function useTiposVehiculoCrud() {
  const tiposVehiculoStore = useTiposVehiculoStore()

  const modalAbierto = ref(false)
  const modoModal = ref('crear')
  const tipoSeleccionado = ref(null)

  function abrirCrear() {
    tiposVehiculoStore.errors = []
    modoModal.value = 'crear'
    tipoSeleccionado.value = null
    modalAbierto.value = true
  }

  async function abrirEditar(tipo) {
    tiposVehiculoStore.errors = []
    await tiposVehiculoStore.obtener(tipo.id)

    if (tiposVehiculoStore.errors.length) {
      toast.error(tiposVehiculoStore.errors[0].message)
      return
    }

    modoModal.value = 'editar'
    tipoSeleccionado.value = tiposVehiculoStore.tipoVehiculoActual
    modalAbierto.value = true
  }

  async function guardar(datos) {
    const ok =
      modoModal.value === 'crear'
        ? await tiposVehiculoStore.crear(datos)
        : await tiposVehiculoStore.modificar(datos, tipoSeleccionado.value.id)

    if (ok) {
      toast.success(
        modoModal.value === 'crear'
          ? 'Tipo de vehículo creado exitosamente'
          : 'Tipo de vehículo actualizado exitosamente',
      )
      modalAbierto.value = false
      tiposVehiculoStore.listar()
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
