# Standard Library
import json
import sys
from collections import defaultdict
from typing import List

# External
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

# Project
from app.core import LOGGER
from app.core.database import get_session
from app.models.centers import Cage, Center, Module, UserCenter
from app.schemas.centers import CenterCageRead, CenterRead

router = APIRouter(
    prefix="/centers",
    tags=["centers"],
)


@router.get("/", response_model=list[CenterCageRead])
def get_centers(id_user: int, db: Session = Depends(get_session)):

    if id_user is None:
        raise HTTPException(status_code=404, detail="id_user not found")

    try:

        statement = (
            select(
                Center.id_centro,
                Center.nombre,
                Module.id_modulo,
                Module.nombre,
                Cage.id_jaula,
                Cage.nombre,
                Cage.numero,
            )
            .join(UserCenter, UserCenter.id_centro == Center.id_centro)
            .join(Module, Module.id_centro == Center.id_centro, isouter=True)
            .join(Cage, Cage.id_modulo == Module.id_modulo, isouter=True)
            .where(UserCenter.id_usuario == id_user)
            .order_by(Center.id_centro, Module.id_modulo, Cage.id_jaula)
        )

        results = db.exec(statement).all()
        centros = defaultdict(lambda: {"nombre": "", "jaulas": []})

        for row in results:
            (
                id_centro,
                nombre_centro,
                id_modulo,
                nombre_modulo,
                id_jaula,
                nombre_jaula,
                numero_jaula,
            ) = row
            centros[id_centro]["nombre"] = nombre_centro

            if id_jaula:
                centros[id_centro]["jaulas"].append(
                    {
                        "id_jaula": id_jaula,
                        "nombre": nombre_jaula,
                        "numero": numero_jaula,
                    }
                )

        centros_list = []
        for id_centro, centro_data in centros.items():
            centros_list.append(
                {
                    "id_centro": id_centro,
                    "nombre": centro_data["nombre"],
                    "jaulas": centro_data["jaulas"],
                }
            )

        return centros_list

    except:
        LOGGER.error("Error when trying to get centers")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when trying to get centers",
        )
