"""Errores de dominio que la API traduce a códigos HTTP.

Los controladores de `main.py` convierten cada uno en una respuesta concreta,
de manera que el frontend distinga "no existe" (404), "dato inválido" (400),
"en uso" (409) y "base de datos caída" (503).
"""


class ErrorBaseDatos(Exception):
    """No se pudo conectar o ejecutar una sentencia en SQL Server (HTTP 503)."""


class ErrorConflicto(Exception):
    """La operación choca con una restricción de la base de datos (HTTP 409)."""


class ErrorDatoNoValido(Exception):
    """El cuerpo de la petición referencia datos inexistentes (HTTP 400)."""
