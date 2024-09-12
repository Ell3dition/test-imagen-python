# Standard Library
from datetime import datetime

# External
from pydantic import BaseModel, Field


class RecordCreate(BaseModel):
    id_necropsia_caso: int
    fecha: datetime
    foto_tipo: str
    foto_url: str


class CaseCreate(BaseModel):
    numero_caso: str
    id_jaula: int
    fecha: datetime
    observacion: str
    creado_por: int


class RecordRead(BaseModel):
    id_necropsia_registro: int
    fecha: datetime
    foto_tipo: str
    foto_url: str | None = None


class CaseRead(BaseModel):
    id_necropsia_caso: int
    numero_caso: str
    id_jaula: int
    fecha: datetime
    observacion: str
    creado_por: int
    registros: list[RecordRead] | None = None
