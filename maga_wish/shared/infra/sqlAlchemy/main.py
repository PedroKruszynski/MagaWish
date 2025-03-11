from sqlmodel import Session, create_engine

from maga_wish.shared.environment.main import settings
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.whislists.infra.alembic.entities.whislists import Wishlist

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))