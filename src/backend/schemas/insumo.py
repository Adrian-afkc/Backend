from pydantic import BaseModel

class Insumo(BaseModel):
    id: int | None = None
    nombre: str
    categoria: str
    cantidad: float
    unidadMedida: str
    stockMinimo: float