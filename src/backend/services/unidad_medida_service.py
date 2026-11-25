from ..db.connection import consultar, ejecutar, insertar
from ..errores import ErrorConflicto
from ..schemas.unidad_medida import UnidadMedidaEntrada, UnidadMedidaSalida

CONSULTA_UNIDADES = '''
SELECT id_unidad, nombre, abreviatura
FROM dbo.UnidadesMedida
'''

class UnidadMedidaService:
    def __mapear(self, fila: dict) -> UnidadMedidaSalida:
        return UnidadMedidaSalida(
            id=fila['id_unidad'],
            nombre=fila['nombre'],
            abreviatura=fila['abreviatura'],
        )

    def buscarUnidad(self, id: int):
        filas = consultar(f'{CONSULTA_UNIDADES} WHERE id_unidad = ?', (id,))
        return self.__mapear(filas[0]) if filas else None

    def mostrarUnidades(self):
        filas = consultar(f'{CONSULTA_UNIDADES} ORDER BY nombre')
        return [self.__mapear(fila) for fila in filas]

    def guardarUnidad(self, unidadNueva: UnidadMedidaEntrada):
        idNuevo = insertar(
            '''
            INSERT INTO dbo.UnidadesMedida (nombre, abreviatura)
            OUTPUT INSERTED.id_unidad
            VALUES (?, ?)
            ''',
            (unidadNueva.nombre, unidadNueva.abreviatura),
        )
        return self.buscarUnidad(idNuevo)

    def actualizarUnidad(self, id: int, unidad: UnidadMedidaEntrada):
        filasAfectadas = ejecutar(
            '''
            UPDATE dbo.UnidadesMedida
            SET nombre = ?, abreviatura = ?
            WHERE id_unidad = ?
            ''',
            (unidad.nombre, unidad.abreviatura, id),
        )

        if filasAfectadas == 0:
            return None
        return self.buscarUnidad(id)

    def eliminarUnidad(self, id: int):
        try:
            filasAfectadas = ejecutar(
                'DELETE FROM dbo.UnidadesMedida WHERE id_unidad = ?',
                (id,),
            )
        except ErrorConflicto:
            raise ErrorConflicto(
                'No se puede eliminar la unidad de medida porque tiene insumos asociados'
            ) from None

        return id if filasAfectadas > 0 else None
