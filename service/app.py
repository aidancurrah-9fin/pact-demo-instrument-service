from fastapi import FastAPI, HTTPException

from service.models import Company, InstrumentResponse
from service.settings import get_settings

app = FastAPI()


@app.get("/{instrument_id}")
def get_instrument_by_id(instrument_id: int) -> InstrumentResponse:
    settings = get_settings()
    instrument = settings.dbal.get_instrument(instrument_id=instrument_id)

    if instrument is None:
        raise HTTPException(status_code=404, detail="Instrument not found")

    company = settings.companies_api.get_company_by_id(company_id=instrument.company_id)

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return InstrumentResponse(
        id=instrument.id,
        company=company,
        amount=instrument.amount,
    )
