# Standard Library
from datetime import datetime

# External
from pydantic import BaseModel


class DiagnosticCreate(BaseModel):
    id_necropsia_caso: int
    id_tipo_mortalidad: int
    certeza: int | None = None
    comentario: str | None = None
    veterinario: int | None = None


class DiagnosticRead(BaseModel):
    id_necropsia_diagnostico: int
    id_necropsia_caso: int
    id_tipo_mortalidad: int
    certeza: int | None = None
    comentario: str | None = None
    veterinario: int | None = None
