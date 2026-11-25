from fastapi import APIRouter, HTTPException
from ..services.categoria_service import CategoriaService
from ..schemas.categoria import CategoriaEntrada

rutaCategoria = APIRouter(prefix='/categoria', tags={'Categorías'})
categoriaServicio = CategoriaService()

@rutaCategoria.post('/')
def guardarCategoria(categoriaNueva: CategoriaEntrada):
    return categoriaServicio.guardarCategoria(categoriaNueva)

@rutaCategoria.get('/')
def mostrarCategorias():
    return categoriaServicio.mostrarCategorias()

@rutaCategoria.get('/{id}')
def buscarCategoria(id: int):
    categoriaEncontrada = categoriaServicio.buscarCategoria(id)
    if categoriaEncontrada is None:
        raise HTTPException(status_code=404, detail=f'Categoría {id} no encontrada')
    return categoriaEncontrada

@rutaCategoria.put('/{id}')
def actualizarCategoria(id: int, categoria: CategoriaEntrada):
    categoriaActualizada = categoriaServicio.actualizarCategoria(id, categoria)
    if categoriaActualizada is None:
        raise HTTPException(status_code=404, detail=f'Categoría {id} no encontrada')
    return categoriaActualizada

@rutaCategoria.delete('/{id}')
def eliminarCategoria(id: int):
    idEliminado = categoriaServicio.eliminarCategoria(id)
    if idEliminado is None:
        raise HTTPException(status_code=404, detail=f'Categoría {id} no encontrada')
    return {'id': idEliminado, 'mensaje': f'Categoría {idEliminado} eliminada'}
