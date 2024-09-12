# Standard Library

from datetime import datetime, timedelta
from typing import List

from azure.storage.blob import BlobServiceClient

# External
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

# Project
from app.core import LOGGER
from app.core.database import get_session
from app.core.storage import upload_image
from app.models.centers import UserCenter
from app.models.necropsy import NecropsyCase, NecropsyRecord
from app.schemas.centers import CenterRead
from app.schemas.necropsy_cases import CaseCreate, CaseRead, RecordCreate, RecordRead

router = APIRouter(
    prefix="/necropsy_cases",
    tags=["necropsy_cases"],
)


@router.get("/", response_model=List[CaseRead])
def get_necropsia_cases(id_user: int, db: Session = Depends(get_session)):

    if id_user is None:
        raise HTTPException(status_code=404, detail="id_user not found")

    fecha_limite = datetime.now() - timedelta(days=7)

    # Crear la consulta SQL
    statement = (
        select(NecropsyCase, NecropsyRecord)
        .join(UserCenter, UserCenter.id_usuario == NecropsyCase.creado_por)
        .join(
            NecropsyRecord,
            NecropsyRecord.id_necropsia_caso == NecropsyCase.id_necropsia_caso,
        )
        .where(UserCenter.id_usuario == id_user, NecropsyCase.fecha >= fecha_limite)
    )

    try:
        results = db.exec(statement).all()

        response_data = []

        for caso, registro in results:
            caso_existente = next(
                (
                    item
                    for item in response_data
                    if item["id_necropsia_caso"] == caso.id_necropsia_caso
                ),
                None,
            )

            if caso_existente:
                caso_existente["registros"].append(
                    {
                        "id_necropsia_registro": registro.id_necropsia_registro,
                        "fecha": registro.fecha,
                        "foto_tipo": registro.foto_tipo,
                        "foto_url": registro.foto_url,
                    }
                )
            else:
                response_data.append(
                    {
                        "id_necropsia_caso": caso.id_necropsia_caso,
                        "numero_caso": caso.numero_caso,
                        "id_jaula": caso.id_jaula,
                        "fecha": caso.fecha,
                        "observacion": caso.observacion,
                        "creado_por": caso.creado_por,
                        "registros": [
                            {
                                "id_necropsia_registro": registro.id_necropsia_registro,
                                "fecha": registro.fecha,
                                "foto_tipo": registro.foto_tipo,
                                "foto_url": registro.foto_url,
                            }
                        ],
                    }
                )

        return response_data

    except:
        LOGGER.error("Error when trying to get cases")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error when trying to get cases",
        )


@router.post("/case_create", response_model=CaseRead)
async def case_create(
    case: CaseCreate,
    session: Session = Depends(get_session),
) -> CaseRead:

    try:
        new_necropsy_case = NecropsyCase(**{**case.model_dump()})
        session.add(new_necropsy_case)
        session.commit()
        session.refresh(new_necropsy_case)
        return new_necropsy_case

    except IntegrityError as e:
        session.rollback()
        LOGGER.error(f"IntegrityError: {e}")
        detail_msg = "There was a problem with the data provided. Check the microservice logs for more details"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg
        ) from e


@router.post("/record_create", response_model=RecordRead)
async def record_create(
    case: int,
    record_date: datetime,
    image_type: str,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> RecordRead:

    contents = await file.read()
    image_url = upload_image(contents, file.filename)

    try:
        new_record = NecropsyRecord(
            id_necropsia_caso=case,
            fecha=record_date,
            foto_tipo=image_type,
            foto_url=image_url,
        )

        session.add(new_record)
        session.commit()
        session.refresh(new_record)

        return new_record

    except IntegrityError as e:
        session.rollback()
        LOGGER.error(f"IntegrityError: {e}")
        detail_msg = "There was a problem with the data provided. Check the microservice logs for more details"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_msg
        ) from e
