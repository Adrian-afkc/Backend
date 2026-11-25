from fastapi import APIRouter, HTTPException
from ..services.insumo_service import InsumoService
from ..schemas.insumo import InsumoEntrada

rutaInsumo = APIRouter(prefix='/insumo', tags={'Insumos'})
insumoServicio = InsumoService()

@rutaInsumo.post('/')
def guardarInsumo(insumoNuevo: InsumoEntrada):
    return insumoServicio.guardarInsumo(insumoNuevo)

@rutaInsumo.get('/')
def mostrarInsumos():
    return insumoServicio.mostrarInsumos()

@rutaInsumo.get('/{id}')
def buscarInsumo(id: int):
    insumoEncontrado = insumoServicio.buscarInsumo(id)
    if insumoEncontrado is None:
        raise HTTPException(status_code=404, detail=f'Insumo {id} no encontrado')
    return insumoEncontrado

@rutaInsumo.put('/{id}')
def actualizarInsumo(id: int, insumo: InsumoEntrada):
    insumoActualizado = insumoServicio.actualizarInsumo(id, insumo)
    if insumoActualizado is None:
        raise HTTPException(status_code=404, detail=f'Insumo {id} no encontrado')
    return insumoActualizado

@rutaInsumo.delete('/{id}')
def eliminarInsumo(id: int):
    idEliminado = insumoServicio.eliminarInsumo(id)
    if idEliminado is None:
        raise HTTPException(status_code=404, detail=f'Insumo {id} no encontrado')
    return {'id': idEliminado, 'mensaje': f'Insumo {idEliminado} eliminado'}
