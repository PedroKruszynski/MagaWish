from sqlmodel import create_engine

from maga_wish.shared.environment.main import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
