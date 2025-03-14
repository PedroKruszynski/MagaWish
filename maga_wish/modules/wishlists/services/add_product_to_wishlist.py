from maga_wish.modules.wishlists.dtos import AddProductToWishlistDTO
from maga_wish.modules.wishlists.infra.sqlAlchemy.entities.wishlists import Wishlist
from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import (
    WishlistRepository,
)
from maga_wish.shared.infra.http.utils import SessionDep


class AddProductToWishlistService:
    def __init__(self, repository: WishlistRepository):
        self.repository = repository

    async def create(
        self, session: SessionDep, data: AddProductToWishlistDTO
    ) -> Wishlist:
        return self.repository.create(session=session, data=data)
