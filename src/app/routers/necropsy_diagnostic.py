from typing import List

from azure.storage.blob import BlobServiceClient

# External
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

# Project
from app.core import LOGGER
from app.core.database import get_session
from app.models.necropsy import NecropsyDiagnostic
from app.schemas.necropsy_diagnostic import DiagnosticCreate, DiagnosticRead

router = APIRouter(
    prefix="/diagnostics",
    tags=["diagnostics"],
)


@router.post("/", response_model=DiagnosticRead)
async def diagnostic_create(
    diagnostic: DiagnosticCreate,
    session: Session = Depends(get_session),
) -> DiagnosticRead:

    try:
        new_necropsy_diagnostic = NecropsyDiagnostic(**{**diagnostic.model_dump()})
        session.add(new_necropsy_diagnostic)
        session.commit()
        session.refresh(new_necropsy_diagnostic)

        return new_necropsy_diagnostic

    except IntegrityError as e:
        session.rollback()
        LOGGER.error(f"IntegrityError: {e}")
        detail_msg = "There was a problem with the data provided. Check the microservice logs for more details"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg
        ) from e


@router.get("/{id_diagnostic}", response_model=DiagnosticRead)
def get_detail_diagnostic(id_diagnostic: int, db: Session = Depends(get_session)):

    try:
        statement = select(
            NecropsyDiagnostic.id_necropsia_diagnostico,
            NecropsyDiagnostic.id_necropsia_caso,
            NecropsyDiagnostic.id_tipo_mortalidad,
            NecropsyDiagnostic.certeza,
            NecropsyDiagnostic.comentario,
            NecropsyDiagnostic.veterinario,
        ).where(NecropsyDiagnostic.id_necropsia_diagnostico == id_diagnostic)

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
