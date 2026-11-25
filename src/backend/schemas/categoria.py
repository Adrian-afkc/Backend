from pydantic import BaseModel

class CategoriaEntrada(BaseModel):
    nombre: str
    descripcion: str | None = None

class CategoriaSalida(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
