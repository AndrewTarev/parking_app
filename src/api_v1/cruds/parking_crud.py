from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.schemas.parking_schemas import ParkingIn
from src.core.database.models import Parking


async def create_parking(
    session: AsyncSession,
    parking_in: ParkingIn,
) -> Parking:
    parking = Parking(**parking_in.model_dump())
    session.add(parking)
    await session.commit()
    await session.refresh(parking)  # Заного запрашивается из БД
    return parking


async def get_parking(
    session: AsyncSession,
    parking_id: int,
) -> Parking | None:
    return await session.get(Parking, parking_id)


async def get_all_parkings(
    session: AsyncSession,
) -> list[Parking]:
    stmt = select(Parking).order_by(Parking.id)
    result: Result = await session.execute(stmt)
    parkings = result.scalars().all()
    return list(parkings)
