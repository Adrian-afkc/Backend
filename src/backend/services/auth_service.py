from datetime import UTC, datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from ..config.settings import obtenerConfiguracionJwt
from ..db.connection import consultarUno
from ..schemas.auth import TokenSalida, UsuarioSalida

hasher = PasswordHasher()


class AuthService:
    def __init__(self):
        self.configJwt = obtenerConfiguracionJwt()

    def __obtenerIniciales(self, nombre: str) -> str:
        partes = [parte for parte in nombre.strip().split() if parte]
        if not partes:
            return 'US'
        return ''.join(parte[0].upper() for parte in partes[:2])

    def __mapearUsuario(self, fila: dict) -> UsuarioSalida:
        nombre = fila.get('Nombre') or fila['Usuario']
        return UsuarioSalida(
            id=fila['Id'],
            usuario=fila['Usuario'],
            nombre=nombre,
            rol=fila.get('Rol') or 'Usuario',
            iniciales=self.__obtenerIniciales(nombre),
        )

    def __crearToken(self, usuario: UsuarioSalida) -> TokenSalida:
        ahora = datetime.now(UTC)
        minutosExpiracion = self.configJwt['minutosExpiracion']
        expira = ahora + timedelta(minutes=minutosExpiracion)

        payload = {
            'sub': str(usuario.id),
            'usuario': usuario.usuario,
            'nombre': usuario.nombre,
            'rol': usuario.rol,
            'iat': int(ahora.timestamp()),
            'exp': int(expira.timestamp()),
        }

        token = jwt.encode(
            payload,
            self.configJwt['secreto'],
            algorithm=self.configJwt['algoritmo'],
        )

        return TokenSalida(
            tokenAcceso=token,
            expiraEn=minutosExpiracion * 60,
            usuario=usuario,
        )

    def iniciarSesion(self, usuario: str, contrasena: str):
        fila = consultarUno(
            '''
            SELECT Id, Usuario, Contrasena, Nombre, Rol
            FROM dbo.Usuarios
            WHERE Usuario = ?
            ''',
            (usuario,),
        )

        hashGuardado = fila['Contrasena'] if fila else hasher.hash('credencial-invalida')

        try:
            contrasenaValida = hasher.verify(hashGuardado, contrasena)
        except (VerifyMismatchError, InvalidHashError):
            contrasenaValida = False

        if not fila or not contrasenaValida:
            return None

        usuarioSalida = self.__mapearUsuario(fila)
        return self.__crearToken(usuarioSalida)

    def decodificarToken(self, token: str):
        try:
            return jwt.decode(
                token,
                self.configJwt['secreto'],
                algorithms=[self.configJwt['algoritmo']],
            )
        except jwt.PyJWTError:
            return None

    def obtenerUsuarioActual(self, token: str):
        payload = self.decodificarToken(token)
        if not payload:
            return None

        idUsuario = payload.get('sub')
        if not idUsuario:
            return None

        fila = consultarUno(
            '''
            SELECT Id, Usuario, Contrasena, Nombre, Rol
            FROM dbo.Usuarios
            WHERE Id = ?
            ''',
            (int(idUsuario),),
        )
        return self.__mapearUsuario(fila) if fila else None
