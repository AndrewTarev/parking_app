# pip install pytest-asyncio
# pip install pytest

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v_1/client/",
        json={
            "name": "Джон",
            "surname": "Смит",
            "credit_card": "3233232313123",
            "car_number": "в344ыв",
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_parking(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v_1/parking/",
        json={
            "address": "ул. Пушкина, дом Колотушкина",
            "opened": True,
            "count_places": 2,
            "count_available_places": 2,
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_driving_in_parking(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v_1/client_parking/",
        json={
            "client_id": 1,
            "parking_id": 1,
        },
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_decrement_parking_place(ac: AsyncClient) -> None:
    response = await ac.get("/api/v_1/parking/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "address": "ул. Пушкина, дом Колотушкина",
        "opened": True,
        "count_places": 2,
        "count_available_places": 1,
    }


@pytest.mark.asyncio
async def test_escape_from_parking(ac: AsyncClient) -> None:
    response = await ac.post(
        "/api/v_1/client_parking/remove",
        json={
            "client_id": 1,
            "parking_id": 1,
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_increment_parking_place(ac: AsyncClient) -> None:
    response = await ac.get("/api/v_1/parking/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "address": "ул. Пушкина, дом Колотушкина",
        "opened": True,
        "count_places": 2,
        "count_available_places": 2,
    }
