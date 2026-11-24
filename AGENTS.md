# AGENTS.md

FastAPI backend for ProyectoEF. The Angular frontend lives in the sibling directory `../Frontend`.

## Setup and run

- Python **3.15** is pinned (`.python-version`, `requires-python >=3.15`). Use `uv` from this directory; do not use bare `python`/`pip` or install a different interpreter.
- Install dependencies: `uv sync`
- Dev server: `uv run uvicorn backend.main:app --reload` (port 8000 by default)
- Smoke check: `curl http://127.0.0.1:8000/api/insumo/` (note the trailing slash)
- Do **not** run `uv run backend` expecting a server: that script only prints a greeting (`src/backend/__init__.py`).

## Layout and conventions

- `src/backend/main.py` owns the `FastAPI` app and is the only place routers are registered: `app.include_router(rutaInsumo, prefix='/api')`. Router prefixes live in the API modules (`/insumo`), so routes end up as `/api/insumo/`.
- Layering: `apis/` = routers and endpoint wiring, `services/` = business logic, `schemas/` = Pydantic models. For a new resource, mirror the insumo trio (`insumo_api.py` with `rutaInsumo`, `InsumoService`, model in `schemas/`) and register the router in `main.py`.
- The codebase uses Spanish domain names and camelCase for functions, variables, and schema fields (`guardarInsumo`, `unidadMedida`, `stockMinimo`, `__listaInsumos`). Follow the local style instead of PEP 8 renaming.
- Endpoints are plain sync `def` and return Pydantic models directly; there are no `response_model`s or explicit status codes.

## Current limitations (don't assume otherwise)

- `InsumoService` is a module-level singleton holding an in-memory `list`. Data is lost on restart/reload and is not shared across uvicorn workers; there is no database or persistence layer.
- `Insumo.id` is required in POST bodies. The service never generates ids, so callers must supply them.
- Update/delete return `None` with HTTP 200 when the id does not exist.
- No CORS middleware is configured; browser calls from the Angular frontend will be blocked until it is added.
- There is no test suite, linter, formatter, or CI config. If you add tests, add pytest as a dev dependency group via `uv add --dev pytest` and document the single-test command here.
