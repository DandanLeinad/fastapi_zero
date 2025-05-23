import pytest
from sqlalchemy.orm import Session as OrmSession

from fastapi_zero.database import engine, get_session


def test_get_session_yields_session_object():
    generator = get_session()
    session = next(generator)

    assert isinstance(session, OrmSession)
    assert session.get_bind() == engine

    # Finaliza o gerador e garante StopIteration
    with pytest.raises(StopIteration):
        next(generator)
