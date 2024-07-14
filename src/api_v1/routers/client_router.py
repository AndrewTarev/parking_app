from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.cruds import client_crud
from src.api_v1.dependencies import get_client_by_id
from src.api_v1.schemas import client_schemas
from src.core.database.db_helper import db_helper
from src.core.database.models import Client

router = APIRouter(prefix="/client", tags=["Clients"])


@router.post(
    "/",
    response_model=client_schemas.ClientOut,
    status_code=status.HTTP_201_CREATED,
)
async def insert_client(
    client_in: client_schemas.ClientIn,
    session: AsyncSession = Depends(
        db_helper.get_db,
    ),
):
    return await client_crud.create_client(session=session, client_in=client_in)


@router.get("/", response_model=list[client_schemas.ClientOut])
async def get_all_clients(
    session: AsyncSession = Depends(db_helper.get_db),
):
    return await client_crud.get_all_clients(session=session)


@router.get("/{client_id}", response_model=client_schemas.ClientOut)
async def get_client(
    client_id: Client = Depends(get_client_by_id),
):
    return client_id


@router.put("/{client_id}", response_model=client_schemas.ClientOut)
async def update_client(
    client_update: client_schemas.ClientUpdate,
    client_id: Client = Depends(get_client_by_id),
    session: AsyncSession = Depends(db_helper.get_db),
):
    return await client_crud.update_client(
        session=session,
        client_update=client_update,
        client_id=client_id,
    )


@router.patch("/{client_id}", response_model=client_schemas.ClientOut)
async def update_client_partial(
    client_update: client_schemas.ClientUpdatePartial,
    client_id: Client = Depends(get_client_by_id),
    session: AsyncSession = Depends(db_helper.get_db),
):
    return await client_crud.update_client(
        session=session,
        client_update=client_update,
        client_id=client_id,
        partial=True,
    )  # При запросе в свагере указывать валидный json, без запятой в конце {"name": "dddd"}


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: Client = Depends(get_client_by_id),
    session: AsyncSession = Depends(db_helper.get_db),
):
    await client_crud.delete_client(
        client_id=client_id,
        session=session,
    )
