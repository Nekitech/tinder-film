import os
from typing import Any, AsyncGenerator

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv()


# DATABASE_URL = (
#     f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
#     f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
# )

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file="../.env")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings(POSTGRES_DB=os.getenv("POSTGRES_DB"),
                    POSTGRES_USER=os.getenv("POSTGRES_USER"),
                    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
                    POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
                    POSTGRES_PORT=int(os.getenv("POSTGRES_PORT")),
                    )

engine = create_async_engine(settings.database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        yield session
