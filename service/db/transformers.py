from service.models import Instrument
from service.db.entities import Instrument as InstrumentTable


class InstrumentTransformer:
    @staticmethod
    def from_db(instrument_orm: InstrumentTable) -> Instrument:
        return Instrument(
            id=instrument_orm.id,
            company_id=instrument_orm.company_id,
            amount=instrument_orm.amount,
        )
