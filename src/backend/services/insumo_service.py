from ..schemas.insumo import Insumo

class InsumoService:
    def __init__(self):
        self.__listaInsumos: list[Insumo] = []

    def guardarInsumo(self, insumoNuevo: Insumo):
        if insumoNuevo.id is None:
            ids = [insumo.id for insumo in self.__listaInsumos if insumo.id is not None]
            insumoNuevo.id = max(ids, default=0) + 1
        self.__listaInsumos.append(insumoNuevo)
        return insumoNuevo

    def mostrarInsumos(self):
        return self.__listaInsumos

    def actualizarInsumo(self, id: int, insumo: Insumo):
        for _, valor in enumerate(self.__listaInsumos):
            if valor.id == id:
                valor.nombre = insumo.nombre
                valor.categoria = insumo.categoria
                valor.cantidad = insumo.cantidad
                valor.unidadMedida = insumo.unidadMedida
                valor.stockMinimo = insumo.stockMinimo
                return valor
        return None

    def eliminarInsumo(self, id: int):
        for indice, valor in enumerate(self.__listaInsumos):
            if valor.id == id:
                self.__listaInsumos.pop(indice)
                return id
        return None