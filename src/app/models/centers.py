from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class UserCenter(SQLModel, table=True):
    __tablename__ = "usuarios_centros"
    id_usuario_centro: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(nullable=False)
    id_centro: int = Field(nullable=False)


class Center(SQLModel, table=True):
    __tablename__ = "centros"
    id_centro: int = Field(primary_key=True, nullable=False)
    nombre: str = Field(nullable=False)
    SIEP: int = Field(nullable=False)
    estado_operacional: int = Field(nullable=False)


class Module(SQLModel, table=True):
    __tablename__ = "modulos"
    id_modulo: int = Field(primary_key=True, nullable=False)
    id_centro: int = Field(foreign_key="centros.id_centro")
    nombre: str = Field(nullable=False)
    estado_operacional: int = Field(default=0, nullable=False)


class Cage(SQLModel, table=True):
    __tablename__ = "jaulas"
    id_jaula: int = Field(primary_key=True, nullable=False)
    id_modulo: int = Field(foreign_key="modulos.id_modulo")
    nombre: str = Field(nullable=False)
    numero: int = None
    estado_operacional: int = Field(default=1, nullable=False)
