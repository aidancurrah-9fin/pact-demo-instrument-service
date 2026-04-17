from pydantic import BaseModel

from service.api.models import Company


class Instrument(BaseModel):
    id: int
    company_id: int
    amount: int


class InstrumentResponse(BaseModel):
    id: int
    company: Company
    amount: int
