from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infraestructure.dependencies.db import get_db


def get_repository(repository):
    def _get_repository(session: AsyncSession = Depends(get_db)):
        return repository(session)

    return _get_repository
