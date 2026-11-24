from fastapi import APIRouter
from ..services.insumo_service import InsumoService
from ..schemas.insumo import Insumo

rutaInsumo = APIRouter(prefix='/insumo', tags={'Insumos'})
insumoServicio = InsumoService()

@rutaInsumo.post('/')
def guardarInsumo(insumoNuevo: Insumo):
    return insumoServicio.guardarInsumo(insumoNuevo)

@rutaInsumo.get('/')
def mostrarInsumos():
    return insumoServicio.mostrarInsumos()

@rutaInsumo.put('/{id}')
def actualizarInsumo(id: int, insumo: Insumo):
    return insumoServicio.actualizarInsumo(id, insumo)

@rutaInsumo.delete('/{id}')
def eliminarInsumo(id: int):
    return insumoServicio.eliminarInsumo(id)