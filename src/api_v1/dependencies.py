from typing import Annotated

from fastapi import Body, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.cruds import client_crud, client_parking_crud, parking_crud
from src.api_v1.schemas import client_parking_schemas
from src.core.database.db_helper import db_helper
from src.core.database.models import Client, ClientParking, Parking


async def get_client_by_id(
    client_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.get_db),
) -> Client:
    client = await client_crud.get_client(session=session, client_id=client_id)
    if client is not None:
        return client
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Client {client_id} not found",
    )


async def get_parking_by_id(
    parking_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.get_db),
) -> Parking:
    parking = await parking_crud.get_parking(session=session, parking_id=parking_id)
    if parking is not None:
        return parking
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Parking {parking_id} not found",
    )


async def get_client_parking_by_id(
    client_parking_id: Annotated[client_parking_schemas.ClientParkingIn, Body],
    session: AsyncSession = Depends(db_helper.get_db),
) -> client_parking_schemas.ClientParkingOut:
    client_parking = (
        await client_parking_crud.get_client_parking_by_client_id_parking_id(
            client_parking_id=client_parking_id,
            session=session,
        )
    )
    if client_parking is not None:
        return client_parking
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Клиента с такими параметрами не существует",
    )
