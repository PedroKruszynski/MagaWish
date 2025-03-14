from maga_wish.modules.wishlists.infra.sqlAlchemy.repository.main import WishlistRepository
from maga_wish.modules.wishlists.dtos import DeleteProductOfWishlistDTO
from maga_wish.shared.infra.http.utils import SessionDep

class DeleteProductOfWishlistService:
    def __init__(self, repository: WishlistRepository):
        self.repository = repository

    async def deleteProduct(self, session: SessionDep, data: DeleteProductOfWishlistDTO) -> bool | None:
        userProduct = self.repository.deleteProductOfWishlist(session=session, data=data)

        return userProduct
