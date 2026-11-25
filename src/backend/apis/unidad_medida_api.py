from fastapi import APIRouter, HTTPException
from ..services.unidad_medida_service import UnidadMedidaService
from ..schemas.unidad_medida import UnidadMedidaEntrada

rutaUnidadMedida = APIRouter(prefix='/unidad-medida', tags={'Unidades de medida'})
unidadServicio = UnidadMedidaService()

@rutaUnidadMedida.post('/')
def guardarUnidad(unidadNueva: UnidadMedidaEntrada):
    return unidadServicio.guardarUnidad(unidadNueva)

@rutaUnidadMedida.get('/')
def mostrarUnidades():
    return unidadServicio.mostrarUnidades()

@rutaUnidadMedida.get('/{id}')
def buscarUnidad(id: int):
    unidadEncontrada = unidadServicio.buscarUnidad(id)
    if unidadEncontrada is None:
        raise HTTPException(status_code=404, detail=f'Unidad de medida {id} no encontrada')
    return unidadEncontrada

@rutaUnidadMedida.put('/{id}')
def actualizarUnidad(id: int, unidad: UnidadMedidaEntrada):
    unidadActualizada = unidadServicio.actualizarUnidad(id, unidad)
    if unidadActualizada is None:
        raise HTTPException(status_code=404, detail=f'Unidad de medida {id} no encontrada')
    return unidadActualizada

@rutaUnidadMedida.delete('/{id}')
def eliminarUnidad(id: int):
    idEliminado = unidadServicio.eliminarUnidad(id)
    if idEliminado is None:
        raise HTTPException(status_code=404, detail=f'Unidad de medida {id} no encontrada')
    return {'id': idEliminado, 'mensaje': f'Unidad de medida {idEliminado} eliminada'}
