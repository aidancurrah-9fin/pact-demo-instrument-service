from logging import Logger
from typing import Protocol, runtime_checkable

from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from service.db.transformers import InstrumentTransformer
from service.models import Instrument
from service.db.entities import Instrument as InstrumentTable


@runtime_checkable
class InstrumentDBALProtocol(Protocol):
    def get_instrument(self, instrument_id: int) -> Instrument | None:
        pass


class InstrumentDBAL(InstrumentDBALProtocol):
    def __init__(self, connection_url: PostgresDsn, logger: Logger) -> None:
        engine = create_engine(str(connection_url))

        self.session = Session(bind=engine)
        self.logger = logger

    def get_instrument(self, instrument_id: int) -> Instrument | None:
        instrument = self.session.get(InstrumentTable, instrument_id)
        if instrument is None:
            return None
        return InstrumentTransformer.from_db(instrument)
