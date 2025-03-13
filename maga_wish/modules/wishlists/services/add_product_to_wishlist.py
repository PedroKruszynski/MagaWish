from typing import List, Optional

from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import WishlistRepository
from maga_wish.modules.wishlists.dtos import AddProductToWishlistDTO
from maga_wish.modules.wishlists.infra.sqlAlchemy.entities.wishlists import Wishlist
from maga_wish.shared.infra.http.utils import SessionDep

class AddProductToWishlistService:
    def __init__(self, repository: WishlistRepository):
        self.repository = repository

    async def addProductToWishlist(self, session: SessionDep, data: AddProductToWishlistDTO) -> Optional[List[Wishlist]]:
        return self.repository.getWishlistByUserId(session=session, data=data)
