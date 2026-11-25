from fastapi import APIRouter
from ..config.settings import obtenerConfiguracionBaseDatos
from ..db.connection import consultarUno

rutaHealth = APIRouter(prefix='/health', tags={'Salud'})

@rutaHealth.get('/db')
def verificarBaseDatos():
    config = obtenerConfiguracionBaseDatos()
    fila = consultarUno('SELECT DB_NAME() AS base_datos, @@VERSION AS version')

    if fila is None:
        return {'estado': 'sin respuesta', 'baseDatos': config['baseDatos']}

    version = (fila['version'] or '').strip().splitlines()[0] if fila['version'] else ''

    return {
        'estado': 'ok',
        'servidor': config['servidor'],
        'driver': config['driver'],
        'baseDatos': fila['base_datos'],
        'autenticacionWindows': config['autenticacionWindows'],
        'version': version,
    }
