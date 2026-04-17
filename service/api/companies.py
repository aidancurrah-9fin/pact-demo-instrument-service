from logging import Logger
from typing import Protocol, runtime_checkable

import requests
from pydantic import HttpUrl

from service.api.models import Company


@runtime_checkable
class CompanyAPIProtocol(Protocol):
    base_url: HttpUrl

    def get_company_by_id(self, company_id: int) -> Company:
        pass


class CompanyAPI(CompanyAPIProtocol):
    def __init__(self, company_api_url: HttpUrl, logger: Logger) -> None:
        self.base_url = company_api_url
        self.logger = logger

    def get_company_by_id(self, company_id: int) -> Company:
        url = f"{self.base_url}/{company_id}"
        response = requests.get(url)
        response.raise_for_status()

        return Company.model_validate(response.json())
