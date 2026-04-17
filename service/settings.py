from logging import getLogger

from pydantic import PostgresDsn, BaseModel, HttpUrl
from pydantic_settings import BaseSettings

from service.api.companies import CompanyAPI, CompanyAPIProtocol
from service.db.dbal import InstrumentDBAL, InstrumentDBALProtocol


class EnvironmentSettings(BaseSettings):
    db_url: PostgresDsn
    companies_api_url: HttpUrl


class Settings(BaseModel):
    environment: EnvironmentSettings
    dbal: InstrumentDBALProtocol
    companies_api: CompanyAPIProtocol

    class Config:
        arbitrary_types_allowed = True


def get_settings() -> Settings:
    logger = getLogger()
    env_settings = EnvironmentSettings()

    return Settings(
        environment=env_settings,
        dbal=InstrumentDBAL(
            connection_url=env_settings.db_url,
            logger=logger,
        ),
        companies_api=CompanyAPI(
            company_api_url=env_settings.companies_api_url,
            logger=logger,
        )
    )
