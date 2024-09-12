from datetime import datetime

from sqlmodel import Field, SQLModel


class NecropsyCase(SQLModel, table=True):
    __tablename__ = "necropsia_casos"
    id_necropsia_caso: int = Field(primary_key=True, nullable=False)
    numero_caso: str = Field(nullable=False)
    id_jaula: int = Field(foreign_key="jaulas.id_jaula")
    fecha: datetime = Field(nullable=False)
    observacion: str = None
    creado_por: int = None


class NecropsyRecord(SQLModel, table=True):
    __tablename__ = "necropsia_registros"
    id_necropsia_registro: int = Field(primary_key=True, nullable=False)
    id_necropsia_caso: int = Field(foreign_key="necropsia_casos.id_necropsia_caso")
    fecha: datetime = Field(nullable=False)
    foto_tipo: str = None
    foto_url: str = Field(nullable=True)


class NecropsyCharacteristic(SQLModel, table=True):
    __tablename__ = "necropsia_caracteristicas"
    id_necropsia_caracteristica: int = Field(primary_key=True, nullable=False)
    organo: str = Field(nullable=False)
    caracteristica: str = Field(nullable=False)
    detalle: str = Field(nullable=False)


class NecropsyAnalisys(SQLModel, table=True):
    __tablename__ = "necropsia_analisis"
    id_necropsia_analisis: int = Field(primary_key=True, nullable=False)
    id_necropsia_registro: int = Field(
        foreign_key="necropsia_registros.id_necropsia_registro"
    )
    id_necropsia_caracteristica: int = Field(
        foreign_key="necropsia_caracteristicas.id_necropsia_caracteristica"
    )
    pos_x: int | None = None
    pos_y: int | None = None
    comentario: str | None = None


class NecropsyDiagnostic(SQLModel, table=True):
    __tablename__ = "necropsia_diagnosticos"
    id_necropsia_diagnostico: int = Field(primary_key=True, nullable=False)
    id_necropsia_caso: int = Field(foreign_key="necropsia_casos.id_necropsia_caso")
    id_tipo_mortalidad: int = Field(nullable=False)
    certeza: int | None = None
    comentario: str | None = None
    veterinario: int | None = None
