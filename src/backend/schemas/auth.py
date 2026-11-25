from pydantic import BaseModel


class CredencialesEntrada(BaseModel):
    usuario: str
    contrasena: str


class UsuarioSalida(BaseModel):
    id: int
    usuario: str
    nombre: str
    rol: str
    iniciales: str


class TokenSalida(BaseModel):
    tokenAcceso: str
    tipoToken: str = 'bearer'
    expiraEn: int
    usuario: UsuarioSalida
