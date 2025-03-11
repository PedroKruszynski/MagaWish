from collections.abc import Generator
from typing import Annotated

from sqlmodel import Session
from fastapi import Depends

from maga_wish.shared.infra.sqlAlchemy.main import engine

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]