from ..db.connection import consultar, ejecutar, insertar
from ..errores import ErrorConflicto
from ..schemas.categoria import CategoriaEntrada, CategoriaSalida

CONSULTA_CATEGORIAS = '''
SELECT id_categoria, nombre, descripcion
FROM dbo.Categorias
'''

class CategoriaService:
    def __mapear(self, fila: dict) -> CategoriaSalida:
        return CategoriaSalida(
            id=fila['id_categoria'],
            nombre=fila['nombre'],
            descripcion=fila['descripcion'],
        )

    def buscarCategoria(self, id: int):
        filas = consultar(f'{CONSULTA_CATEGORIAS} WHERE id_categoria = ?', (id,))
        return self.__mapear(filas[0]) if filas else None

    def mostrarCategorias(self):
        filas = consultar(f'{CONSULTA_CATEGORIAS} ORDER BY nombre')
        return [self.__mapear(fila) for fila in filas]

    def guardarCategoria(self, categoriaNueva: CategoriaEntrada):
        idNuevo = insertar(
            '''
            INSERT INTO dbo.Categorias (nombre, descripcion)
            OUTPUT INSERTED.id_categoria
            VALUES (?, ?)
            ''',
            (categoriaNueva.nombre, categoriaNueva.descripcion),
        )
        return self.buscarCategoria(idNuevo)

    def actualizarCategoria(self, id: int, categoria: CategoriaEntrada):
        filasAfectadas = ejecutar(
            '''
            UPDATE dbo.Categorias
            SET nombre = ?, descripcion = ?
            WHERE id_categoria = ?
            ''',
            (categoria.nombre, categoria.descripcion, id),
        )

        if filasAfectadas == 0:
            return None
        return self.buscarCategoria(id)

    def eliminarCategoria(self, id: int):
        try:
            filasAfectadas = ejecutar(
                'DELETE FROM dbo.Categorias WHERE id_categoria = ?',
                (id,),
            )
        except ErrorConflicto:
            raise ErrorConflicto(
                'No se puede eliminar la categoría porque tiene insumos asociados'
            ) from None

        return id if filasAfectadas > 0 else None
