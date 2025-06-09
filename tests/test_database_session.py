import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import engine, get_session


@pytest.mark.asyncio
async def test_get_session_yields_session_object():
    async for session in get_session():
        assert isinstance(session, AsyncSession)
        assert session.get_bind() == engine.engine
