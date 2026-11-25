from ..db.connection import consultar, consultarUno, ejecutar, insertar
from ..errores import ErrorDatoNoValido
from ..schemas.insumo import InsumoEntrada, InsumoSalida

CONSULTA_INSUMOS = '''
SELECT i.id_insumo,
       i.nombre,
       i.cantidad,
       i.stock_minimo,
       i.id_categoria,
       i.id_unidad,
       c.nombre AS categoria,
       u.nombre AS unidad_medida,
       i.fecha_registro
FROM dbo.Insumos AS i
INNER JOIN dbo.Categorias AS c ON c.id_categoria = i.id_categoria
INNER JOIN dbo.UnidadesMedida AS u ON u.id_unidad = i.id_unidad
'''

class InsumoService:
    def __mapear(self, fila: dict) -> InsumoSalida:
        return InsumoSalida(
            id=fila['id_insumo'],
            nombre=fila['nombre'],
            cantidad=float(fila['cantidad']),
            stockMinimo=float(fila['stock_minimo']),
            idCategoria=fila['id_categoria'],
            idUnidad=fila['id_unidad'],
            categoria=fila['categoria'],
            unidadMedida=fila['unidad_medida'],
            fechaRegistro=fila['fecha_registro'],
        )

    def __validarReferencias(self, idCategoria: int, idUnidad: int):
        if consultarUno(
            'SELECT 1 AS existe FROM dbo.Categorias WHERE id_categoria = ?',
            (idCategoria,),
        ) is None:
            raise ErrorDatoNoValido(f'La categoría {idCategoria} no existe')

        if consultarUno(
            'SELECT 1 AS existe FROM dbo.UnidadesMedida WHERE id_unidad = ?',
            (idUnidad,),
        ) is None:
            raise ErrorDatoNoValido(f'La unidad de medida {idUnidad} no existe')

    def buscarInsumo(self, id: int):
        filas = consultar(f'{CONSULTA_INSUMOS} WHERE i.id_insumo = ?', (id,))
        return self.__mapear(filas[0]) if filas else None

    def mostrarInsumos(self):
        filas = consultar(f'{CONSULTA_INSUMOS} ORDER BY i.nombre')
        return [self.__mapear(fila) for fila in filas]

    def guardarInsumo(self, insumoNuevo: InsumoEntrada):
        self.__validarReferencias(insumoNuevo.idCategoria, insumoNuevo.idUnidad)

        idNuevo = insertar(
            '''
            INSERT INTO dbo.Insumos
                (nombre, cantidad, stock_minimo, id_categoria, id_unidad, fecha_registro)
            OUTPUT INSERTED.id_insumo
            VALUES (?, ?, ?, ?, ?, GETDATE())
            ''',
            (
                insumoNuevo.nombre,
                insumoNuevo.cantidad,
                insumoNuevo.stockMinimo,
                insumoNuevo.idCategoria,
                insumoNuevo.idUnidad,
            ),
        )
        return self.buscarInsumo(idNuevo)

    def actualizarInsumo(self, id: int, insumo: InsumoEntrada):
        self.__validarReferencias(insumo.idCategoria, insumo.idUnidad)

        filasAfectadas = ejecutar(
            '''
            UPDATE dbo.Insumos
            SET nombre = ?,
                cantidad = ?,
                stock_minimo = ?,
                id_categoria = ?,
                id_unidad = ?
            WHERE id_insumo = ?
            ''',
            (
                insumo.nombre,
                insumo.cantidad,
                insumo.stockMinimo,
                insumo.idCategoria,
                insumo.idUnidad,
                id,
            ),
        )

        if filasAfectadas == 0:
            return None
        return self.buscarInsumo(id)

    def eliminarInsumo(self, id: int):
        filasAfectadas = ejecutar('DELETE FROM dbo.Insumos WHERE id_insumo = ?', (id,))
        return id if filasAfectadas > 0 else None
