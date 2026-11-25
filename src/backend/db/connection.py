"""Acceso a SQL Server con pyodbc (sin ORM: SQL parametrizado explícito)."""

from collections.abc import Iterator, Sequence
from contextlib import contextmanager

import pyodbc

from ..config.settings import obtenerCadenaConexion
from ..errores import ErrorBaseDatos, ErrorConflicto

# Códigos nativos de SQL Server que representan conflictos de integridad.
CODIGOS_CONFLICTO = ('547', '2601', '2627')


def _mensajeError(error: pyodbc.Error) -> str:
    return ' '.join(str(argumento) for argumento in error.args)


def _traducirError(error: pyodbc.Error) -> Exception:
    mensaje = _mensajeError(error)
    if any(codigo in mensaje for codigo in CODIGOS_CONFLICTO):
        return ErrorConflicto(mensaje)
    return ErrorBaseDatos(mensaje)


def _ejecutarSentencia(cursor: pyodbc.Cursor, sql: str, parametros: Sequence):
    if parametros:
        return cursor.execute(sql, parametros)
    return cursor.execute(sql)


@contextmanager
def obtenerCursor() -> Iterator[pyodbc.Cursor]:
    """Entrega un cursor y garantiza commit/rollback y cierre de la conexión."""
    try:
        conexion = pyodbc.connect(obtenerCadenaConexion())
    except pyodbc.Error as error:
        raise ErrorBaseDatos(_mensajeError(error)) from error

    cursor = conexion.cursor()
    try:
        yield cursor
        conexion.commit()
    except pyodbc.Error as error:
        conexion.rollback()
        raise _traducirError(error) from error
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def consultar(sql: str, parametros: Sequence = ()) -> list[dict]:
    with obtenerCursor() as cursor:
        _ejecutarSentencia(cursor, sql, parametros)
        if cursor.description is None:
            return []
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


def consultarUno(sql: str, parametros: Sequence = ()) -> dict | None:
    filas = consultar(sql, parametros)
    return filas[0] if filas else None


def ejecutar(sql: str, parametros: Sequence = ()) -> int:
    """Ejecuta INSERT/UPDATE/DELETE y devuelve las filas afectadas."""
    with obtenerCursor() as cursor:
        _ejecutarSentencia(cursor, sql, parametros)
        return cursor.rowcount


def insertar(sql: str, parametros: Sequence = ()) -> int | None:
    """Ejecuta un INSERT con OUTPUT INSERTED.<id> y devuelve el id generado."""
    with obtenerCursor() as cursor:
        _ejecutarSentencia(cursor, sql, parametros)
        fila = cursor.fetchone()
        return fila[0] if fila else None
