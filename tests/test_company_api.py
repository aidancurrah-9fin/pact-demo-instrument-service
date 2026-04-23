from logging import getLogger
from pathlib import Path
from typing import Generator

import pact_ffi
import pytest
from pact import Pact
from pydantic import HttpUrl
from requests import HTTPError

from service.api.companies import CompanyAPI
from service.api.models import Company, Region


@pytest.fixture(autouse=True, scope="session")
def pact_logging():
    pact_ffi.log_to_stderr("INFO")


@pytest.fixture(scope="session")
def mock_company_service() -> Generator[str, None, None]:
    pact = Pact("instrument-service", "company-service")

    (
        pact.upon_receiving(f"A request for company ID 1")
        .given("Company ID 1 exists")
        .with_request("GET", "/1")
        .will_respond_with(200)
        .with_body({"id": 1, "street_name": "Test", "regions": ["Europe"]}, content_type="application/json")
    )
    (
        pact.upon_receiving(f"A request for company ID 2")
        .given("Company ID 2 does not exist")
        .with_request("GET", "/2")
        .will_respond_with(404)
        .with_body({"detail": "Company not found"}, content_type="application/json")
    )

    with pact.serve() as srv:
        yield str(srv.url)

    pact.write_file(Path(__file__).parent.parent / "pacts")


def test_company_api_valid_id(mock_company_service: str) -> None:
    expected_company = Company(
        id=1,
        street_name="Test",
        regions=[Region.EUROPE],
    )

    company_api = CompanyAPI(
        company_api_url=HttpUrl(mock_company_service),
        logger=getLogger(),
    )

    fetched_company = company_api.get_company_by_id(company_id=1)
    assert fetched_company == expected_company



def test_company_api_invalid_id(mock_company_service: str) -> None:
    company_api = CompanyAPI(
        company_api_url=HttpUrl(mock_company_service),
        logger=getLogger(),
    )

    pytest.raises(HTTPError, company_api.get_company_by_id, company_id=2)
