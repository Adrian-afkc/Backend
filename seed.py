"""Semilla de datos de demostración para la base OllaComunSector10.

Inserta un ejemplo de cada estado del inventario:
- Frijoles: abastecido.
- Lentejas: crítico con prioridad alta (20 % del mínimo).
- Aceite: crítico con prioridad media (33 % del mínimo).

También crea un usuario demo con contraseña hasheada con Argon2.

Es idempotente: si una fila ya existe por nombre/usuario, no la duplica.

Uso:
    uv run python seed.py
"""

from argon2 import PasswordHasher

from backend.db.connection import consultar, ejecutar, insertar

CATEGORIAS = [
    ('Abarrotes', 'Productos secos y de despensa'),
    ('Menestras', 'Legumbres y granos'),
    ('Verduras', 'Productos frescos'),
    ('Lácteos', 'Productos derivados de la leche'),
]

UNIDADES = [
    ('kg', 'kg'),
    ('unidades', 'unid.'),
]

INSUMOS = [
    ('Frijoles', 12, 5, 'Abarrotes', 'kg'),
    ('Lentejas', 1, 5, 'Menestras', 'kg'),
    ('Aceite', 2, 6, 'Abarrotes', 'unidades'),
]

USUARIOS = [
    ('admin', 'Admin2026', 'Administrador', 'Coordinador de Cocina'),
]


def obtenerIdCategoria(nombre: str) -> int | None:
    filas = consultar('SELECT id_categoria FROM dbo.Categorias WHERE nombre = ?', (nombre,))
    return filas[0]['id_categoria'] if filas else None


def obtenerIdUnidad(nombre: str) -> int | None:
    filas = consultar('SELECT id_unidad FROM dbo.UnidadesMedida WHERE nombre = ?', (nombre,))
    return filas[0]['id_unidad'] if filas else None


def sembrarCategorias():
    for nombre, descripcion in CATEGORIAS:
        if obtenerIdCategoria(nombre) is None:
            insertar(
                '''
                INSERT INTO dbo.Categorias (nombre, descripcion)
                OUTPUT INSERTED.id_categoria
                VALUES (?, ?)
                ''',
                (nombre, descripcion),
            )
            print(f'Categoría creada: {nombre}')
        else:
            print(f'Categoría ya existe: {nombre}')


def sembrarUnidades():
    for nombre, abreviatura in UNIDADES:
        if obtenerIdUnidad(nombre) is None:
            insertar(
                '''
                INSERT INTO dbo.UnidadesMedida (nombre, abreviatura)
                OUTPUT INSERTED.id_unidad
                VALUES (?, ?)
                ''',
                (nombre, abreviatura),
            )
            print(f'Unidad creada: {nombre}')
        else:
            print(f'Unidad ya existe: {nombre}')


def sembrarInsumos():
    for nombre, cantidad, stockMinimo, categoria, unidad in INSUMOS:
        existentes = consultar('SELECT 1 AS existe FROM dbo.Insumos WHERE nombre = ?', (nombre,))
        if existentes:
            print(f'Insumo ya existe: {nombre}')
            continue

        idCategoria = obtenerIdCategoria(categoria)
        idUnidad = obtenerIdUnidad(unidad)
        if idCategoria is None or idUnidad is None:
            raise RuntimeError(f'No se encontraron los catálogos para {nombre}')

        insertar(
            '''
            INSERT INTO dbo.Insumos
                (nombre, cantidad, stock_minimo, id_categoria, id_unidad, fecha_registro)
            OUTPUT INSERTED.id_insumo
            VALUES (?, ?, ?, ?, ?, GETDATE())
            ''',
            (nombre, cantidad, stockMinimo, idCategoria, idUnidad),
        )
        print(f'Insumo creado: {nombre}')


def existeColumna(tabla: str, columna: str) -> bool:
    filas = consultar(
        '''
        SELECT 1 AS existe
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = ? AND COLUMN_NAME = ?
        ''',
        (tabla, columna),
    )
    return bool(filas)


def existeIndice(tabla: str, indice: str) -> bool:
    filas = consultar(
        '''
        SELECT 1 AS existe
        FROM sys.indexes
        WHERE name = ? AND object_id = OBJECT_ID(?)
        ''',
        (indice, f'dbo.{tabla}'),
    )
    return bool(filas)


def asegurarEsquemaUsuarios():
    if not existeColumna('Usuarios', 'Nombre'):
        ejecutar('ALTER TABLE dbo.Usuarios ADD Nombre NVARCHAR(120) NULL')
        print('Columna agregada: Usuarios.Nombre')

    if not existeColumna('Usuarios', 'Rol'):
        ejecutar('ALTER TABLE dbo.Usuarios ADD Rol NVARCHAR(80) NULL')
        print('Columna agregada: Usuarios.Rol')

    if not existeIndice('Usuarios', 'UX_Usuarios_Usuario'):
        ejecutar('CREATE UNIQUE INDEX UX_Usuarios_Usuario ON dbo.Usuarios(Usuario)')
        print('Índice creado: UX_Usuarios_Usuario')


def sembrarUsuarios():
    asegurarEsquemaUsuarios()
    hasher = PasswordHasher()

    for usuario, contrasena, nombre, rol in USUARIOS:
        hashContrasena = hasher.hash(contrasena)
        existentes = consultar('SELECT Id FROM dbo.Usuarios WHERE Usuario = ?', (usuario,))

        if existentes:
            ejecutar(
                '''
                UPDATE dbo.Usuarios
                SET Contrasena = ?, Nombre = ?, Rol = ?
                WHERE Usuario = ?
                ''',
                (hashContrasena, nombre, rol, usuario),
            )
            print(f'Usuario actualizado: {usuario}')
        else:
            insertar(
                '''
                INSERT INTO dbo.Usuarios (Usuario, Contrasena, Nombre, Rol)
                OUTPUT INSERTED.Id
                VALUES (?, ?, ?, ?)
                ''',
                (usuario, hashContrasena, nombre, rol),
            )
            print(f'Usuario creado: {usuario}')


def resumen():
    totalInsumos = consultar('SELECT COUNT(*) AS total FROM dbo.Insumos')[0]['total']
    totalUsuarios = consultar('SELECT COUNT(*) AS total FROM dbo.Usuarios')[0]['total']
    print(f'\nSemilla completada. Insumos: {totalInsumos}. Usuarios: {totalUsuarios}')


if __name__ == '__main__':
    sembrarCategorias()
    sembrarUnidades()
    sembrarInsumos()
    sembrarUsuarios()
    resumen()
