# Standard Library
from datetime import datetime

# External
from pydantic import BaseModel, Field


class CharacteriticRead(BaseModel):
    id_necropsia_caracteristica: int
    organo: str
    caracteristica: str
    detalle: str


class AnalysisCreate(BaseModel):
    id_necropsia_registro: int
    id_necropsia_caracteristica: int
    pos_x: int | None = None
    pos_y: int | None = None
    comentario: str | None = None


class AnalysisRead(BaseModel):
    id_necropsia_analisis: int
    id_necropsia_registro: int
    id_necropsia_caracteristica: int
    pos_x: int | None = None
    pos_y: int | None = None
    comentario: str | None = None
