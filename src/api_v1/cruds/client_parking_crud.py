from datetime import datetime, timezone
from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import update, func, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.cruds import parking_crud
from src.api_v1.schemas import client_parking_schemas
from src.core.database.models import ClientParking, Parking


async def create_client_parking(
    session: AsyncSession,
    client_parking_in: client_parking_schemas.ClientParkingIn,
) -> ClientParking:
    client_parking = ClientParking(**client_parking_in.model_dump())

    parking = await parking_crud.get_parking(
        session=session, parking_id=client_parking.parking_id
    )

    if parking.opened is False or parking.count_available_places <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There are no available places for this parking",
        )

    decrement_available_place = (
        update(Parking)
        .where(parking.id == client_parking.parking_id)
        .values(count_available_places=Parking.count_available_places - 1)
    )

    await session.execute(decrement_available_place)
    session.add(client_parking)
    await session.commit()
    return client_parking


async def get_client_parking_by_client_id_parking_id(
    session: AsyncSession,
    client_parking_id: client_parking_schemas.ClientParkingIn,
) -> client_parking_schemas.ClientParkingOut:
    client_parking = ClientParking(**client_parking_id.model_dump())
    stmt = select(ClientParking).where(
        ClientParking.client_id == client_parking.client_id
        and ClientParking.parking_id == client_parking.parking_id
    )
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_client_parking(
    session: AsyncSession,
    client_parking_in: client_parking_schemas.ClientParkingOut,
):
    parking = await parking_crud.get_parking(
        session=session, parking_id=client_parking_in.parking_id
    )

    increment_available_place = (
        update(Parking)
        .where(client_parking_in.parking_id == parking.id)
        .values(count_available_places=Parking.count_available_places + 1)
    )

    time_out = (
        update(ClientParking)
        .where(ClientParking.id == client_parking_in.id)
        .values(time_out=datetime.now())
    )
    await session.execute(time_out)
    hour_on_parking = client_parking_in.check_time_parking
    res_hour = ceil(hour_on_parking)
    valid_res = f"{res_hour} час(ов)"
    await session.execute(increment_available_place)
    await session.delete(client_parking_in)
    await session.commit()
    return {"Время парковки": valid_res}
