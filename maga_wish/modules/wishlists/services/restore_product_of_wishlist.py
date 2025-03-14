from maga_wish.modules.wishlists.dtos import RestoreProductOfWishlistDTO
from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import (
    WishlistRepository,
)
from maga_wish.shared.infra.http.utils import SessionDep


class RestoreProductOfWishlistService:
    def __init__(self, repository: WishlistRepository):
        self.repository = repository

    async def restoreProduct(
        self, session: SessionDep, data: RestoreProductOfWishlistDTO
    ) -> bool | None:
        userProduct = self.repository.restoreProductOfWishlist(
            session=session, data=data
        )

        return userProduct
