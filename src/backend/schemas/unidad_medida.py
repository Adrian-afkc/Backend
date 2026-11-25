from pydantic import BaseModel

class UnidadMedidaEntrada(BaseModel):
    nombre: str
    abreviatura: str

class UnidadMedidaSalida(BaseModel):
    id: int
    nombre: str
    abreviatura: str
