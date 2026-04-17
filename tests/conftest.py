import os
from typing import Generator
from unittest.mock import patch

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer

from service.db.entities import Base
from service.app import app
from tests.mocks import MockCompanyAPI


@fixture(scope="session")
def postgres_database() -> Generator[str, None, None]:
    with PostgresContainer("postgres:16", dbname="postgres") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)

        yield postgres.get_connection_url()


@fixture(scope="session")
def mocked_environment(
    postgres_database: str,
) -> None:
    os.environ["DB_URL"] = postgres_database
    os.environ["COMPANIES_API_URL"] = "http://localhost/"


@fixture
def mocked_settings(
    mocked_environment: None,
) -> Generator[None, None, None]:
    from service.settings import get_settings
    test_settings = get_settings()
    test_settings.companies_api = MockCompanyAPI()

    with patch("service.app.get_settings") as patched_settings:
        patched_settings.return_value = test_settings
        yield


@fixture
def test_app(mocked_settings: None) -> TestClient:
    return TestClient(app)
