from typing import List

from azure.storage.blob import BlobServiceClient

# External
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

# Project
from app.core import LOGGER
from app.core.database import get_session
from app.models.necropsia import (
    NecropsiaAnalisis,
    NecropsiaCaracteristica,
    NecropsiaDiagnostico,
)
from app.schemas.necropsia_diagnostico import DiagnosticoCreate, DiagnosticoRead

router = APIRouter(
    prefix="/diagnostics",
    tags=["diagnostics"],
)


@router.post("/", response_model=DiagnosticoRead)
async def create_diagnostico(
    body: DiagnosticoCreate,
    session: Session = Depends(get_session),
) -> DiagnosticoRead:

    try:
        new_necropsia_diagnostico = NecropsiaDiagnostico(
            **{
                **body.model_dump(),
                "id_necropsia_caso": body.id_necropsia_caso,
                "id_tipo_mortalidad": body.id_tipo_mortalidad,
                "certeza": body.certeza,
                "comentario": body.comentario,
                "veterinario": body.veterinario,
            }
        )
        session.add(new_necropsia_diagnostico)
        session.commit()
        session.refresh(new_necropsia_diagnostico)

        return new_necropsia_diagnostico

    except IntegrityError as e:
        session.rollback()
        LOGGER.error(f"IntegrityError: {e}")
        detail_msg = "There was a problem with the data provided. Check the microservice logs for more details"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg
        ) from e


@router.get("/{id_diagnostic}", response_model=DiagnosticoRead)
def get_dianostico_detail(id_diagnostic: int, db: Session = Depends(get_session)):

    try:
        statement = select(
            NecropsiaDiagnostico.id_necropsia_diagnostico,
            NecropsiaDiagnostico.id_necropsia_caso,
            NecropsiaDiagnostico.id_tipo_mortalidad,
            NecropsiaDiagnostico.certeza,
            NecropsiaDiagnostico.comentario,
            NecropsiaDiagnostico.veterinario,
        ).where(NecropsiaDiagnostico.id_necropsia_diagnostico == id_diagnostic)

        result = db.exec(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="diagnostic ID not found")

        return result

    except IntegrityError as e:
        LOGGER.error("Error when trying to get diagnostic details:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when trying to get diagnostic Detail",
        )
