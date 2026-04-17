from service.api.companies import CompanyAPIProtocol
from service.api.models import Company, Region


class MockCompanyAPI(CompanyAPIProtocol):
    mock_companies = [
        Company(
            id=1,
            street_name="Mock Street",
            regions=[Region.EUROPE],
        )
    ]

    def __init__(self) -> None:
        self.companies_map = {company.id: company for company in self.mock_companies}

    def get_company_by_id(self, company_id: int) -> Company:
        return self.companies_map.get(company_id)
