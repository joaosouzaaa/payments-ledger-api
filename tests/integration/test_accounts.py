from uuid import uuid4

from httpx import AsyncClient

BASE = "/api/v1/accounts"


async def _create(client: AsyncClient, **overrides: str) -> dict[str, str]:
    payload = {"name": "Cash", "type": "asset", "currency": "EUR", **overrides}
    response = await client.post(BASE, json=payload)
    assert response.status_code == 201, response.text
    return response.json()


async def test_create_account_returns_active_account(client: AsyncClient) -> None:
    account = await _create(client)

    assert account["name"] == "Cash"
    assert account["status"] == "active"
    assert account["currency"] == "EUR"


async def test_create_rejects_invalid_currency(client: AsyncClient) -> None:
    response = await client.post(BASE, json={"name": "X", "type": "asset", "currency": "euro"})

    assert response.status_code == 422


async def test_get_unknown_account_returns_problem_json(client: AsyncClient) -> None:
    response = await client.get(f"{BASE}/{uuid4()}")

    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    assert response.json()["title"] == "AccountNotFoundError"


async def test_list_is_paginated(client: AsyncClient) -> None:
    for i in range(3):
        await _create(client, name=f"Acc {i}")

    response = await client.get(BASE, params={"limit": 2, "offset": 1})

    assert response.status_code == 200
    assert [a["name"] for a in response.json()] == ["Acc 1", "Acc 2"]


async def test_rename_account(client: AsyncClient) -> None:
    account = await _create(client)

    response = await client.patch(f"{BASE}/{account['id']}", json={"name": "Petty cash"})

    assert response.status_code == 200
    assert response.json()["name"] == "Petty cash"
    assert (await client.get(f"{BASE}/{account['id']}")).json()["name"] == "Petty cash"


async def test_closed_account_cannot_be_renamed(client: AsyncClient) -> None:
    account = await _create(client)
    close = await client.post(f"{BASE}/{account['id']}/close")
    assert close.json()["status"] == "closed"

    response = await client.patch(f"{BASE}/{account['id']}", json={"name": "New"})

    assert response.status_code == 409
