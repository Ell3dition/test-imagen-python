# Standard Library
from datetime import date, datetime
from typing import Optional

# External
from pydantic import BaseModel, Field


class CageRead(BaseModel):
    id_jaula: int
    nombre: str
    numero: int


class ModuleRead(BaseModel):
    id_modulo: int
    nombre: str
    estado_operacional: int
    jaulas: Optional[list] = Field(default=[])


class CenterRead(BaseModel):
    id_centro: int
    nombre: str
    SIEP: int
    estado_operacional: int
    modulos: Optional[list] = Field(default=[])


class CenterCageRead(BaseModel):
    id_centro: int
    nombre: str
    jaulas: list[CageRead]
