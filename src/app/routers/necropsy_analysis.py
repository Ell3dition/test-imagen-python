import json
from typing import List

from azure.storage.blob import BlobServiceClient

# External
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

# Project
from app.core import LOGGER
from app.core.database import get_session
from app.models.necropsy import NecropsyAnalisys, NecropsyCharacteristic
from app.schemas.necropsy_analysis import (
    AnalysisCreate,
    AnalysisRead,
    CharacteriticRead,
)

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)


@router.get("/characteristics", response_model=List[CharacteriticRead])
def get_characteristics(db: Session = Depends(get_session)):

    try:

        statement = select(NecropsyCharacteristic)
        caracteristicas_list = db.exec(statement).all()

        return caracteristicas_list

    except IntegrityError as e:
        LOGGER.error("Error when trying to get characteristics:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when trying to get characteristics",
        )


@router.post("/", response_model=AnalysisRead)
async def analysis_create(
    analysis: AnalysisCreate,
    session: Session = Depends(get_session),
) -> AnalysisRead:

    try:
        new_necropsy_analysis = NecropsyAnalisys(**{**analysis.model_dump()})
        session.add(new_necropsy_analysis)
        session.commit()
        session.refresh(new_necropsy_analysis)

        return new_necropsy_analysis

    except IntegrityError as e:
        session.rollback()
        LOGGER.error(f"IntegrityError: {e}")
        detail_msg = "There was a problem with the data provided. Check the microservice logs for more details"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg
        ) from e


@router.get("/{id_analysis}", response_model=AnalysisRead)
def get_analysis_detail(id_analysis: int, db: Session = Depends(get_session)):

    try:

        statement = select(
            NecropsyAnalisys.id_necropsia_analisis,
            NecropsyAnalisys.id_necropsia_registro,
            NecropsyAnalisys.id_necropsia_caracteristica,
            NecropsyAnalisys.pos_x,
            NecropsyAnalisys.pos_y,
            NecropsyAnalisys.comentario,
        ).where(NecropsyAnalisys.id_necropsia_analisis == id_analysis)

        result = db.exec(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="analysis ID not found")

        return result

    except IntegrityError as e:
        LOGGER.error("Error when trying to get analysis details:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when trying to get analysis Detail",
        )
