from datetime import datetime

from pydantic import BaseModel

class InsumoEntrada(BaseModel):
    nombre: str
    cantidad: float
    stockMinimo: float
    idCategoria: int
    idUnidad: int

class InsumoSalida(BaseModel):
    id: int
    nombre: str
    cantidad: float
    stockMinimo: float
    idCategoria: int
    idUnidad: int
    categoria: str
    unidadMedida: str
    fechaRegistro: datetime | None = None
