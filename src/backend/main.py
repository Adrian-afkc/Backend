import pyodbc
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .apis.auth_api import rutaAuth
from .apis.categoria_api import rutaCategoria
from .apis.health_api import rutaHealth
from .apis.insumo_api import rutaInsumo
from .apis.unidad_medida_api import rutaUnidadMedida
from .errores import ErrorBaseDatos, ErrorConflicto, ErrorDatoNoValido

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:4200',
        'http://127.0.0.1:4200',
        'http://localhost:4000',
        'http://127.0.0.1:4000',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(ErrorDatoNoValido)
def manejarDatoNoValido(peticion: Request, error: ErrorDatoNoValido):
    return JSONResponse(status_code=400, content={'detail': str(error)})

@app.exception_handler(ErrorConflicto)
def manejarConflicto(peticion: Request, error: ErrorConflicto):
    return JSONResponse(status_code=409, content={'detail': str(error)})

@app.exception_handler(ErrorBaseDatos)
def manejarErrorBaseDatos(peticion: Request, error: ErrorBaseDatos):
    return JSONResponse(
        status_code=503,
        content={'detail': 'No se pudo conectar con la base de datos', 'detalle': str(error)},
    )

@app.exception_handler(pyodbc.Error)
def manejarErrorPyodbc(peticion: Request, error: pyodbc.Error):
    return JSONResponse(
        status_code=503,
        content={'detail': 'Error al comunicarse con la base de datos', 'detalle': str(error)},
    )

app.include_router(rutaAuth, prefix='/api')
app.include_router(rutaInsumo, prefix='/api')
app.include_router(rutaCategoria, prefix='/api')
app.include_router(rutaUnidadMedida, prefix='/api')
app.include_router(rutaHealth, prefix='/api')
