from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.schemas.client_schemas import (
    ClientUpdate,
    ClientUpdatePartial,
    ClientIn,
)
from src.core.database.models import Client


async def get_all_clients(session: AsyncSession) -> list[Client]:
    stmt = select(Client).order_by(Client.id)
    result: Result = await session.execute(stmt)
    clients = (
        result.scalars().all()
    )  # scalars - представляет объект списком а не тюплами, если в select(2 таблицы)
    return list(clients)


async def get_client(
    session: AsyncSession,
    client_id: int,
) -> Client | None:
    return await session.get(Client, client_id)


async def create_client(
    session: AsyncSession,
    client_in: ClientIn,
) -> Client:
    client = Client(**client_in.model_dump())
    try:
        session.add(client)
        await session.commit()
        # await session.refresh(client)  # Заного запрашивается из БД
        return client
    except IntegrityError as e:
        if e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Такие имя, фамилия уже существуют",
            )


async def update_client(
    session: AsyncSession,
    client_id: Client,
    client_update: ClientUpdate | ClientUpdatePartial,
    partial: bool = False,
) -> Client:
    for name, value in client_update.model_dump(exclude_unset=partial).items():
        setattr(client_id, name, value)
    await session.commit()
    return client_id


async def delete_client(
    session: AsyncSession,
    client_id: Client,
) -> None:
    await session.delete(client_id)
    await session.commit()
