from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.cruds import parking_crud
from src.api_v1.dependencies import get_parking_by_id
from src.api_v1.schemas import parking_schemas
from src.core.database import models
from src.core.database.db_helper import db_helper
from src.core.database.models import Parking

router = APIRouter(prefix="/parking", tags=["Parking"])


@router.post(
    "/",
    response_model=parking_schemas.ParkingOut,
    status_code=status.HTTP_201_CREATED,
)
async def insert_parking(
    parking_in: parking_schemas.ParkingIn,
    session: AsyncSession = Depends(db_helper.get_db),
):
    return await parking_crud.create_parking(session=session, parking_in=parking_in)


@router.get("/{parking_id}/", response_model=parking_schemas.ParkingOut)
async def get_parking(parking_id: Parking = Depends(get_parking_by_id)):
    return parking_id


@router.get("/", response_model=list[parking_schemas.ParkingOut])
async def get_all_parkings(
    session: AsyncSession = Depends(db_helper.get_db),
) -> list[Parking]:
    return await parking_crud.get_all_parkings(session=session)
