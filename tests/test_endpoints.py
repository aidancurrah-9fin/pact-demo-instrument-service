import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from service.db.entities import Instrument


@pytest.fixture(scope="module")
def seed_data(postgres_database: str) -> None:
    engine = create_engine(postgres_database)
    with Session(engine) as session:
        base_instrument = Instrument(
            id=1,
            company_id=1,
            amount=1_000_000,
        )
        session.add(base_instrument)
        session.commit()


@pytest.mark.parametrize(
    "company_id, status, expected",
    [
        (1, 200, {"id": 1, "company": {"id": 1, "street_name": "Mock Street", "regions": ["Europe"]}, "amount": 1_000_000}),
        (2, 404, {"detail": "Instrument not found"}),
    ],
)
def test_get_company(
    company_id: int,
    status: int,
    expected: dict,
    mocked_settings: None,
    test_app: TestClient,
    seed_data: None,
) -> None:
    response = test_app.get(f"/{company_id}")

    assert response.status_code == status
    assert response.json() == expected
