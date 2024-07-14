from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.cruds import client_parking_crud
from src.api_v1.dependencies import get_client_parking_by_id
from src.api_v1.schemas import client_parking_schemas
from src.core.database.db_helper import db_helper

router = APIRouter(prefix="/client_parking", tags=["Client_parking"])


@router.post(
    "/",
    response_model=client_parking_schemas.ClientParkingOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_client_parking(
    client_parking_in: client_parking_schemas.ClientParkingIn,
    session: AsyncSession = Depends(db_helper.get_db),
):
    return await client_parking_crud.create_client_parking(
        session=session,
        client_parking_in=client_parking_in,
    )


@router.post("/remove")
async def remove_client_parking(
    client_parking_in: client_parking_schemas.ClientParkingIn = Depends(
        get_client_parking_by_id
    ),
    session: AsyncSession = Depends(db_helper.get_db),
):
    return await client_parking_crud.delete_client_parking(
        session=session,
        client_parking_in=client_parking_in,
    )
