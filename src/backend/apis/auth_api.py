from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..schemas.auth import CredencialesEntrada, TokenSalida, UsuarioSalida
from ..services.auth_service import AuthService

rutaAuth = APIRouter(prefix='/auth', tags={'Autenticación'})
authServicio = AuthService()
seguridad = HTTPBearer(auto_error=False)


def requiereAutenticacion(
    credenciales: HTTPAuthorizationCredentials | None = Depends(seguridad),
) -> UsuarioSalida:
    if credenciales is None or credenciales.scheme.lower() != 'bearer':
        raise HTTPException(status_code=401, detail='Debes iniciar sesión para continuar')

    usuario = authServicio.obtenerUsuarioActual(credenciales.credentials)
    if usuario is None:
        raise HTTPException(status_code=401, detail='La sesión no es válida o expiró')

    return usuario


@rutaAuth.post('/login')
def iniciarSesion(credenciales: CredencialesEntrada) -> TokenSalida:
    token = authServicio.iniciarSesion(credenciales.usuario, credenciales.contrasena)
    if token is None:
        raise HTTPException(status_code=401, detail='Usuario o contraseña incorrectos')
    return token


@rutaAuth.get('/me')
def obtenerUsuarioActual(usuario: UsuarioSalida = Depends(requiereAutenticacion)) -> UsuarioSalida:
    return usuario
