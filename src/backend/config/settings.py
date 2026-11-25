"""Configuración leída desde el archivo .env de la raíz del proyecto."""

import os
from pathlib import Path

from dotenv import load_dotenv

RUTA_RAIZ = Path(__file__).resolve().parents[3]

# Carga las variables del .env una sola vez al importar el módulo.
load_dotenv(RUTA_RAIZ / '.env')

DRIVER_POR_DEFECTO = 'ODBC Driver 18 for SQL Server'
SERVIDOR_POR_DEFECTO = 'localhost'
BASE_DATOS_POR_DEFECTO = 'OllaComunSector10'


def _valorBooleano(nombre: str, porDefecto: bool) -> bool:
    valor = os.getenv(nombre)
    if valor is None:
        return porDefecto
    return valor.strip().lower() in {'1', 'si', 'sí', 'true', 'yes', 'y'}


def obtenerConfiguracionBaseDatos() -> dict:
    return {
        'driver': os.getenv('DB_DRIVER', DRIVER_POR_DEFECTO),
        'servidor': os.getenv('DB_SERVER', SERVIDOR_POR_DEFECTO),
        'baseDatos': os.getenv('DB_DATABASE', BASE_DATOS_POR_DEFECTO),
        'autenticacionWindows': _valorBooleano('DB_TRUSTED_CONNECTION', True),
        'usuario': os.getenv('DB_USER'),
        'contrasena': os.getenv('DB_PASSWORD'),
        'encriptar': os.getenv('DB_ENCRYPT', 'yes'),
        'confiarCertificado': os.getenv('DB_TRUST_SERVER_CERTIFICATE', 'yes'),
        'tiempoEspera': os.getenv('DB_TIMEOUT', '15'),
    }


def obtenerConfiguracionJwt() -> dict:
    return {
        'secreto': os.getenv('JWT_SECRETO', 'cambia-esta-clave-en-produccion'),
        'algoritmo': os.getenv('JWT_ALGORITMO', 'HS256'),
        'minutosExpiracion': int(os.getenv('JWT_MINUTOS_EXPIRACION', '120')),
    }


def obtenerCadenaConexion() -> str:
    config = obtenerConfiguracionBaseDatos()

    partes = [
        f"DRIVER={{{config['driver']}}}",
        f"SERVER={config['servidor']}",
        f"DATABASE={config['baseDatos']}",
        f"Encrypt={config['encriptar']}",
        f"TrustServerCertificate={config['confiarCertificado']}",
        f"Connection Timeout={config['tiempoEspera']}",
    ]

    if config['autenticacionWindows']:
        partes.append('Trusted_Connection=yes')
    else:
        partes.append(f"UID={config['usuario'] or ''}")
        partes.append(f"PWD={config['contrasena'] or ''}")

    return ';'.join(partes)
